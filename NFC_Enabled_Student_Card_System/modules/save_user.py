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
        while True:
            lcd.lcd_clear()
            lcd.lcd_display_string("Place Card to ", 1, 0)
            lcd.lcd_display_string("register", 2, 0)
            output_callback("Place Card to register")

            id, Tag = read.read()  # Fetch RFID UID
            print("RFID UID:", id)

            cursor.execute("SELECT id FROM students WHERE user_id=%s", (id,))
            record = cursor.fetchone()

            if record:
                lcd.lcd_clear()
                lcd.lcd_display_string("Overwrite existing user?", 1, 1)
                output_callback("Overwrite existing user?")
                overwrite = input("Overwrite (Y/N)? ")

                if overwrite[0] == 'Y' or overwrite[0] == 'y':
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Overwriting user.", 1, 2)
                    output_callback("Overwriting user.")
                    time.sleep(1)
                    sql_update = "UPDATE students SET name = %s WHERE user_id=%s"
                    cursor.execute(sql_update, (name, id))
                else:
                    lcd.lcd_clear()
                    lcd.lcd_display_string('Continue? (y/n)', 1, 0)
                    output_callback("Continue? (y/n)")
                    continue_response = input("Continue? (y/n): ")
                    if continue_response.lower() != 'y':
                        continue
            else:
                sql_insert = "INSERT INTO students (user_id, name, department) VALUES (%s, %s, %s)"
                cursor.execute(sql_insert, (id, name, department))

            db.commit()

            lcd.lcd_clear()
            lcd.lcd_display_string("User " + name + "\nSaved", 1, 0)
            output_callback("User " + name + "\nSaved")
            lcd.lcd_display_string("Department " + department + "\nSaved", 2, 0)
            output_callback("Department " + department + "\nSaved")
            time.sleep(2)

            lcd.lcd_clear()
            lcd.lcd_display_string('Continue? (y/n)', 1, 0)
            output_callback("Continue? (y/n)")
            continue_response = input("Continue? (y/n): ")
            if continue_response.lower() != 'y':
                break
    finally:
        GPIO.cleanup()

    GPIO.cleanup()

