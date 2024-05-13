import os, sys
import mysql.connector
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
sys.path.insert(0, '/home/raissa/NFC-Enabled-Student-Card-System/NFC_Enabled_Student_Card_System/dependencies/')
import I2C_LCD_driver as LCD
import threading
import tkinter as tk
from tkinter import messagebox
from decimal import Decimal

db_config = {
    'host': "localhost",
    'user': "nfcsysadmin",
    'passwd': "",
    'database': "nfcstudentsys"
}


def get_db_connection():
    return mysql.connector.connect(**db_config)


def save_or_update_user(user_id, name, department, balance):
    """
    :param user_id: The ID of the user.
    :param name: The name of the user.
    :param department: The department of the user.
    :param balance: The balance of the user.
    :return: None

    This method saves or updates a user in the database. It takes in the user ID, name, department, and balance as parameters. If a user with the given user ID exists in the database, it updates the user's name and department. Otherwise, it inserts a new user with the provided information. The method handles any errors that occur during the database operations and does a rollback if necessary. It then closes the database cursor and connection.
    """
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.execute("SELECT id FROM students WHERE user_id = %s", (user_id,))
        record = cursor.fetchone()
        if record:
            cursor.execute("UPDATE students SET name = %s, department = %s WHERE user_id = %s",
                           (name, department, user_id))
        else:
            cursor.execute("INSERT INTO students (user_id, name, department, balance) VALUES (%s, %s, %s, %s)",
                           (user_id, name, department, balance))
        db.commit()
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))
        db.rollback()
    finally:
        cursor.close()
        db.close()


def read_card_id(lcd, read):
    """
    :param lcd: The LCD object used to display messages.
    :param read: The RFID reader object used to read the card ID.
    :return: The ID of the RFID card that was read.
    """
    lcd.lcd_display_string("Place Card", 1)
    lcd.lcd_display_string("to update balance", 2)
    user_id, text = read.read()
    lcd.lcd_clear()
    return user_id


class NFCSYS:
    """
    The NFCSYS class represents a system for updating student balances using NFC cards.

    Methods:
    - __init__: Initializes the NFCSYS object.
    - setup_gui: Sets up the GUI elements for the application.
    - update_balance_threaded: Starts a new thread for updating the balance.
    - _update_balance: Updates the balance for a given user.
            Only used internally by the update_balance_threaded method.
        - clear_status_text: Clears the status text in the GUI.
        - display_message: Displays a message in the status text area of the GUI.
    """
    def __init__(self, master):
        self.master = master
        self.lcd = LCD.lcd()
        self.read = SimpleMFRC522()
        self.setup_gui()

    def setup_gui(self):
        self.master.title("NFC Student Balance System")

        self.instructions_label = tk.Label(self.master, text="Please scan your card and enter the balance to update.")
        self.instructions_label.pack(pady=10)

        self.balance_label = tk.Label(self.master, text="Enter Amount to Update Balance:")
        self.balance_label.pack(pady=5)

        self.balance_entry = tk.Entry(self.master)
        self.balance_entry.pack()

        self.update_balance_button = tk.Button(self.master, text="Update Balance", command=self.update_balance_threaded)
        self.update_balance_button.pack(pady=15)

        self.status_text = tk.Text(self.master, height=4, width=50)
        self.status_text.pack(pady=10)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_application)
        self.exit_button.pack(side="bottom")

    def update_balance_threaded(self):
        amount = self.balance_entry.get()
        threading.Thread(target=self._update_balance, args=(amount,)).start()

    def _update_balance(self, amount):
        try:
            amount_decimal = Decimal(amount)
            if amount_decimal < 0:
                self.display_message("Invalid amount: Must be greater than 0.")
                self.lcd.lcd_display_string("Invalid amount", 1, 0)
                self.lcd.lcd_display_string("Must be > 0", 2, 0)
                return
        except ValueError:
            self.display_message("Invalid amount entered. Please enter a numeric value.")
            return

        try:
            self.display_message("Ready to scan card...")
            self.lcd.lcd_display_string("Ready to scan ", 1, 0)
            self.lcd.lcd_display_string("card...", 2, 0)
            user_id, _ = self.read.read()
            self.display_message(f"Card scanned with ID: {user_id}")
        except Exception as e:
            self.display_message(f"Error scanning card: {str(e)}")
            return

        if user_id:
            db = get_db_connection()
            cursor = db.cursor()

            try:
                cursor.execute("SELECT balance FROM students WHERE user_id = %s", (user_id,))
                result = cursor.fetchone()
                if result:
                    current_balance = result[0] if result[0] is not None else Decimal('0.00')
                    new_balance = current_balance + amount_decimal
                    cursor.execute("UPDATE students SET balance = %s WHERE user_id = %s", (new_balance, user_id))
                    db.commit()
                    self.lcd.lcd_clear()
                    self.display_message(f"Balance updated successfully. New Balance: €{new_balance}")
                    self.lcd.lcd_display_string(f"New Balance:", 1, 0)
                    self.lcd.lcd_display_string(f"{new_balance}", 2, 0)
                else:
                    self.display_message("User not found. Balance not updated.")
                    self.lcd.lcd_display_string("User not found.", 1, 0)
            except mysql.connector.Error as err:
                self.display_message(f"Database error: {str(err)}")
                db.rollback()
            finally:
                cursor.close()
                db.close()

    def clear_status_text(self):
        self.status_text.delete('1.0', tk.END)

    def display_message(self, message):
        self.status_text.insert(tk.END, message + '\n')

    def exit_application(self):
        """
        Cleans up the GPIO pins, destroys the main window, and exits the application.
        """
        self.lcd.lcd_clear()
        GPIO.cleanup()
        self.master.quit()
        self.master.destroy()
        sys.exit(0)


def cleanup_gpio():
    GPIO.cleanup()


if __name__ == "__main__":
    root = tk.Tk()
    app = NFCSYS(root)
    root.protocol("WM_DELETE_WINDOW", app.exit_application)
    root.mainloop()