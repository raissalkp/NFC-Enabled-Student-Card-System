#!/usr/bin/env python
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mysql.connector
import I2C_LCD_driver as LCD


def check_attendance():
    db = mysql.connector.connect(
      host="localhost",
      user="attendanceadmin",
      passwd="pimylifeup",
      database="attendancesystem"
    )

    cursor = db.cursor()
    read = SimpleMFRC522()

    lcd = LCD.lcd()


    try:
        while True:
            lcd.lcd_clear()
            lcd.lcd_display_string("Place Card to ",1,0)
            lcd.lcd_display_string("record attendance",2,0)
            id,Tag = read.read()

            cursor.execute("Select id, name FROM users where rfid_uid="+str(id))
            result = cursor.fetchone()

            lcd.lcd_clear()

            if cursor.rowcount >=1:
                lcd.lcd_display_string("Signed in " + result[1])
                cursor.execute("INSERT INTO attendance (user_id) VALUES (%s)", (result[0],))
                db.commit()
            else:
                lcd.lcd_display_string("User does not exist.")
            time.sleep(2)
    finally:
        GPIO.cleanup()