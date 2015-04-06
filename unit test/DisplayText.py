import CharLCD
from time import sleep, strftime
import RPi.GPIO as GPIO
import sys

lcd = CharLCD.CharLCD()
lcd.begin(16, 1)
 
lcd.clear()
sleep(0.01)
lcd.message(sys.argv[1] + "\n"+ sys.argv[2])
GPIO.cleanup()
