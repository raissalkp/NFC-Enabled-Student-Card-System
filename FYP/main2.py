import tkinter as tk
from tkinter import messagebox, ttk
import unlock
import threading
import RPi.GPIO as GPIO


class DoorLockGUI:
    def __init__(self, master):
        self.master = master
        master.title("Door Lock System")

        self.label = tk.Label(master, text="Door lock system")
        self.label.pack()

        self.department_label = tk.Label(master, text="Select Department:")
        self.department_label.pack()

        self.department_var = tk.StringVar(master)
        self.department_var.set("IT")  # Default department
        self.department_dropdown = ttk.Combobox(master, textvariable=self.department_var)
        self.department_dropdown['values'] = (
            "IT", "Beauty", "Sci", "Culinary", "Eng", "Staff")  # Add more departments as needed
        self.department_dropdown.pack()

        self.button = tk.Button(master, text="Unlock Door", command=self.unlock_door_threaded)
        self.button.pack()

        self.text = tk.Text(master, height=10, width=50)
        self.text.pack()

    def display_message(self, message):
        self.text.insert(tk.END, message + '\n')

    def get_user_input(self):
        return messagebox.askquestion("Continue?", "Continue? (y/n)")

    def unlock_door_threaded(self):
        department = self.department_var.get()
        threading.Thread(target=self._unlock_door, args=(department,)).start()

    def _unlock_door(self, department):
        output_callback = self.display_message  # Assuming display_message is a method in your GUI class
        unlock.unlock_door(department, output_callback)  # Call the unlock_door function with output_callback
        GPIO.cleanup()


root = tk.Tk()
gui = DoorLockGUI(root)
root.mainloop()
