import unittest
import sys
from unittest.mock import patch, MagicMock
from PyQt5 import QtWidgets
sys.path.append('/home/raissa/FYP/FYP')
# Assume 'main.py' content is placed in a module named main_module
from main import ExtendedMainWindow



class TestMainPy(unittest.TestCase):
    def setUp(self):
        self.app = QtWidgets.QApplication([])
        self.main_window = ExtendedMainWindow()

    def test_initialization(self):
        # Test initial GUI states, e.g., comboBox has the correct items
        self.assertEqual(self.main_window.comboBox.count(), 3)  # Assuming 3 items
        self.assertTrue(self.main_window.dateTimeEdit.isReadOnly())

    @patch('main_module.threading.Thread')
    def test_combobox_change_attendance(self, mock_thread):
        # Simulate selecting "Attendance" in the comboBox
        self.main_window.comboBox.setCurrentIndex(0)  # Assuming "Attendance" is at index 0
        self.main_window.onComboBoxChanged(0)
        mock_thread.assert_called_once()

    # Similar tests can be created for "Add New Student" and "Unlock Door" options


if __name__ == '__main__':
    unittest.main()
