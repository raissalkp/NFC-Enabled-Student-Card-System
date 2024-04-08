import unittest
from unittest.mock import MagicMock
from check_attendance import check_attendance


class TestCheckAttendance(unittest.TestCase):
    def test_check_attendance(self):
        # Mocking the necessary objects
        mock_output_callback = MagicMock()
        mock_read = MagicMock()
        mock_lcd = MagicMock()
        mock_cursor = MagicMock()
        mock_db = MagicMock()

        mock_read.read.return_value = ("RFID_UID", "Tag")
        mock_cursor.fetchone.return_value = (1, "John Doe")
        mock_db.cursor.return_value = mock_cursor

        with unittest.mock.patch("mysql.connector.connect", return_value=mock_db):
            with unittest.mock.patch("time.sleep", side_effect=lambda x: None):
                with unittest.mock.patch("RPi.GPIO.cleanup"):
                    check_attendance(mock_output_callback)

        # Assertions
        self.assertEqual(mock_output_callback.call_count, 2)
        mock_lcd.lcd_display_string.assert_called_with("Place Card to ", 1, 0)
        mock_lcd.lcd_clear.assert_called_once()
        mock_cursor.execute.assert_called_with("INSERT INTO attendance (user_id, name) VALUES (%s, %s)",
                                               ("RFID_UID", "John Doe"))


if __name__ == '__main__':
    unittest.main()
