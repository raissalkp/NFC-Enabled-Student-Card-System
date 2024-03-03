import unittest
from unittest.mock import patch, MagicMock


class TestUnlockDoor(unittest.TestCase):
    @patch('unlock_module.is_allowed_to_unlock', return_value=True)
    @patch('unlock_module.SimpleMFRC522')
    @patch('unlock_module.I2C_LCD_driver.lcd')
    @patch('unlock_module.GPIO')
    @patch('unlock_module.sleep', side_effect=lambda x: None)  # To skip actual sleeping
    @patch('builtins.input', side_effect=['y', 'n'])  # Simulate user input to continue, then stop
    def test_access_granted(self, mock_input, mock_sleep, mock_gpio, mock_lcd, mock_rfid, mock_is_allowed):
        from unlock import unlock_door

        # Setup the RFID reader's return value
        mock_rfid.return_value.read.return_value = (123456789, 'Test Tag')

        # Call the function
        unlock_door('IT', MagicMock())

        # Verify that the LCD displayed the correct messages
        mock_lcd_instance = mock_lcd.return_value
        mock_lcd_instance.lcd_display_string.assert_any_call('Door lock system', 1, 0)
        mock_lcd_instance.lcd_display_string.assert_any_call('Place your Tag', 1, 0)
        mock_lcd_instance.lcd_display_string.assert_any_call('Access granted for department: IT', 1, 0)

        # Verify GPIO actions for access granted
        mock_gpio.output.assert_any_call(26, mock_gpio.LOW)  # Relay
        mock_gpio.output.assert_any_call(19, mock_gpio.HIGH)  # Buzzer on
        mock_gpio.output.assert_any_call(19, mock_gpio.LOW)  # Buzzer off

        # Ensure cleanup was called
        mock_gpio.cleanup.assert_called_once()


if __name__ == '__main__':
    unittest.main()
