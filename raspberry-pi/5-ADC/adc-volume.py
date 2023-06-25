import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [21, 20, 16, 12, 7, 8, 25, 24]
nbits = len (dac)
levels = 2**nbits
maxVoltage = 3.3
comp = 4
troyka = 17

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)
GPIO.setup (leds, GPIO.OUT)
GPIO.setup (troyka, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup (comp, GPIO.IN)

def d2b (val):
    return [int (elem) for elem in bin (val) [2:].zfill(8)]

def adc ():
    val = 0
    for bit in range (7, -1, -1):
        val = val + 2**bit
        signal = d2b (val)
        GPIO.output (dac, signal)
        time.sleep (0.007)
        compVal = GPIO.input (comp)
        if compVal == 0:
            val = val - 2**bit
    return val

def fill (val):
	bit = (val + 8) // 32
	bitval = d2b (0)
	ctr = 0
	while ctr < bit:
		bitval[7 - ctr] = 1
		ctr += 1
	return bitval

try:
	while True:
		value = adc ()
		voltage = value / levels * maxVoltage
		print ("ADC val = {:^3}, input voltage = {:.2f}".format(value, voltage))
		bitval = fill (value)
		GPIO.output (leds, bitval)

except KeyboardInterrupt:
	print ('\nProg was stopped by the kybd')

finally:
	GPIO.output (dac, GPIO.LOW)
	GPIO.output (leds, 0)
	GPIO.cleanup(dac)
	GPIO.cleanup (leds)
