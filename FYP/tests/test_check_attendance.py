import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('C:/Users/raiss/OneDrive - TUS MM/SDB/Year 4/FYP/FYP')


class TestCheckAttendance(unittest.TestCase):
    @patch('check_attendance.LCD.lcd')
    @patch('check_attendance.mysql.connector.connect')
    @patch('check_attendance.SimpleMFRC522')
    @patch('check_attendance.GPIO.cleanup')
    @patch('check_attendance.time.sleep', side_effect=lambda x: None)  # To skip actual sleeping
    def test_successful_attendance(self, mock_sleep, mock_gpio_cleanup, mock_rfid, mock_db, mock_lcd):
        from check_attendance import check_attendance

        # Setup mock RFID read
        mock_rfid.return_value.read.return_value = (123456789, 'Test Tag')

        # Setup mock database connection and query results
        mock_cursor = MagicMock()
        mock_cursor.fetchone.return_value = (1, 'John Doe')
        mock_cursor.rowcount = 1
        mock_db.return_value.__enter__.return_value.cursor.return_value = mock_cursor

        # Mock output callback
        mock_output_callback = MagicMock()

        # Assuming the function will now exit after one iteration for testing purposes
        with self.assertRaises(StopIteration):
            check_attendance(None, mock_output_callback)

        # Verify LCD messages
        mock_lcd_instance = mock_lcd.return_value
        mock_lcd_instance.lcd_display_string.assert_any_call("Place Card to ", 1, 0)
        mock_lcd_instance.lcd_display_string.assert_any_call("record attendance", 2, 0)
        mock_lcd_instance.lcd_display_string.assert_called_with("Signed in John Doe")

        # Verify database interactions
        mock_cursor.execute.assert_called()
        mock_db.return_value.commit.assert_called_once()

        # Verify output callback was called with the correct message
        mock_output_callback.assert_called_with("Signed in John Doe")

        # Verify GPIO cleanup was called
        mock_gpio_cleanup.assert_called()


if __name__ == '__main__':
    unittest.main()
