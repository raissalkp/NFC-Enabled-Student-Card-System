import tkinter as tk
from tkinter import messagebox, ttk
import unlock
import save_user
import threading
import RPi.GPIO as GPIO


class DoorLockGUI:
    def __init__(self, master):
        self.master = master
        master.title("NFC Student System")

        self.label = tk.Label(master, text="NFC Student System")
        self.label.pack()

        self.department_label = tk.Label(master, text="Select Department:")
        self.department_label.pack()

        self.department_var = tk.StringVar(master)
        self.department_var.set("IT")
        self.department_dropdown = tk.OptionMenu(master, self.department_var, "IT", "Beauty", "Sci",
                                                 "Culinary", "Eng", "Staff")
        self.department_dropdown.pack()

        self.name_label = tk.Label(master, text="Enter Name:")
        self.name_label.pack()
        self.name_entry = tk.Entry(master)
        self.name_entry.pack()

        self.button = tk.Button(master, text="Unlock Door", command=self.unlock_door_threaded)
        self.button.pack()
        self.register_button = tk.Button(master, text="Register User", command=self.register_user)
        self.register_button.pack()

        self.text = tk.Text(master, height=10, width=50)
        self.text.pack()

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


root = tk.Tk()
gui = DoorLockGUI(root)
root.mainloop()
