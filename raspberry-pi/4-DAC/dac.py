import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]

GPIO.setmode (GPIO.BCM)
GPIO.setup (dac, GPIO.OUT)

def d2b (val):
    return (int (elem) for elem in bin (val) [2:].zfill(8))

def is_digit (str):
    if (str.isdigit()):
        return True
    else:
        try:
            float (str)
            return True
        except ValueError:
            return False

try:
    print ("enter the number")
    val = input ()

    if val == "q":
        quit ()

    if is_digit (val) == False:
        print ("no, enter a number")
        quit ()

    if float (val) % 1 != 0:
        print ("no, an integer")
        quit ()

    val = int (val)

    if val > 255:
        print ("no, less then 256")
        quit ()

    if val < 0:
        print ("no, a postive one")
        quit ()

    GPIO.output (dac, list (d2b (val)))
    print (val / 256 * 3.3)
    time.sleep (4)

finally:
    GPIO.output (dac, 0)
    GPIO.cleanup ()
