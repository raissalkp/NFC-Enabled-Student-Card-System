import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import os, sys

sys.path.insert(0, '/home/raissa/NFC-Enabled-Student-Card-System/NFC_Enabled_Student_Card_System/dependencies/')
import I2C_LCD_driver as LCD


def check_attendance(output_callback):
    """
    This method checks the attendance of a student by reading their NFC card. It takes an output_callback as a parameter
    , which is a function that will be called to output messages during the method.
    The method first initialises the MFRC522 reader and the LCD.
    It then displays a message on the LCD screen and calls the output_callback function to display a message.
    Next, it reads the ID and Tag from the NFC card.
    It connects to the MySQL database and executes a SELECT query to retrieve the student's ID and name based on their
    NFC card ID.
    If a matching student is found, it displays a message on the LCD screen and calls the output_callback function to
    display a message. It also inserts the attendance record into the database.
    If no matching student is found, it displays a "User does not exist" message on the LCD screen and calls the
    output_callback function to display a message.
    If any exception occurs during the execution of the method, an error message with the exception details is displayed
    and the GPIO is cleaned up.
    The GPIO.cleanup() method is called in the finally block to ensure that the GPIO pins are cleaned up even if an
    exception occurs.
    """
    try:
        read = SimpleMFRC522()
        lcd = LCD.lcd()
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

    except Exception as e:
        output_callback("Error: " + str(e))
    finally:
        GPIO.cleanup()
