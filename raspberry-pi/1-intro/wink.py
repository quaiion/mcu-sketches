import RPi.GPIO as GPIO
import time

out_pin = 23

GPIO.setmode (GPIO.BCM)
GPIO.setup (out_pin, GPIO.OUT)

while True:
    GPIO.output (out_pin, 1)
    time.sleep (1)
    GPIO.output (out_pin, 0)
    time.sleep (1)
