import pytest
import sys, os
import tkinter as tk
import threading
from unittest.mock import MagicMock, patch

sys.path.insert(0, 'NFC_Enabled_Student_Card_System/modules')
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

sys.modules['RPi'] = MagicMock()
sys.modules['RPi.GPIO'] = MagicMock()
sys.modules['check_attendance'] = MagicMock()
sys.modules['save_user'] = MagicMock()
sys.modules['unlock'] = MagicMock()

from NFC_Enabled_Student_Card_System.modules.main import NFCSYS


class TestNFCSYS:
    """

    The TestNFCSYS class represents a set of unit tests for the NFCSYS class.

    Methods:
        - setup_method(): A pytest fixture that sets up the necessary mocks and initialises the nfcsys_obj.
        - test_init(): Tests whether nfcsys_obj's master attribute is set correctly.
        - test_start_api_and_open_browser(): Tests whether start_api_and_open_browser method calls the Thread class.
        - test_display_message(): Tests whether display_message method calls the insert method of the text widget.
        - test_unlock_door_threaded(): Tests whether unlock_door_threaded method calls the Thread class.
        - test_register_user_threaded(): Tests whether register_user_threaded method calls the Thread class.
        - test_check_attendance_threaded(): Tests whether check_attendance_threaded method calls the Thread class.
    """
    @pytest.fixture(autouse=True)
    def setup_method(self):
        self.master = MagicMock(spec=tk.Tk)
        self.master.tk = MagicMock()
        self.master.children = {}
        # Mock the text widget specifically
        self.text_mock = MagicMock()
        self.nfcsys_obj = NFCSYS(self.master)
        self.nfcsys_obj.text = self.text_mock

    def test_init(self):
        assert self.nfcsys_obj.master == self.master

    def test_start_api_and_open_browser(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.start_api_and_open_browser()
            mock_Thread.assert_called_once()

    def test_display_message(self):
        test_message = 'Test Message'
        self.nfcsys_obj.display_message(test_message)
        self.text_mock.insert.assert_called_once_with(tk.END, test_message + '\n')

    def test_unlock_door_threaded(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.unlock_door_threaded()
            mock_Thread.assert_called_once()

    def test_register_user_threaded(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.register_user_threaded()
            mock_Thread.assert_called_once()

    def test_check_attendance_threaded(self):
        with patch('threading.Thread') as mock_Thread:
            self.nfcsys_obj.check_attendance_threaded()
            mock_Thread.assert_called_once()
