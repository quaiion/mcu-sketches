import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
nbits = len (dac)
levels = 2**nbits
maxVoltage = 3.3
comp = 4
troyka = 17

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)

def d2b (val):
    return [int (elem) for elem in bin (val) [2:].zfill(8)]

def adc ():
	for value in range (256):
		signal = d2b (value)
		GPIO.output (dac, signal)
		time.sleep (0.001)
		compVal = GPIO.input (comp)
		if compVal == 0:
			return value
	return 256

try:
	while True:
		value = adc ()
		voltage = value / levels * maxVoltage
		print ("ADC val = {:^3}, input voltage = {:.2f}".format(value, voltage))

except KeyboardInterrupt:
	print ('\nProg was stopped by the kybd')

finally:
	GPIO.output (dac, GPIO.LOW)
	GPIO.cleanup (dac)
