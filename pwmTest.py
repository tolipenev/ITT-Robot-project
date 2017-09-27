#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import argparse

GPIO.setmode(GPIO.BCM)

Motor1PWM = 15
Motor1A = 17
Motor1B = 18
Motor2PWM = 2
Motor2A = 4
Motor2B = 3

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1PWM, GPIO.OUT)
GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2PWM, GPIO.OUT)

def setupTest(params):

	lconf = GPIO.PWM(15, params.lm_freq)
	rconf = GPIO.PWM(2,params.rm_freq)
	runTest(params, lconf, rconf)

def handleCmdArgs():
	parser = argparse.ArgumentParser()
	parser.add_argument("lm_freq", type=int)
	parser.add_argument("lm_speed", type=int)
	parser.add_argument("rm_freq", type=int)
	parser.add_argument("rm_speed", type=int)

	args = parser.parse_args()
	return args

def rpiCleanup():
	GPIO.cleanup()

def runTest(params, lconf, rconf):
	try:
		while(True):
			GPIO.setup(Motor1A,GPIO.HIGH)
			GPIO.setup(Motor1B,GPIO.LOW)
			GPIO.setup(Motor2A,GPIO.HIGH)
			GPIO.setup(Motor2B,GPIO.LOW)
			lconf.start(params.lm_speed)
			rconf.start(params.rm_speed)

	except KeyboardInterrupt:

		print "cleanup"
		rpiCleanup()

if __name__ == "__main__":
	config = handleCmdArgs()
	setupTest(config)
