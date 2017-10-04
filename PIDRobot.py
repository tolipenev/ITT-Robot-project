#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import ptvsd

ptvsd.enable_attach('visual')

GPIO.setmode(GPIO.BCM)


lmControl1 = 17
lmControl2 = 18
lmEnable = 15
rmControl1 = 3
rmControl2 = 4
rmEnable = 2
lsOut = 24
sensVCC = 23
csOut = 22
rsOut = 27

GPIO.setup(lmControl1, GPIO.OUT)
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
LM = GPIO.PWM(lmEnable, 50)
RM = GPIO.PWM(rmEnable, 50)    


def getError():
    
    sensor = [GPIO.input(lsOut), GPIO.input(csOut), GPIO.input(rsOut)]
    error = str(sensor[0]) + str(sensor[1]) + str(sensor[2])
    #error = int(error)

    if(error == '000'):
        error = 0
    elif(error == '001'):
        error = 2
    elif(error == '010'):
        error = 0
    elif(error == '011'):
        error = 1
    elif(error == '100'):
        error = -2
    elif(error == '101'):
        error = 0
    elif(error == '110'):
        error = -1
    elif(error == '111'):
        error = 0   

    return error

def run(dcL, dcR):
    try:        
        dcL = int(dcL)
        dcR = int(dcR)
        
        if(dcL > 0):
            if(dcL > 100):
                GPIO.setup(lmControl1, GPIO.HIGH)
                GPIO.setup(lmControl2, GPIO.LOW)
                LM.start(80)
            else:
                GPIO.setup(lmControl1, GPIO.HIGH)
                GPIO.setup(lmControl2, GPIO.LOW)
                LM.start(dcL)
        else:
            if(dcL < -100):
                GPIO.setup(lmControl1, GPIO.LOW)
                GPIO.setup(lmControl2, GPIO.HIGH)
                LM.start(80)
            else:
                GPIO.setup(lmControl1, GPIO.LOW)
                GPIO.setup(lmControl2, GPIO.HIGH)
                LM.start(dcL * (-1))

        if(dcR > 0):
            if(dcR > 100):
                GPIO.setup(rmControl1, GPIO.HIGH)
                GPIO.setup(rmControl2, GPIO.LOW)
                RM.start(80)
            else:
                GPIO.setup(rmControl1, GPIO.HIGH)
                GPIO.setup(rmControl2, GPIO.LOW)
                RM.start(dcR)
        else:
            if(dcR < -100):
                GPIO.setup(rmControl1, GPIO.LOW)
                GPIO.setup(rmControl2, GPIO.HIGH)
                RM.start(80)
            else:
                GPIO.setup(rmControl1, GPIO.LOW)
                GPIO.setup(rmControl2, GPIO.HIGH)
                RM.start(dcR *(-1))
        
    except KeyboardInterrupt:
        GPIO.cleanup()

def stop():
    LM.stop()
    RM.stop()
        

Kp = 90
Ki = 22
Kd = 100500
offset = 0.5
Tp = 190
integral = 0
integral_max = 5
integral_min = -5
lastError = 0
derivative = 0
try:
    while(True):
        error = getError()
        
        error = error - offset
        integral = integral + error
        if(integral > integral_max):
            integral = integral_max
        elif(integral < integral_min):
            integral = integral_min
        derivative = error - lastError
        Turn = Kp*error + Ki*integral + Kd*derivative
        run(Tp + Turn, Tp - Turn)
        lastError = error
        #print (Turn)
except KeyboardInterrupt:
    GPIO.cleanup()
