NFC Enabled Student Card System
===========================================

Copyright © 2024 Raissa Pululu. All rights reserved.
----------------------------------------------------

### Introduction

This project presents an advanced NFC Based Student Attendance Management System designed to automate attendance 
tracking, access control and a parking system using NFC/RFID technology, interfaced with Python and API integration. 
It's an ideal solution 
for educational institutions or corporate environments looking to streamline their attendance processes through modern, 
contactless identification methods.

### System Overview

The system uses NFC/RFID tags for identifying individuals, logging their attendance, access control, topping up their 
balance and a parking system automatically upon tag detection. The integration with an I2C LCD display provides 
real-time feedback, such as user identification and attendance status.

![img.png](NFC_Enabled_Student_Card_System/assets/img.png)
----------------------------------------------------
Hardware setup for NFC Enabled Student Card System. 

### Running the System

#### Cloning the Repository

Start by cloning the repository to obtain the latest version of the project:

`git clone https://github.com/raissalkp/NFC-Enabled-Student-Card-System`

### Software Dependencies

Install Python libraries or dependencies in a `requirements.txt` file for easy installation using `pip install -r requirements.txt` or `sudo pip3 install -r requirements.txt`.

### Setup System
To set up hardware:
* Connect the GPIO Extension Board to the Raspberry Pi
* Connect Extension Board to breadboard
* For the RFID RC522:
  * connect GND to GND (-)
  * connect SDA to CEO
  * connect SCk to SCLK
  * connect MOSI to MOSI
  * connect MISO to MISO
  * connect GND to GND
  * connect RST to GPIO25
  * connect 3.3v -- 3.3v
* Connect the buzzer to pin 27 + and - and connect + to GPIO19
* For the LCD:
  * connect GND to GND
  * connect VCC TO 5v
  * connect SDA to SDA
  * connect SCL to SCL
* For the relay module
  * connect VCC to 3.3v
  * connect GND to GND
  * connect IN to GPIO26
  * connect COM to a 12VDC input
  * connect NC to the solenoid lock
  * connect the solenoid lock to 12VDC input

To set up software:
* Install Raspberry Pi on an SD card
* Insert SD card into Raspberry Pi
* Connect all the necessary peripherals i.e. mouse, keyboard, monitor, power supply
* Connect to network
* Install pip through command line `sudo apt install python3-dev python3-pip`
* Install spidev `sudo pip3 install spidev`
* Install RC522 library `sudo pip3 install mfrc522`
* Enable I2C and SPI communications through Raspberry Pi configuration

#### Execute System
 
1. **Running the Main Application**: Navigate to the project directory and execute the `main.py` script to initiate the access control, attendance tracking and adding a student to the system:
`python main.py`
2. **Running the Top-Up Application**: Navigate to the project directory and execute the `top_up.py` script to initiate the top up of the balance:`python top_up.py`

3. **Running the Parking System Application**: Navigate to the project directory and execute the `parking_sys.py` script to initiate the parking system:`python parking_sys.py`
4. All applications can also be executed by opening the IDE Thonny, locating the directory and running it through the IDE.

### System Structure

The system comprises several Python scripts, each serving a unique function within the attendance management ecosystem:

*   **`I2C_LCD_driver.py`**: Manages interactions with the I2C LCD display.
*   **`check_attendance.py`**: Handles attendance verification and logging.
*   **`save_user.py`**: Manages user data storage and retrieval.
*   **`top_up.py`**: Manages account top-ups for users.
* **`parking_sys.py`**: Handles payment for parking.
*   **`unlock.py`**: Controls access mechanisms based on user authentication.
* **`main.py`**: Acts as the central script to run the application as well as the API scripts.

### Hardware Requirements

*   NFC/RFID Reader Module
*   NFC/RFID Tags or Cards
*   I2C LCD Display
* Breadboard
* GPIO Breakout Board
* 12VDC Lock-style Solenoid
* Relay Module
* Wall Adapter Power Supply
* USB-C Cable
* Jumper Wires M/M
* Jumper Wires M/F
* RFID Cards/Tags
*   Raspberry Pi (or compatible device)

### Code References
* This project used the `I2C_LCD_driver.py` library designed by Denis Pleic, which can be found [here](https://gist.github.com/vay3t/8b0577acfdb27a78101ed16dd78ecba1) 
* This project has taken inspiration from the following projects [PiMyLifeUp](https://pimylifeup.com/raspberry-pi-rfid-attendance-system/), [SriTu Hobby](https://www.youtube.com/watch?v=p1RfcgJnHR4&t=12s), [davidcdupuis](https://github.com/davidcdupuis/NFCAttendanceLogger/blob/master/NFC.py), 
