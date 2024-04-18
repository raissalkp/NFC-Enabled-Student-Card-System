import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import NFC_Enabled_Student_Card_System.dependencies.I2C_LCD_driver as LCD
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_attendance(output_callback):
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
                    user="nfcsysadmin",
                    passwd="",
                    database="nfcstudentsys"
            ) as db:
                cursor = db.cursor()
                cursor.execute("SELECT id, name FROM students WHERE user_id=%s", (str(id),))
                result = cursor.fetchone()

                lcd.lcd_clear()
                if cursor.rowcount >= 1:
                    lcd.lcd_display_string("Signed in " + result[1])
                    output_callback("Signed in " + result[1])
                    cursor.execute("INSERT INTO attendance (user_id, name) VALUES (%s, %s)",
                                   (result[0], result[1]))
                    db.commit()
                else:
                    lcd.lcd_display_string("User does not exist.")
                    output_callback("User does not exist.")
                    lcd.lcd_clear()
                    lcd.lcd_display_string('Continue? (y/n)', 1, 0)
                    output_callback("Continue? (y/n)")
                    continue_response = input("Continue? (y/n): ")
                    if continue_response.lower() != 'y':
                        continue

            time.sleep(2)
            lcd.lcd_clear()
            lcd.lcd_display_string('Continue? (y/n)', 1, 0)
            output_callback("Continue? (y/n)")
            continue_response = input("Continue? (y/n): ")
            if continue_response.lower() != 'y':
                break

    except Exception as e:
        output_callback("Error: " + str(e))
    finally:
        GPIO.cleanup()
    GPIO.cleanup()
