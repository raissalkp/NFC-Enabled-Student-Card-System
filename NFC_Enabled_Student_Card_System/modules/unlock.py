import I2C_LCD_driver
import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def is_allowed_to_unlock(tag_id, department):
    db = mysql.connector.connect(
        host="localhost",
        user="nfcsysadmin",
        passwd="",
        database="nfcstudentsys"
    )

    cursor = db.cursor()

    tag_id = tag_id.strip()
    department = department.strip()

    try:
        cursor.execute("SELECT * FROM students WHERE user_id = %s AND department = %s", (tag_id, department))
        record = cursor.fetchone()

        if record is not None:
            print(f"Query result: {record}")
            return True
        else:
            print("No records found for the given tag ID and department.")
            return False

    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        return False
    finally:
        db.close()


def unlock_door(department, output_callback):
    buzzer = 19
    relay = 26
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(buzzer, GPIO.OUT)
    GPIO.setup(relay, GPIO.OUT)
    lcd = I2C_LCD_driver.lcd()
    read = SimpleMFRC522()

    try:
        lcd.lcd_clear()
        lcd.lcd_display_string("Place your Tag", 1, 0)
        output_callback("Place your Tag")

        id, _ = read.read()
        id = str(id).strip()

        if is_allowed_to_unlock(id, department):
            output_callback("Access granted for department: " + department)
            GPIO.output(relay, GPIO.LOW)
            GPIO.output(buzzer, GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer, GPIO.LOW)
            GPIO.output(relay, GPIO.HIGH)  # Ensure relay is turned off after opening
        else:
            output_callback("Access denied for department: " + department)
            for _ in range(3):
                GPIO.output(buzzer, GPIO.HIGH)
                sleep(0.3)
                GPIO.output(buzzer, GPIO.LOW)
                sleep(0.3)
    finally:
        GPIO.cleanup()

