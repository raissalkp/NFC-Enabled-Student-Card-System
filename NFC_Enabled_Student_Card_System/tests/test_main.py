import pytest
import sys
import tkinter as tk
import threading
from unittest.mock import MagicMock, patch

sys.path.insert(0, 'NFC_Enabled_Student_Card_System/modules')

# Mock modules that are not available or not necessary for the unit tests
sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['check_attendance'] = MagicMock()
sys.modules['save_user'] = MagicMock()
sys.modules['unlock'] = MagicMock()

from NFC_Enabled_Student_Card_System.modules.main import NFCSYS


class TestNFCSYS:
    @pytest.fixture(autouse=True)
    def setup_method(self):
        # Mock the tkinter root window and its necessary components
        self.master = MagicMock(spec=tk.Tk)
        self.master.tk = MagicMock()
        self.master.children = {}
        # Mock the text widget specifically
        self.text_mock = MagicMock()
        self.nfcsys_obj = NFCSYS(self.master)
        # Replace the text attribute in your nfcsys_obj with the mocked text widget
        self.nfcsys_obj.text = self.text_mock

    def test_init(self):
        assert self.nfcsys_obj.master == self.master

    def test_start_api_and_open_browser(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.start_api_and_open_browser()
            mock_Thread.assert_called_once()  # Ensure a new thread was created once 

    def test_display_message(self):
        test_message = 'Test Message'
        self.nfcsys_obj.display_message(test_message)
        # Use the mocked text attribute for assertion
        self.text_mock.insert.assert_called_once_with(tk.END, test_message + '\n')

    def test_unlock_door_threaded(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.unlock_door_threaded()
            mock_Thread.assert_called_once()  # Check that threading.Thread has been called 

    def test_register_user_threaded(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.register_user_threaded()
            mock_Thread.assert_called_once()  # Ensure that threading.Thread was called once

    def test_check_attendance_threaded(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.check_attendance_threaded()
            mock_Thread.assert_called_once()  # Ensure that threading.Thread was called once
