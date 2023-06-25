import RPi.GPIO as GPIO

GPIO.setmode (GPIO.BCM)

leds = [21, 20, 16, 12, 7, 8, 25, 24]
GPIO.setup (leds, GPIO.OUT)

GPIO.output (leds, 0)
GPIO.cleanup ()
