import RPi.GPIO as GPIO
from config import *
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(BURN_PIN, GPIO.OUT)
GPIO.output(BURN_PIN, GPIO.LOW)
raw_input('Press enter to burn')
GPIO.output(BURN_PIN, GPIO.HIGH)
time.sleep(5)
GPIO.output(BURN_PIN, GPIO.LOW)
GPIO.cleanup()
