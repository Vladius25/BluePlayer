from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt

import src.gui
from src.blue import BlueConnector
from src.media import MediaController
import alsaaudio

class BlueApp(QtWidgets.QMainWindow, src.gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.connector = BlueConnector(self)
        device = self.connector.connect()
        self.player = MediaController(device)

        if self.connector.state["Status"] == "playing":
            self.playButton.setText("Pause")
        else:
            self.playButton.setText("Play")

        self.label.setAlignment(Qt.AlignCenter)
        self.status_label.setAlignment(Qt.AlignCenter)

        self.playButton.clicked.connect(self.play)
        self.nextButton.clicked.connect(self.next)
        self.prevButton.clicked.connect(self.prevoius)

        self.audio = alsaaudio.Mixer()
        self.sound_slider.setMinimum(0)
        self.sound_slider.setMaximum(100)
        if not self.audio.getmute():
            self.sound_slider.setValue(self.audio.getvolume()[0])
        self.sound_slider.valueChanged.connect(self.sound_change)


    def play(self):
        if self.connector.state["Status"] == "playing":
            self.player.stop()
            self.playButton.setText("Play")
        else:
            self.playButton.setText("Pause")
            self.player.play()

    def next(self):
        self.player.next()

    def prevoius(self):
        self.player.prevoius()

    def sound_change(self):
        volume = self.sound_slider.value()
        if volume == 0:
            self.audio.setmute(1)
        else:
            self.audio.setmute(0)
            self.audio.setvolume(volume)



