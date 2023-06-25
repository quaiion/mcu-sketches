import time
import matplotlib.pyplot as plt
import numpy as np
import RPi.GPIO as GPIO

comp = 4
troyka = 17
leds = [21, 20, 16, 12, 7, 8, 25, 24]
dac = [26, 19, 13, 6, 5, 11, 9, 10]

def from_binary (bits):
    number = 0
    for bit in bits:
        number *= 2
        number += bit
    return number

def adc ():
    size_in_bits = 8
    current_bits = [0] * size_in_bits
    for i in range(size_in_bits):
        current_bits[i] = 1
        GPIO.output(dac, current_bits)
	
        time.sleep(0.05)
        
        if GPIO.input(comp) == GPIO.LOW:
            current_bits[i] = 0
	    
    return from_binary(current_bits)

def makplot (volt, filename=None):
    fig = plt.figure (figsize=(15, 18))
    plt.plot (volt)
    if filename is not None:
        plt.savefig (filename)

    plt.show()

def savdat (voltages, time, period, step, discr):
    with open ("data.txt", "w") as file:
        str_volts = list(map(lambda x: str(x), voltages))
        file.write ("\n".join(str_volts))
    
    with open("settings.txt", "w") as file:
        file.write(f"whole measurement duration: {time}\n")
        file.write(f"single measurement duration: {period}\n")
        file.write(f"step duration: {step}\n")
        file.write(f"discretization rate: {discr}")

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(leds, GPIO.OUT)
    GPIO.setup(dac, GPIO.OUT)
    GPIO.setup(troyka, GPIO.OUT, initial = GPIO.HIGH)
    GPIO.setup(comp, GPIO.IN)

    voltage_values = list()

    try:
        time_start = time.time()
        GPIO.output(troyka, GPIO.HIGH)

        voltage = 0

        while voltage / 3.3 <= 0.92:
            bitnum = adc ()
            voltage = bitnum * 3.3 / 256
            print (voltage)

            voltage_values.append (voltage)

        print ("goin down...")
        GPIO.output(troyka, GPIO.LOW)

        while voltage / 3.3 >= 0.07:
            bitnum = adc()
            voltage = bitnum * 3.3 / 256
            print (voltage)

            voltage_values.append (voltage)

        time_end = time.time()
        experiment_time = time_end - time_start
        savdat (voltage_values, experiment_time, experiment_time / 2, experiment_time / len(voltage_values), 3.3 / 256)
        makplot(voltage_values, "plot-voltages.png")

    except KeyboardInterrupt:
        print("prog was stopped by the kybd")        
            
    finally:
        GPIO.output(dac, 0)
        GPIO.cleanup()
        