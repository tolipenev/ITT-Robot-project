#!/usr/bin/python

import RPi.GPIO as GPIO
import time

#global vars

GPIO.setmode(GPIO.BCM)

Sensor1 = 24
Sensor2 = 22
Sensor3 = 27
# Sensor1Vcc = 16
Sensor2Vcc = 23
# Sensor3Vcc = 25

GPIO.setup( Sensor1, GPIO.IN )
GPIO.setup( Sensor2, GPIO.IN )
GPIO.setup( Sensor3, GPIO.IN )
# GPIO.setup( Sensor1Vcc, GPIO.OUT )
GPIO.setup( Sensor2Vcc, GPIO.OUT )
# GPIO.setup( Sensor3Vcc, GPIO.OUT )

waitTime = 0.5 #change waittime here

def turnOnSensors():
    
   # GPIO.output( Sensor1Vcc, GPIO.HIGH )
    GPIO.output( Sensor2Vcc, GPIO.HIGH )
   # GPIO.output( Sensor3Vcc, GPIO.HIGH )
   # GPIO.setup( Sensor1, GPIO.HIGH )
   # GPIO.setup( Sensor2, GPIO.HIGH )        
   # GPIO.setup( Sensor3, GPIO.HIGH )
    
def cleanupGpio():
    ''' code to ensure that the IO ports are in a good state after
        the program is run
    '''
    GPIO.cleanup()

def printPinValueLoop( Sensor1, Sensor2, Sensor3, waitTime ):
    ''' loops forever and shows current value of the input pin
    '''
    # count is a counter to make output look nice
    count = 0

    # loop forever
    while (True):
        val1 = GPIO.input( Sensor1 )
        val2 = GPIO.input( Sensor2 )
        val3 = GPIO.input( Sensor3 )        
        print ("%3d Values from left to right: %d, %d, %d"%(count, val1, val2, val3 ))
        time.sleep( waitTime )
        count = count +1
    
def readPin( Sensor1, Sensor2, Sensor3, waitTime ):
    ''' Reads the specified pin a given intervals and outputs
        the result on the terminal
        pinNo: the BCM numbered pin to use
        waitTime: the time in seconds between toggling
        '''

    # to catch ctrl+c in a nice way
    try:
        printPinValueLoop( Sensor1, Sensor2, Sensor3, waitTime )
    except KeyboardInterrupt:
        print ("Done")

    cleanupGpio()


# run if this is the "main" program (as opposed to included as module)
if __name__ == "__main__":
        turnOnSensors()
        readPin( Sensor1, Sensor2, Sensor3, waitTime )
