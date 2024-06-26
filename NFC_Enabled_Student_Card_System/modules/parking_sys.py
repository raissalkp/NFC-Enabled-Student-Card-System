import tkinter as tk
from tkinter import messagebox
import threading
from datetime import datetime, timedelta
from decimal import Decimal
import mysql.connector
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import os, sys

sys.path.insert(0, '/home/raissa/NFC-Enabled-Student-Card-System/NFC_Enabled_Student_Card_System/dependencies/')
import I2C_LCD_driver as LCD

db_config = {
    'host': "localhost",
    'user': "nfcsysadmin",
    'passwd': "",
    'database': "nfcstudentsys"
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


class ParkingSystem:
    """
    This class represents the NFC Parking System.

    Methods:
    - display_message: Displays a message in the status text area.
    - start_parking_session_threaded: Starts a parking session in a separate thread.
    - start_parking_session: Starts a parking session.
    - end_parking_session_threaded: Ends a parking session in a separate thread.
    - end_parking_session: Ends a parking session.
    - exit_application: Exits the application.
    """

    def __init__(self, master):
        self.master = master
        master.title("NFC Parking System")
        self.lcd = LCD.lcd()
        self.read = SimpleMFRC522()

        self.hour_label = tk.Label(master, text="Enter Parking Hours:")
        self.hour_label.pack()

        self.hour_entry = tk.Entry(master)
        self.hour_entry.pack()

        self.license_plate_label = tk.Label(master, text="Enter License Plate:")
        self.license_plate_label.pack()

        self.license_plate_entry = tk.Entry(master)
        self.license_plate_entry.pack()

        self.start_session_button = tk.Button(master, text="Start Parking Session",
                                              command=self.start_parking_session_threaded)
        self.start_session_button.pack()

        self.status_text = tk.Text(master, height=10, width=50)
        self.status_text.pack()

        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application)
        self.exit_button.pack(side="bottom")
        self.lcd.lcd_clear()

    def display_message(self, message):
        self.status_text.insert(tk.END, message + '\n')

    def start_parking_session_threaded(self):
        self.running = True
        threading.Thread(target=self.start_parking_session).start()

    def start_parking_session(self):
        hours_parked = self.hour_entry.get()
        license_plate = self.license_plate_entry.get()

        try:
            hours_parked = float(hours_parked)
            if hours_parked <= 0:
                self.lcd.lcd_display_string("Parking hours ", 1, 0)
                self.lcd.lcd_display_string("must be > than 0 ", 2, 0)
                self.lcd.lcd_clear()
                raise ValueError("Parking hours must be greater than 0.")
        except ValueError as e:
            self.lcd.lcd_display_string("Invalid parking ", 1, 0)
            self.lcd.lcd_display_string(f"hours: {str(e)}", 2, 0)
            self.display_message(f"Invalid parking hours: {str(e)}")
            return

        try:
            self.display_message("Ready to scan card...")
            self.lcd.lcd_display_string("Ready to scan ", 1, 0)
            self.lcd.lcd_display_string("card...", 2, 0)
            user_id, _ = self.read.read()
            self.display_message(f"Card scanned with ID: {user_id}")
            self.lcd.lcd_display_string("Card scanned ", 1, 0)
            self.lcd.lcd_display_string(f"{user_id}", 2, 0)
        except Exception as e:
            self.display_message(f"Error scanning card: {str(e)}")
            self.lcd.lcd_display_string("Error scanning card", 1, 0)
            return

        if hours_parked <= 2:
            charge = Decimal('0.50') * Decimal(hours_parked)
        else:
            charge = (Decimal('1.00') * (Decimal(hours_parked) - Decimal('2'))) + Decimal('1.00')

        end_time = datetime.now() + timedelta(hours=hours_parked)

        db = get_db_connection()
        cursor = db.cursor()

        try:
            cursor.execute("UPDATE students SET balance = balance - %s WHERE user_id = %s", (charge, user_id))

            cursor.execute("""
                INSERT INTO parking_sessions (user_id, rate, license_plate, charged, end_time) 
                VALUES (%s, %s, %s, %s, %s)
            """, (user_id, 0.50, license_plate, charge, end_time))

            db.commit()
            self.display_message(
                f"Parking started for {hours_parked} hour(s). Charge: €{charge}. End time: {end_time}. Balance updated.")
        except mysql.connector.Error as err:
            self.display_message(f"User does not exist")
            db.rollback()
        finally:
            cursor.close()
            db.close()

    def end_parking_session_threaded(self):
        threading.Thread(target=self.end_parking_session).start()

    def end_parking_session(self):
        self.display_message("Ending parking session...")
        self.lcd.lcd_display_string("Ending parking ", 1, 0)
        self.lcd.lcd_display_string("session...", 1, 0)

    def exit_application(self):
        self.lcd.lcd_clear()
        GPIO.cleanup()
        self.master.quit()
        self.master.destroy
        sys.exit(0)


if __name__ == "__main__":
    root = tk.Tk()
    app = ParkingSystem(root)
    root.mainloop()

