import threading
import tkinter as tk
import webbrowser
import time
import socket

from flask import Flask, jsonify
import mysql.connector
from datetime import datetime, timedelta
import RPi.GPIO as GPIO

from check_attendance import check_attendance
from save_user import save_user
from unlock import unlock_door

app = Flask(__name__)


def cleanup_gpio():
    GPIO.cleanup()


app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="nfcsysadmin",
        passwd="",
        database="nfcstudentsys"
    )


@app.route('/attendance/last_1_hours')
def get_recent_attendance():
    one_hours_ago = datetime.now() - timedelta(hours=1)
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM attendance WHERE clock_in >= %s"
    cursor.execute(query, (one_hours_ago,))
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(records)


def start_flask_app():
    app.run(host='0.0.0.0', port=2000, debug=True, use_reloader=False)


def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


class NFCSYS:
    def __init__(self, master):
        self.master = master
        master.title("NFC Student System")

        self.label = tk.Label(master, text="NFC Student System")
        self.label.pack()

        self.start_api_button = tk.Button(master, text="Start API Server and Open Browser",
                                          command=self.start_api_and_open_browser)
        self.start_api_button.pack()

        self.department_label = tk.Label(master, text="Select Department:")
        self.department_label.pack()

        self.department_var = tk.StringVar(master)
        self.department_var.set("IT")  # Default department
        self.department_dropdown = tk.OptionMenu(master, self.department_var, "IT", "Beauty", "OP", "Sci",
                                                 "Culinary", "Eng", "Staff")
        self.department_dropdown.pack()

        self.name_frame = tk.Frame(master)
        self.name_label = tk.Label(self.name_frame, text="Enter Name:")
        self.name_label.pack(side="left")
        self.name_entry = tk.Entry(self.name_frame)
        self.name_entry.pack(side="left")
        self.name_frame.pack()

        self.button = tk.Button(master, text="Unlock Door", command=self.unlock_door_threaded)
        self.button.pack()
        self.register_button = tk.Button(master, text="Register User", command=self.register_user)
        self.register_button.pack()
        self.button_check_attendance = tk.Button(master, text="Attendance", command=self.check_attendance_threaded)
        self.button_check_attendance.pack()

        self.text = tk.Text(master, height=10, width=50)
        self.text.pack()

    def start_api_and_open_browser(self):
        self.display_message("API server starting on http://0.0.0.0:2000")
        threading.Thread(target=self.open_browser).start()

    def open_browser(self):
        ip_address = get_ip_address()
        url = f'http://{ip_address}:2000/attendance/last_1_hours'
        time.sleep(5)
        webbrowser.open(url)

    def display_message(self, message):
        self.text.insert(tk.END, message + '\n')

    def unlock_door_threaded(self):
        threading.Thread(target=self._unlock_door).start()

    def _unlock_door(self):
        department = self.department_var.get()  # Assuming department selection is already handled
        output_callback = self.display_message
        unlock_door(department, output_callback)

    def register_user_threaded(self):
        threading.Thread(target=self.register_user).start()

    def register_user(self):
        department = self.department_var.get()
        name = self.name_entry.get()  # Retrieve the entered name
        output_callback = self.display_message
        save_user(department, name, output_callback)

    def check_attendance_threaded(self):
        threading.Thread(target=self._check_attendance).start()

    def _check_attendance(self):
        output_callback = self.display_message
        check_attendance(output_callback)


if __name__ == "__main__":
    # Start Flask in the main thread
    threading.Thread(target=start_flask_app).start()

    # Initialize and run the Tkinter GUI in the main thread
    root = tk.Tk()
    gui = NFCSYS(root)
    root.protocol("WM_DELETE_WINDOW", cleanup_gpio)
    root.mainloop()
    