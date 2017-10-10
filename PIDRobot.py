#!/usr/bin/python
import RPi.GPIO as GPIO
import time
#import ptvsd

#ptvsd.enable_attach('visual')

GPIO.setmode(GPIO.BCM)


lmControl1 = 18         #Left Motor Control 1
lmControl2 = 17         #Left Motor Control 2
lmEnable = 15           #Left Motor Enable
rmControl1 = 3          #Right Motor Control 1
rmControl2 = 4          #Right Motor Control 2
rmEnable = 2            #Right Motor Enable
lsOut = 24              #Left Sensor Output
sensVCC = 23            #VCC output for Sensor
csOut = 22              #Center Sensor Output
rsOut = 27              #Right Sensor Output
pin_startbutton = 5

GPIO.setup(lmControl1, GPIO.OUT)        #Setting the GPIO Ports up on the rPi
GPIO.setup(lmControl2, GPIO.OUT)
GPIO.setup(lmEnable, GPIO.OUT)
GPIO.setup(rmControl1, GPIO.OUT)
GPIO.setup(rmControl2, GPIO.OUT)
GPIO.setup(rmEnable, GPIO.OUT)
GPIO.setup(lsOut, GPIO.IN)
GPIO.setup(sensVCC, GPIO.OUT)
GPIO.setup(csOut, GPIO.IN)
GPIO.setup(rsOut, GPIO.IN)

GPIO.setup(lmControl1, GPIO.LOW)
GPIO.setup(lmControl2, GPIO.HIGH)
GPIO.setup(rmControl1, GPIO.LOW)
GPIO.setup(rmControl2, GPIO.HIGH)
GPIO.output(sensVCC, GPIO.HIGH)
LM = GPIO.PWM(lmEnable, 50)             #Setting Left Motor to PWM Output with 50 Hz
RM = GPIO.PWM(rmEnable, 50)             #Setting Right Motor to PWM Output with 50 Hz
GPIO.setup(pin_startbutton, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def waitforbuttonpress(pin_number):
    while True:
        press = GPIO.input(pin_number)
        if press == True:
            return
        else:
            time.sleep (0.05)

def getError():
    #create a list that gathers the sensor outputs and stores them as strings

    sensor = [GPIO.input(lsOut), GPIO.input(csOut), GPIO.input(rsOut)]
    error = str(sensor[0]) + str(sensor[1]) + str(sensor[2])
    
    if(error == '000'):
        error = 0
    elif(error == '001'):
        error = 15
    elif(error == '010'):
        error = 0
    elif(error == '011'):
        error = 1
    elif(error == '100'):
        error = -15
    elif(error == '101'):
        error = 0
    elif(error == '110'):
        error = -1
    elif(error == '111'):
        error = 0   

    return error

def run(dcL, dcR):
    #the def that gets the enginge running by setting the dutycycle of the Left and Right Motors. 
    #If the reieved value exceeds 100 or -100 the dutycycle is set to 100 
    try:        
        dcL = int(dcL)
        dcR = int(dcR)
        
        if(dcL > 0):
            if(dcL > 100):
                GPIO.setup(lmControl1, GPIO.HIGH)
                GPIO.setup(lmControl2, GPIO.LOW)
                LM.start(100)
            else:
                GPIO.setup(lmControl1, GPIO.HIGH)
                GPIO.setup(lmControl2, GPIO.LOW)
                LM.start(dcL)
        else:
            if(dcL < -100):
                GPIO.setup(lmControl1, GPIO.LOW)
                GPIO.setup(lmControl2, GPIO.HIGH)
                LM.start(100)
            else:
                GPIO.setup(lmControl1, GPIO.LOW)
                GPIO.setup(lmControl2, GPIO.HIGH)
                LM.start(dcL * (-1))

        if(dcR > 0):
            if(dcR > 100):
                GPIO.setup(rmControl1, GPIO.HIGH)
                GPIO.setup(rmControl2, GPIO.LOW)
                RM.start(100)
            else:
                GPIO.setup(rmControl1, GPIO.HIGH)
                GPIO.setup(rmControl2, GPIO.LOW)
                RM.start(dcR)
        else:
            if(dcR < -100):
                GPIO.setup(rmControl1, GPIO.LOW)
                GPIO.setup(rmControl2, GPIO.HIGH)
                RM.start(100)
            else:
                GPIO.setup(rmControl1, GPIO.LOW)
                GPIO.setup(rmControl2, GPIO.HIGH)
                RM.start(dcR *(-1))
        
    except KeyboardInterrupt:
        GPIO.cleanup()

def stop():
    LM.stop()
    RM.stop()
        
#Kp = gain where robot oscilation is consistent. start with setting this value until robot oscillates 
#Ki and Kd is calculated based on the Ziegler Method which says: 
#Kp = 0.6*Kc where Kc==Kp, the critical gain, being when the robot oscillates consistently and follows the line. 
#Ki = 2*Kp*dT/Pc, dT is the time in seconds it takes to loop the code and Pc is the oscillation time the robot oscillates from left to right and back.
#Kd = Kp*Kc/(8*dT), and thats the calculations for the 3 K constants using the Ziegler method 
Kp = 75             
Ki = 0.27            
Kd = 10982.8
dT = 0.000435           #dT is the loop time for the code to execute
offset = -0.476         #the offset determines in this case where the robot is aligning itself. in this case the PID tries to have an error at -0.475 which is making the robot be slightly to the right of the line because our left engigne is slower then the right 
Tp = 1000               #Target Power is the duty cycle we aim for both engigne to have when the error is 0. when the robot is on the line
integral = 0
integral_max = 20
integral_min = -20
lastError = 0
derivative = 0

stop ()
run(0,0)
print "press Button to start"
waitforbuttonpress(pin_startbutton)

try:
    print "starting code"
    #the PID code calculations
    while(True):
        error = getError()
        
        error = error - offset

        integral = integral + error * dT

        if(integral > integral_max):
            integral = integral_max
        elif(integral < integral_min):
            integral = integral_min

        derivative = (error - lastError)/dT

        Turn = Kp*error + Ki*integral + Kd*derivative

        run(Tp + Turn, Tp - Turn)

        lastError = error
        
except KeyboardInterrupt:
    GPIO.cleanup()
