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

Sensor1 = 24
Sensor2 = 22
Sensor3 = 27
Sensor2Vcc = 23

Speed = 60
Turn_speed = 10

GPIO.setup(Motor1A, GPIO.OUT)
GPIO.setup(Motor1B, GPIO.OUT)
GPIO.setup(Motor1PWM, GPIO.OUT)

GPIO.setup(Motor2A, GPIO.OUT)
GPIO.setup(Motor2B, GPIO.OUT)
GPIO.setup(Motor2PWM, GPIO.OUT)

#StartButton = 19 # change this 
#GPIO.setup(StartButton, GPIO.IN)
#start = false

GPIO.setup(Sensor1, GPIO.IN)
GPIO.setup(Sensor2, GPIO.IN)
GPIO.setup(Sensor3, GPIO.IN)
GPIO.setup(Sensor2Vcc, GPIO.OUT)

motor1 = GPIO.PWM(15,50) # set motor1 pwm frequency here
motor1.start(Speed) # set motor1 dc here

motor2 = GPIO.PWM(2,50) # set motor2 pwm frequency here
motor2.start(Speed) # set motor2 dc here

waitTime = 0.05 #change waittime here

#-----

def turnOnSensor():
    
    GPIO.output(Sensor2Vcc, GPIO.HIGH)
    print("Initializing...")

#-----

def motors_straight():
    GPIO.setup(Motor1A,GPIO.HIGH)
    GPIO.setup(Motor1B,GPIO.LOW)
    GPIO.setup(Motor2A,GPIO.HIGH)
    GPIO.setup(Motor2B,GPIO.LOW)
    motor1.ChangeDutyCycle(Speed)
    motor2.ChangeDutyCycle(Speed)

def motor1_slow():
    motor1.ChangeDutyCycle(Turn_speed)

def motor2_slow():
    motor2.ChangeDutyCycle(Turn_speed)   

def motor1_reverse():
    GPIO.setup(Motor1A,GPIO.LOW)
    GPIO.setup(Motor1B,GPIO.HIGH)

def motor2_reverse():    
    GPIO.setup(Motor2A,GPIO.LOW)
    GPIO.setup(Motor2B,GPIO.HIGH)

def motors_left():
    motors_straight()
    motor1_slow()  

def motors_right():
    motors_straight()
    motor2_slow()    
  
def motors_zigzag():
    motors_straight()
    motor1_reverse()
    time.sleep(0.15)
    motors_straight()
    motor2_reverse()
    time.sleep(0.15)
    
#-----
    
def cleanupGpio():
    
    GPIO.cleanup()

#-----

#def readStartButton():
 #   press = GPIO.input( StartButton )
 #   if press is GPIO.HIGH: # check the return
#        if start is false:
 #           start = true
 #       else:
#            start = false
        

def SensorLoop(Sensor1, Sensor2, Sensor3, waitTime):


    while (True):
  #      readStartButton()
   #     if start:
            val1 = GPIO.input(Sensor1)
            val2 = GPIO.input(Sensor2)
            val3 = GPIO.input(Sensor3)
            vals = [val1, val2, val3]
            print ("| %d | %d | %d |"%(val1, val2, val3))

            # white = 0, black = 1

            if(vals[0] == 1 and vals[2] == 0): # going left
                motors_left()

            elif(vals[0] == 0 and vals[2] == 1): # going right
                motors_right()

            elif (vals[1] == 1): # going straight
                motors_straight()
                
            else:
                motors_zigzag() # off the path
                  
            time.sleep(waitTime)

#-----
        
def readPin(Sensor1, Sensor2, Sensor3, waitTime):

    try:
        SensorLoop( Sensor1, Sensor2, Sensor3, waitTime )
    except KeyboardInterrupt:
        print ("Done!")

    cleanupGpio()

#-----

if __name__ == "__main__":
        turnOnSensor()
        motors_straight()
        readPin(Sensor1, Sensor2, Sensor3, waitTime)
