import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)

def d2b (val):
    return (int (elem) for elem in bin (val) [2:].zfill(8))

try:
    print ("enter the period")
    per = int (input ())

    while True:
        for num in range (0, 255):
            GPIO.output (dac, list (d2b (num)))
            time.sleep (per / 256)
        for num in range (255, 0, -1):
            GPIO.output (dac, list (d2b (num)))
            time.sleep (per / 64)


finally:
    GPIO.output (dac, 0)
    GPIO.cleanup ()
