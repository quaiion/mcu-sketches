import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
GPIO.setup (leds, GPIO.OUT)

counter_1 = 0
while counter_1 < 3:
    for led in leds:
        GPIO.output (led, 1)
        time.sleep (0.2)
        GPIO.output (led, 0)
    counter_1 = counter_1 + 1

GPIO.output (leds, 0)
GPIO.cleanup ()
