import pytest
import sys
import os
import tkinter as tk
from unittest.mock import MagicMock, patch

sys.path.insert(0, '/NFC_Enabled_Student_Card_System/modules')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

sys.modules['mfrc522'] = MagicMock()
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['I2C_LCD_driver'] = MagicMock()

from NFC_Enabled_Student_Card_System.modules.parking_sys import ParkingSystem


@pytest.fixture
def app():
    """
    Create and return an instance of the ParkingSystem class.
    """
    master = MagicMock(spec=tk.Tk)
    master.tk = MagicMock()
    master.children = {}
    master.title.return_value = "NFC Parking System"
    app = ParkingSystem(master)
    app.status_text = MagicMock()
    return app


def test_initialization(app):
    """
    Check if the app initialization is correct.
    """
    assert app.master.title() == "NFC Parking System"
    assert isinstance(app.hour_entry, tk.Entry)


def test_start_parking_session_threaded(app):
    """
    Test the start_parking_session_threaded method.
    """
    with patch('threading.Thread') as mock_thread:
        app.start_parking_session_threaded()
        mock_thread.assert_called_once()


def test_display_message(app):
    """
    This method tests the `display_message` method of the given `app` object. It passes a test message, "Welcome to Parking System", to the `display_message` method and asserts that the `insert` method of the `status_text` attribute of the `app` object is called once with the test message appended with a newline character.
    """
    test_message = "Welcome to Parking System"
    app.display_message(test_message)
    app.status_text.insert.assert_called_once_with(tk.END, test_message + '\n')


if __name__ == "__main__":
    pytest.main(['-vv'])
