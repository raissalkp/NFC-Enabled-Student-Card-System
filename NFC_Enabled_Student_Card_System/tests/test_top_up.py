import os
import sys
import tkinter as tk
from unittest.mock import MagicMock, patch

import pytest

sys.path.insert(0, '/NFC_Enabled_Student_Card_System/module')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Mock external dependencies
sys.modules['mfrc522'] = MagicMock()
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['I2C_LCD_driver'] = MagicMock()
sys.modules['mysql.connector'] = MagicMock()

from NFC_Enabled_Student_Card_System.modules.top_up import NFCSYS


@pytest.fixture
def app():
    """
    Returns an instance of the NFCSYS application.
    """
    master = MagicMock(spec=tk.Tk)
    master.tk = MagicMock()
    master.children = {}  # Properly mock the children dictionary
    master.title = MagicMock(return_value="NFC Student Balance System")
    nfcsys_app = NFCSYS(master)
    nfcsys_app.status_text = MagicMock()
    nfcsys_app.lcd = MagicMock()
    nfcsys_app.read = MagicMock()
    return nfcsys_app


def test_initialization(app):
    """
    This method is used to test the initialisation of the tkinter application.
    """
    app.master.title.assert_called_with("NFC Student Balance System")
    assert isinstance(app.update_balance_button, tk.Button)


def test_update_balance_threaded(app):
    """
    Test that the update_balance_threaded method starts a new thread to handle balance updates.
    """
    with patch('threading.Thread') as mock_thread:
        app.update_balance_threaded()
        mock_thread.assert_called_once()


def test_display_message(app):
    """
    Test method to verify the behaviour  of the display_message method in the application.
    """
    message = "Test message"
    app.display_message(message)
    app.status_text.insert.assert_called_once_with(tk.END, message + '\n')


if __name__ == "__main__":
    pytest.main(['-vv'])
