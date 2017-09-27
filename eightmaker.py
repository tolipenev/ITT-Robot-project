#!/usr/bin/python
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

Motor1PWM = 15
Motor1A = 17
Motor1B = 18
Motor2PWM = 2
Motor2A = 4
Motor2B = 3

GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1PWM,GPIO.OUT)
GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2PWM,GPIO.OUT)

def rpiCleanup():
	GPIO.cleanup()
try:
    while (True):
        print "Stumbling forwards"
	GPIO.setup(Motor1PWM,GPIO.HIGH)
	GPIO.setup(Motor1A,GPIO.HIGH)
	GPIO.setup(Motor1B,GPIO.LOW)
	GPIO.setup(Motor2PWM,GPIO.HIGH)
	GPIO.setup(Motor2A,GPIO.HIGH)
	GPIO.setup(Motor2B,GPIO.LOW)

	time.sleep(1)

	print "Drunkenly falling to the right"
    	GPIO.setup(Motor1PWM,GPIO.HIGH)
    	GPIO.setup(Motor1A,GPIO.HIGH)
    	GPIO.setup(Motor1B,GPIO.LOW)
    	GPIO.setup(Motor2PWM,GPIO.HIGH)
    	GPIO.setup(Motor2A,GPIO.LOW)
    	GPIO.setup(Motor2B,GPIO.LOW)

    	time.sleep(1.2)

    	print "Stumbling forward again"
    	GPIO.setup(Motor1PWM,GPIO.HIGH)
    	GPIO.setup(Motor1A,GPIO.HIGH)
    	GPIO.setup(Motor1B,GPIO.LOW)
    	GPIO.setup(Motor2PWM,GPIO.HIGH)
    	GPIO.setup(Motor2A,GPIO.HIGH)
    	GPIO.setup(Motor2B,GPIO.LOW)

    	time.sleep(1)

    	print "Being shoved to the left"
    	GPIO.setup(Motor1PWM,GPIO.HIGH)
    	GPIO.setup(Motor1A,GPIO.LOW)
    	GPIO.setup(Motor1B,GPIO.LOW)
    	GPIO.setup(Motor2PWM,GPIO.HIGH)
    	GPIO.setup(Motor2A,GPIO.HIGH)
    	GPIO.setup(Motor2B,GPIO.LOW)

    	time.sleep(1.2)

except KeyboardInterrupt:
	print "cleanup"
	rpiCleanup()
