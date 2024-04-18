from NFC_Enabled_Student_Card_System.modules.main import NFCSYS, start_flask_app, get_recent_attendance
import unittest
from unittest.mock import patch, MagicMock, ANY
import tkinter as tk
import sys, os


sys.modules['mfrc522'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['RPi'] = MagicMock()
sys.modules['smbus'] = MagicMock()
sys.modules['save_user'] = MagicMock()
sys.modules['unlock'] = MagicMock()


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestNFCSYS(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = NFCSYS(self.root)

    @patch('mysql.connector.connect')
    def test_register_user_integration(self, mock_connect):
        # Setup the mock connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Set up the test scenario
        self.app.department_var.set("IT")
        self.app.name_entry.insert(0, "Alice")
        self.app.register_user()

        # Assert the correct SQL command was executed
        mock_cursor.execute.assert_called_with(ANY, ("IT", "Alice"))
        mock_conn.commit.assert_called_once()

    def tearDown(self):
        self.root.destroy()


if __name__ == '__main__':
    unittest.main()
