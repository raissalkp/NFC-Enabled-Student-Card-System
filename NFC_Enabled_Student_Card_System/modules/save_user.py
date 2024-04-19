import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import I2C_LCD_driver as LCD
import time
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save_user(department, name, output_callback):
    db = mysql.connector.connect(
        host="localhost",
        user="nfcsysadmin",
        passwd="",
        database="nfcstudentsys"
    )

    cursor = db.cursor()
    read = SimpleMFRC522()

    lcd = LCD.lcd()

    try:
        lcd.lcd_clear()
        lcd.lcd_display_string("Place Card to ", 1, 0)
        lcd.lcd_display_string("register", 2, 0)
        output_callback("Place Card to register")

        id, Tag = read.read()  # Fetch RFID UID
        output_callback(f"RFID UID: {id}")

        cursor.execute("SELECT id FROM students WHERE user_id=%s", (id,))
        record = cursor.fetchone()

        if record:
            lcd.lcd_clear()
            lcd.lcd_display_string("User already registered.", 1, 1)
            output_callback("User already registered.")
            time.sleep(2)
        else:
            sql_insert = "INSERT INTO students (user_id, name, department) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (id, name, department))
            db.commit()

            lcd.lcd_clear()
            lcd.lcd_display_string("User " + name + " Saved", 1, 0)
            output_callback("User " + name + " Saved")
            lcd.lcd_display_string("Department " + department + " Saved", 2, 0)
            output_callback("Department " + department + " Saved")
            time.sleep(2)

    finally:
        cursor.close()
        db.close
        GPIO.cleanup()
