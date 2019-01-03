import os
import sys
from PyQt5 import QtWidgets

from src.blueapp import BlueApp

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BlueApp()
    window.show()
    app.exec_()
    os._exit(0)
