#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import I2C_LCD_driver as LCD


def check_attendance(user_input, output_callback):
    try:
        read = SimpleMFRC522()
        lcd = LCD.lcd()

        while True:
            lcd.lcd_clear()
            lcd.lcd_display_string("Place Card to ", 1, 0)
            lcd.lcd_display_string("record attendance", 2, 0)
            output_callback("Place Card to record attendance")

            id, Tag = read.read()

            with mysql.connector.connect(
                    host="localhost",
                    user="attendanceadmin",
                    passwd="pimylifeup",
                    database="attendancesystem"
            ) as db:
                cursor = db.cursor()
                cursor.execute("SELECT id, name FROM users WHERE rfid_uid=%s", (str(id),))
                result = cursor.fetchone()

                lcd.lcd_clear()
                if cursor.rowcount >= 1:
                    lcd.lcd_display_string("Signed in " + result[1])
                    output_callback("Signed in " + result[1])
                    cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],))
                    db.commit()
                else:
                    lcd.lcd_display_string("User does not exist.")
                    output_callback("User does not exist.")

            # Handle 'continue' logic through your PyQt5 interface instead of console input
            # Wait for a signal from the GUI or use a different mechanism

            time.sleep(2)
    except Exception as e:
        output_callback("Error: " + str(e))
    finally:
        GPIO.cleanup()
    GPIO.cleanup()
