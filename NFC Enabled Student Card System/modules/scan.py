import I2C_LCD_driver
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep


def scan(user_input, output_callback):
    buzzer = 19

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(buzzer, GPIO.OUT)

    lcd = I2C_LCD_driver.lcd()

    scan = SimpleMFRC522()

    try:
        print("Now place your Tag to scan")
        output_callback("Now place your Tag to scan")
        lcd.lcd_display_string("Place your Tag", 1, 1)
        output_callback("Place your Tag")
        scan.write("Tag ID")
        output_callback("Tag ID")
        id, Tag = scan.read()
        print("Your Tag ID is : " + str(id))
        output_callback("Your Tag ID is : " + str(id))
        lcd.lcd_clear()
        lcd.lcd_display_string("Tag ID", 1, 5)
        output_callback("Tag ID")
        lcd.lcd_display_string(str(id), 2, 1)

        GPIO.output(buzzer, GPIO.HIGH)
        sleep(0.5)
        GPIO.output(buzzer, GPIO.LOW)

    finally:
        GPIO.cleanup()
