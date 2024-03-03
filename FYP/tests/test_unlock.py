import pytest
from unittest.mock import patch, MagicMock
from unlock import unlock_door  # Make sure this matches the actual import

@patch('unlock.GPIO')
@patch('unlock.I2C_LCD_driver.my_lcd')  # Assuming `my_lcd` is the instance of the LCD used
def test_unlock_door(MockLCD, MockGPIO):
    MockLCD.lcd_display_string = MagicMock()
    MockGPIO.setup = MagicMock()
    MockGPIO.output = MagicMock()

    unlock_door()

    MockGPIO.setup.assert_any_call(19, MockGPIO.OUT)
    MockGPIO.setup.assert_any_call(26, MockGPIO.OUT)
    MockGPIO.output.assert_any_call(26, MockGPIO.HIGH)
    MockGPIO.output.assert_any_call(19, MockGPIO.LOW)
    MockLCD.lcd_display_string.assert_called_with("Door Unlocked!", 1)
