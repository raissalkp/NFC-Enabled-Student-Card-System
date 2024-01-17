import threading
from PyQt5 import QtCore, QtWidgets
from dash import Ui_MainWindow
import check_attendance
import save_user
import unlock


class ExtendedMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    update_output_signal = QtCore.pyqtSignal(str)

    def __init__(self, parent=None):
        super(ExtendedMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)
        self.update_output_signal.connect(self.update_output)

    def onComboBoxChanged(self, index):
        if self.comboBox.currentText() == "Attendance":
            self.start_check_attendance()
        elif self.comboBox.currentText() == "Add New Student":
            self.start_save_user()
        elif self.comboBox.currentText() == "Unlock Door":
            self.start_unlock()

    def start_check_attendance(self):
        user_input = self.lineEdit_input.text()
        thread = threading.Thread(
            target=lambda: check_attendance.check_attendance(user_input, self.update_output_signal.emit))
        thread.start()

    def start_save_user(self):
        user_input = self.lineEdit_input.text()
        thread = threading.Thread(target=lambda: save_user.save_user(user_input, self.update_output_signal.emit))
        thread.start()

    def start_unlock(self):
        user_input = self.lineEdit_input.text()
        thread = threading.Thread(target=lambda: unlock.unlock_door(user_input, self.update_output_signal.emit))
        thread.start()

    def update_output(self, message):
        # This function updates the UI and is triggered by the signal
        self.label_output.setText(message)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ExtendedMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
