import threading
from PyQt5 import QtWidgets
from dash import Ui_MainWindow
import check_attendance
import save_user
import unlock


def start_check_attendance():
    thread = threading.Thread(target=check_attendance.checkattendance)
    thread.start()


def start_save_user():
    thread = threading.Thread(target=save_user.saveuser)
    thread.start()


def start_unlock():
    thread = threading.Thread(target=unlock.unlock)
    thread.start()


class ExtendedMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExtendedMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)

    def onComboBoxChanged(self, index):
        if self.comboBox.currentText() == "Attendance":
            start_check_attendance()
        elif self.comboBox.currentText() == "Add New Student":
            start_save_user()
        elif self.comboBox.currentText() == "Unlock Door":
            start_unlock()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ExtendedMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
