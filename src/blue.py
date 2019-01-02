import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GLib
import threading
import os


class BlueConnector:

    def __init__(self):
        DBusGMainLoop(set_as_default=True)
        self.bus = dbus.SystemBus()
        self.manager = dbus.Interface(self.bus.get_object("org.bluez", "/"),
                                      "org.freedesktop.DBus.ObjectManager")
        self.device = None
        self.props_iface = None
        self.state = {"Status": "Stopped", "Position": 0, "Title": ""}

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
        threading.Thread(target=loop.run).start()

    def handler(self, *args, **kwargs):
        self.state["Status"] = str(self.props_iface.Get("org.bluez.MediaPlayer1", "Status"))
        self.state["Position"] = int(self.props_iface.Get("org.bluez.MediaPlayer1", "Position"))
        self.state["Title"] = str(self.props_iface.Get("org.bluez.MediaPlayer1", "Track")["Title"])
