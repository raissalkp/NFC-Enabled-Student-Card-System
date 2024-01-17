from PyQt5 import QtWidgets
from dash import Ui_MainWindow
import check_attendance
import save_user
import unlock


class ExtendedMainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(ExtendedMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)

    def onComboBoxChanged(self, index):
        if self.comboBox.currentText() == "Attendance":
            check_attendance.check_attendance()
        elif self.comboBox.currentText() == "Add New Student":
            save_user.save_user()  # Replace with the actual function to call
        elif self.comboBox.currentText() == "Unlock Door":
            unlock.unlock_door()  # Replace with the actual function to call


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    mainWindow = ExtendedMainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
