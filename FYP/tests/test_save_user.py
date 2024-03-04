import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('/home/raissa/FYP/FYP')


class TestSaveUser(unittest.TestCase):
    @patch('user_module.builtins.input',
           side_effect=['John Doe', 'IT', 'n'])  # Simulated inputs for new user details and to stop the loop
    @patch('save_user.LCD.lcd')
    @patch('save_user.mysql.connector.connect')
    @patch('save_user.SimpleMFRC522')
    @patch('save_user.GPIO.cleanup')
    @patch('save_user.time.sleep', side_effect=lambda x: None)
    def test_add_new_user(self, mock_sleep, mock_gpio_cleanup, mock_rfid, mock_db, mock_lcd, mock_input):
        from save_user import save_user

        # Setup mock RFID read
        mock_rfid.return_value.read.return_value = (123456789, 'Test Tag')

        # Setup mock database connection and cursor to simulate no existing user
        mock_cursor = MagicMock()
        mock_cursor.rowcount = 0
        mock_db.return_value.cursor.return_value = mock_cursor

        # Mock output callback
        mock_output_callback = MagicMock()

        # Execute the function under test
        save_user("New User Input", mock_output_callback)

        # Verify LCD and callback interactions
        mock_lcd_instance = mock_lcd.return_value
        mock_lcd_instance.lcd_display_string.assert_any_call('Enter new name', 1, 0)
        mock_lcd_instance.lcd_display_string.assert_any_call('Enter new department', 1, 0)
        mock_lcd_instance.lcd_display_string.assert_any_call('User John Doe\nSaved', 1, 0)
        mock_lcd_instance.lcd_display_string.assert_any_call('Department IT\nSaved', 2, 0)

        # Verify database insert operation
        mock_cursor.execute.assert_called_with("INSERT INTO users (rfid_uid, name, department) VALUES (%s, %s, %s)",
                                               (123456789, 'John Doe', 'IT'))
        mock_db.return_value.commit.assert_called_once()

        # Verify GPIO cleanup was called
        mock_gpio_cleanup.assert_called()


if __name__ == '__main__':
    unittest.main()
