#referance 
#https://code.google.com/p/raspberry-gpio-python/wiki/PWM

import time
import RPi.GPIO as GPIO
import urllib2
import requests

def LoginSCE(username, password):
  loginUrl = "https://ckwca.sce.pccu.edu.tw/login.php"
  checkUrl = "https://ckwca.sce.pccu.edu.tw/loginCheck.php"
  data = {"user" : username, "password": password, "authserver" : "38"}

  s = requests.session()
  s.get(loginUrl)
  r = s.post(checkUrl, data)
  print r

    
pin = 12
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)

p = GPIO.PWM(pin, 1024)  # channel=12 frequency=50Hz
p.start(0)  # where dc is the duty cycle (0.0 <= dc <= 100.0)

try:
  for dc in range(100, 70, -5):
    p.start(0)
    p.ChangeDutyCycle(dc)
    time.sleep(0.1)
    p.stop()
    
  for dc in range(100, 70, -5):
    p.start(0) 
    p.ChangeDutyCycle(dc)
    time.sleep(0.1)
    p.stop()    
    
except KeyboardInterrupt:
    pass
p.stop()
GPIO.cleanup()
