import threading
import tkinter as tk

import RPi.GPIO as GPIO

import check_attendance
import save_user
import unlock
import requests


def cleanup_gpio():
    GPIO.cleanup()


BASE_URL = "http://192.168.1.10:5000"


class NFCSYS:
    def __init__(self, master):
        self.master = master
        master.title("NFC Student System")

        self.label = tk.Label(master, text="NFC Student System")
        self.label.pack()

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

    def get_recent_attendance(self):
        endpoint = "/attendance/last_2_hours"
        url = BASE_URL + endpoint

        try:
            # Make the API call
            response = requests.get(url)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                # Get the JSON response
                records = response.json()

                # Display the attendance records or process them as needed
                # For example, you could update a text box with the attendance data
                print(records)
            else:
                # Print an error message if the request was unsuccessful
                print("Error:", response.status_code)
        except requests.RequestException as e:
            # Handle connection errors or other exceptions
            print("Error:", e)

    def display_message(self, message):
        self.text.insert(tk.END, message + '\n')

    def unlock_door_threaded(self):
        department = self.department_var.get()
        threading.Thread(target=self._unlock_door, args=(department,)).start()

    def _unlock_door(self, department):
        output_callback = self.display_message
        unlock.unlock_door(department, output_callback)
        GPIO.cleanup()

    def register_user(self):
        department = self.department_var.get()
        name = self.name_entry.get()  # Retrieve the entered name
        threading.Thread(target=self._register_user, args=(department, name)).start()

    def _register_user(self, department, name):
        output_callback = self.display_message
        save_user.save_user(department, name, output_callback)
        GPIO.cleanup()

    def check_attendance_threaded(self):
        threading.Thread(target=self._check_attendance).start()

    def _check_attendance(self):
        output_callback = self.display_message
        check_attendance.check_attendance(output_callback)
        GPIO.cleanup()


root = tk.Tk()
gui = NFCSYS(root)
root.protocol("WM_DELETE_WINDOW", cleanup_gpio)
root.mainloop()