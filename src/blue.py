import dbus
from PyQt5 import QtCore
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QMovie, QPainter, QBitmap
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import threading
import os
import src.qrc

from src.imager import Imager


class BlueConnector:

    def __init__(self, app):
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),
                                      "org.freedesktop.DBus.ObjectManager")
        self.device = None
        self.props_iface = None
        self.state = {"Launch": True, "Last": "", "Status": "Stopped", "Position": 0, "Duration": 0, "Title": "",
                      "Artist": "", "Album": ""}
        self.app = app
        global counter
        counter = 0

    def connect(self):
        connected_devices = self.find_devs()
        self.choose_dev(connected_devices)
        self.init_handler()

        return self.device

    def find_devs(self):
        objects = self.manager.GetManagedObjects()
        connected_devices = []

        for path, interfaces in objects.items():
            if "org.bluez.Device1" not in interfaces.keys():
                continue

            properties = objects[path]["org.bluez.Device1"]
            if properties["Connected"]:
                dev = dbus.Interface(self.bus.get_object("org.bluez", path), "org.bluez.MediaControl1")
                connected_devices.append({"device": dev, "props": properties})

        return connected_devices

    def choose_dev(self, connected_devices):
        num = 0
        if len(connected_devices) < 1:
            print("No devices connected")
            os._exit(0)
        elif len(connected_devices) > 1:
            print("Choose device")
            for i, dev in enumerate(connected_devices):
                print(str(i) + ") " + dev["props"]["Name"])
            print("q) Exit")
            num = input("Choose: ")

        try:
            num = int(num)
            self.device = connected_devices[num]["device"]
        except (ValueError, IndexError):
            os._exit(0)

    def init_handler(self):
        loop = GLib.MainLoop()
        path = self.device.object_path + "/player0"
        self.props_iface = dbus.Interface(self.bus.get_object("org.bluez", path), "org.freedesktop.DBus.Properties")
        self.bus.get_object("org.bluez", path).connect_to_signal(
            "PropertiesChanged", self.handler)
        self.handler()
        threading.Thread(target=loop.run).start()

    def handler(self, *args, **kwargs):
        self.state["Status"] = str(self.props_iface.Get("org.bluez.MediaPlayer1", "Status"))
        self.state["Position"] = int(self.props_iface.Get("org.bluez.MediaPlayer1", "Position"))
        self.state["Duration"] = int(self.props_iface.Get("org.bluez.MediaPlayer1", "Track")["Duration"])
        self.state["Title"] = str(self.props_iface.Get("org.bluez.MediaPlayer1", "Track")["Title"])
        self.state["Artist"] = str(self.props_iface.Get("org.bluez.MediaPlayer1", "Track")["Artist"])
        self.state["Album"] = str(self.props_iface.Get("org.bluez.MediaPlayer1", "Track")["Album"])

        if not self.state["Last"] == self.state["Title"] or self.state["Launch"]:
            self.app.label.setScaledContents(False)
            movie = QMovie(":/images/load.gif")
            movie.setScaledSize(QSize(200, 200))
            self.app.label.setMovie(movie)
            movie.start()
            threading.Thread(target=self.load_img, args=[counter]).start()

            self.state["Launch"] = False
            self.state["Last"] = self.state["Title"]
            self.app.status_label.setText(self.state["Artist"] + " \"" + self.state["Title"] + "\"")

    def load_img(self, c):
        global counter
        counter += 1
        imager = Imager(self.state["Title"], self.state["Artist"])
        data = imager.get_data()

        if (c + 1 != counter):
            return

        pixmap = QPixmap()
        pixmap.loadFromData(data)

        map = QBitmap(pixmap.size())
        map.fill(Qt.color0)
        painter = QPainter(map)
        painter.setBrush(Qt.color1)
        painter.drawRoundedRect(0, 0, pixmap.width(), pixmap.height(), 10, 10);
        painter.end()

        self.app.label.setScaledContents(True)
        pixmap.setMask(map)
        self.app.label.setPixmap(
            pixmap.scaled(self.app.label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
