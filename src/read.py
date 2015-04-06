#! /usr/bin/env python 
#-*-coding:utf-8-*-

import MFRC522
import subprocess
from time import sleep, strftime
import CharLCD
import urllib
import urllib2
import RPi.GPIO as GPIO
from threading import Thread
from datetime import datetime
import sqlite3

def DisplayTextOnLCD(lcd, text1, text2):
  lcd.clear()
  sleep(0.01)
  lcd.message(text1 + "\n" + text2)

def PostData(Time, UID):
  url = "http://{Domain URL}/signin.ashx"
  url = url + "?uid="+ UID
  url = url + "&Time="+ urllib.quote_plus(Time)  
  print url
  
  try:
    urllib2.urlopen(url).read()
    return True
  except Exception:  
    return False

def QueueFunc():
  while not closeApp:
    conn = sqlite3.connect('/home/pi/crm/CRM.sqlite')
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM USER")
    rows = int(c.fetchone()[0])
    if rows > 0:
      c.execute("SELECT * FROM USER ORDER BY ID ASC Limit 1")
      data = c.fetchone()
      if PostData(str(data[1]), str(data[2])) == True:
        id = str(data[0])
        print "Delete Key ID=" + id
        c.execute("DELETE FROM USER WHERE ID='" + id + "'")
        conn.commit()
    conn.close()
    sleep(1)

closeApp = False
try:
  #subprocess.call(["sudo", "/home/pi/spincl/spincl", "-ib"])
  continue_reading = True
  readdata = ""
  
  ######## This is MFRC522 Init #########
  MIFAREReader = MFRC522.MFRC522()
  #######################################

  ######## This is LCD1602 Init #########
  lcd = CharLCD.CharLCD()
  lcd.begin(16, 1)
  time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
  DisplayTextOnLCD(lcd, "Card Reader:", time)
  #######################################

  ######## This is Buzzer Init..... ######
  pin = 18
  #GPIO.setmode(GPIO.BOARD)
  GPIO.setup(pin, GPIO.OUT)
  p = GPIO.PWM(pin, 1024)  # channel=12 frequency=50Hz
  ########################################

  t = Thread(target=QueueFunc)
  t.start()

  while continue_reading:
    (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    #print "MFRC522_Request"
    #print "status:" + str(status)
    #if status == MIFAREReader.MI_ERR and readdata != "":
      #print "MI_ERR data not null"
      #continue_reading = False
      
    #if status == MIFAREReader.MI_OK:
    #  continue_reading = False
   
    (status,backData) = MIFAREReader.MFRC522_Anticoll()
    if status == MIFAREReader.MI_OK:
      DisplayTextOnLCD(lcd, "Card Reader:", "SignIn OK")
      readdata = hex(backData[3])[2:] + hex(backData[2])[2:] + hex(backData[1])[2:] + hex(backData[0])[2:]
      
      uid = str(int(readdata, 16))
      print "UID: " + uid
      DisplayTextOnLCD(lcd, "Card Reader:", "UID: " + uid)   
  
      ########## This run Buzzer ##########
      p.start(0)  # where dc is the duty cycle (0.0 <= dc <= 100.0)
      p.ChangeDutyCycle(99)
      sleep(0.3)
      p.stop()
      #####################################
    
      #t = Thread(target=SignIn, args=(uid,))
      #t.start()
      conn = sqlite3.connect('/home/pi/crm/CRM.sqlite')
      c = conn.cursor()
      time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
      c.execute("INSERT INTO USER (Time, CardID)VALUES (?,?)", (time, uid))
      conn.commit()
      conn.close()

      DisplayTextOnLCD(lcd, "Card Reader:", time)
finally:
  GPIO.cleanup()
  subprocess.call(["sudo", "/home/pi/spincl/spincl", "-ib"])
  print "finally"
  closeApp = True
