import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import I2C_LCD_driver as LCD
import time
import os, sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def save_user(department, name, output_callback):
    """
    :param department: The department of the user being saved.
    :param name: The name of the user being saved.
    :param output_callback: A callback function used to output messages or information.

    :return: None

    This method is used to save a user's information into the database. It takes three parameters: department, name, and output_callback. The department parameter represents the department of the user being saved. The name parameter represents the name of the user being saved. The output_callback parameter is a callback function that can be used to output messages or information during the execution of the method.

    Example usage:
    save_user("Sales", "John Doe", output_function)

    The method connects to a MySQL database using the provided credentials. It then initializes an RFID reader and an LCD display. The method prompts the user to place their card on the RFID reader and retrieves the unique ID (UID) of the card. The method checks if the user is already registered in the database by searching for the UID in the "students" table. If the user is already registered, a message is displayed on the LCD display and outputted using the output_callback function. If the user is not registered, their information is inserted into the "students" table in the database. A success message is displayed on the LCD display and outputted using the output_callback function.

    The method ensures that the database connection, cursor, GPIO, and LCD resources are properly closed or cleaned up.
    """
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
