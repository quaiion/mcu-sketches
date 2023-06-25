import RPi.GPIO as GPIO

out_pin = 23
in_pin = 24

GPIO.setmode (GPIO.BCM)
GPIO.setup (out_pin, GPIO.OUT)
GPIO.setup (in_pin, GPIO.IN)

while True:
    GPIO.output (out_pin, GPIO.input (in_pin)) 