# Include the library files
import I2C_LCD_driver
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

#Include the buzzer pin
buzzer = 19

#Include the relay pin
relay = 26

#Enter your tag ID
Tag_ID = "584184844258"

door = True

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(buzzer,GPIO.OUT)
GPIO.setup(relay,GPIO.OUT)

# Create a object for the LCD
lcd = I2C_LCD_driver.lcd()

# Create a object for the RFID module
read = SimpleMFRC522()

#Starting text
lcd.lcd_display_string("Door lock system",1,0)
for a in range (0,15):
    lcd.lcd_display_string(".",2,a)
    sleep(0.1)


while True:
    lcd.lcd_clear()
    lcd.lcd_display_string("Place your Tag",1,1)
    id,Tag = read.read()
    
    id = str(id)
               
    if id == Tag_ID:
        lcd.lcd_clear()
        lcd.lcd_display_string("Successful",1,3)
        
        if door == True:
            lcd.lcd_display_string("Door is locked",2,1)
            GPIO.output(relay,GPIO.HIGH)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW)
            door = False
            sleep(3)
            
            
        elif door == False:
            lcd.lcd_display_string("Door is open",2,2)
            GPIO.output(relay,GPIO.LOW)
            GPIO.output(buzzer,GPIO.HIGH)
            sleep(0.5)
            GPIO.output(buzzer,GPIO.LOW)
            door = True
            sleep(3)
                        
        
    else:
        lcd.lcd_clear()
        lcd.lcd_display_string("Wrong Tag!",1,3)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.LOW)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.HIGH)
        sleep(0.3)
        GPIO.output(buzzer,GPIO.LOW)            

GPIO.cleanup()     
        