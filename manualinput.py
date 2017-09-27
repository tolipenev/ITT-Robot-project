#!/usr/bin/python

import RPi.GPIO as GPIO
import sys, tty, termios, time

#global vars

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

motor1 = GPIO.PWM(15,100) # set motor1 pwm frequency here
motor1.start(0)
motor1.ChangeDutyCycle(0)

motor2 = GPIO.PWM(2,80) # set motor2 pwm frequency here
motor2.start(0)
motor2.ChangeDutyCycle(0)

# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def motor1_forward():
    GPIO.setup(Motor1A,GPIO.HIGH)
    GPIO.setup(Motor1B,GPIO.LOW)

def motor1_reverse():
    GPIO.setup(Motor1A,GPIO.LOW)
    GPIO.setup(Motor1B,GPIO.HIGH)

def motor2_forward():
    GPIO.setup(Motor2A,GPIO.HIGH)
    GPIO.setup(Motor2B,GPIO.LOW)

def motor2_reverse():
    GPIO.setup(Motor2A,GPIO.LOW)
    GPIO.setup(Motor2B,GPIO.HIGH)

def toggleAccel(movement): #sets whether car is going forward,
                            #backward or is stopped.
    global accelStatus

    if(movement == "forward"):
        if(accelStatus == "stop"):
            motor1_forward()
            motor2_forward()
            motor1.ChangeDutyCycle(99)
            motor2.ChangeDutyCycle(99)
            accelStatus = "forward"
        elif(accelStatus == "reverse"):
            motor1.ChangeDutyCycle(0)
            motor2.ChangeDutyCycle(0)
            accelStatus = "stop"

    if(movement == "reverse"):
        if(accelStatus == "stop"):
            motor1_reverse()
            motor2_reverse()
            motor1.ChangeDutyCycle(50)
            motor2.ChangeDutyCycle(50)
            accelStatus = "reverse"
        elif(accelStatus == "forward"):
            motor1.ChangeDutyCycle(0)
            motor2.ChangeDutyCycle(0)
            accelStatus = "stop"

    if(movement == "stop"):
        if(accelStatus == "reverse"):
            motor1.ChangeDutyCycle(0)
            motor2.ChangeDutyCycle(0)
            accelStatus = "stop"
        elif(accelStatus == "forward"):
            motor1.ChangeDutyCycle(0)
            motor2.ChangeDutyCycle(0)
            accelStatus = "stop" 
            
            
def toggleSteering(direction): #sets direction of car

    global wheelStatus

    if(direction == "right"):
        if(wheelStatus == "centre"):
            motor1_forward()
            motor1.ChangeDutyCycle(75)
            motor2.ChangeDutyCycle(0)
            wheelStatus = "right"
        elif(wheelStatus == "left"):
            motor1_forward()
            motor1.ChangeDutyCycle(75)
            motor2.ChangeDutyCycle(0)
            wheelStatus = "right"

    if(direction == "left"):
        if(wheelStatus == "centre"):
            motor2_forward()
            motor2.ChangeDutyCycle(75)
            motor1.ChangeDutyCycle(0)
            wheelStatus = "left"
        elif(wheelStatus == "right"):
            motor2_forward()
            motor2.ChangeDutyCycle(75)
            motor1.ChangeDutyCycle(0)
            wheelStatus = "left"

    if(direction == "centre"):
        if(wheelStatus == "left"):
            motor1.ChangeDutyCycle(0)
            motor2.ChangeDutyCycle(0)
            wheelStatus = "centre"
        elif(wheelStatus == "right"):
            motor1.ChangeDutyCycle(0)
            motor2.ChangeDutyCycle(0)
            wheelStatus = "centre"           

# Setting the PWM pins to false so the motors will not move
# until the user presses the first key
GPIO.setup(Motor1A,GPIO.LOW)
GPIO.setup(Motor1B,GPIO.LOW)
GPIO.setup(Motor2A,GPIO.LOW)
GPIO.setup(Motor2B,GPIO.LOW)

# Global variables for the status of the acceleration and steering
wheelStatus = "centre"
accelStatus = "stop"

# Instructions for when the user has an interface
print("W/S: acceleration")
print("A/D: steering")
print("X: exit")

# Infinite loop that will not end until the user presses the
# exit key
while (True):
    # Keyboard character retrieval method is called and saved
    # into variable
    char = getch()

    # The car will drive forward when the "w" key is pressed
    if(char == "w"):
        toggleSteering("centre")
        toggleAccel("forward")

    # The car will reverse when the "s" key is pressed
    if(char == "s"):
        toggleSteering("centre")       
        toggleAccel("reverse")
        
    # The "a" key will toggle the steering left
    if(char == "a"):
        toggleAccel("stop")
        toggleSteering("left")

    # The "d" key will toggle the steering right
    if(char == "d"):
        toggleAccel("stop")
        toggleSteering("right")

    # The "x" key will break the loop and exit the program
    if(char == "x"):
        print("Program Ended. Commencing GPIO cleanup")
        break
  

    # The keyboard character variable will be set to blank, ready
    # to save the next key that is pressed
    char = ""

# Program will cease all GPIO activity before terminating
GPIO.cleanup()
