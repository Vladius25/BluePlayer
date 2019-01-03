import sys
from PyQt5 import QtWidgets
import src.gui


class BlueApp(QtWidgets.QMainWindow, src.gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = BlueApp()
    window.show()
    app.exec_()
