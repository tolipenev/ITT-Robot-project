#!/usr/bin/python
import RPi.GPIO as GPIO
import time

dc_forward = 60
dc_turn = 20
isStopped = True
config = []


def gpioConfig():
    try:
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(17, GPIO.OUT)
        GPIO.setup(18, GPIO.OUT)
        GPIO.setup(15, GPIO.OUT)
        GPIO.setup(4, GPIO.OUT)
        GPIO.setup(3, GPIO.OUT)
        GPIO.setup(2, GPIO.OUT)
        GPIO.setup(24, GPIO.IN)
        GPIO.setup(23, GPIO.OUT)
        GPIO.setup(22, GPIO.IN)
        GPIO.setup(27, GPIO.IN)

        GPIO.setup(17, GPIO.HIGH)
        GPIO.setup(18, GPIO.LOW)
        GPIO.setup(4, GPIO.HIGH)
        GPIO.setup(3, GPIO.LOW)
        GPIO.output(23, GPIO.HIGH)
        GPIO.add_event_detect(24, GPIO.RISING, callback=goLeft)
        GPIO.add_event_detect(22, GPIO.RISING, callback=goStraight)
        GPIO.add_event_detect(27, GPIO.RISING, callback=goRight)
    except:
        GPIO.cleanup()


def cleanupGpio():
    GPIO.cleanup()


def motorConfig():
    global config
    LM = GPIO.PWM(15, 50)
    RM = GPIO.PWM(2, 50)
    config = [LM, RM]


def stop():
    global isStopped
    global config
    LM = config[0]
    RM = config[1]
    print("stopped")
    if (isStopped == False):
        LM.stop()
        RM.stop()
        isStopped = True
    config[0] = LM
    config[1] = RM


def goLeft(channel):
    global isStopped
    global config
    global result
    slVal = GPIO.input(24)
    scVal = GPIO.input(22)
    LM = config[0]
    RM = config[1]

    while (slVal == 1):
        if (scVal == 1):
            if (isStopped == True):
                LM.start(dc_turn)
                RM.start(dc_forward)
                isStopped = False
            elif (isStopped == False):
                LM.ChangeDutyCycle(dc_turn)
                RM.ChangeDutyCycle(dc_forward)
            config[0] = LM
            config[1] = RM
        elif (scVal == 0):
            if (isStopped == True):
                LM.start(0)
                RM.start(dc_forward)
                isStopped = False
            elif (isStopped == False):
                LM.ChangeDutyCycle(0)
                RM.ChangeDutyCycle(dc_forward)
            config[0] = LM
            config[1] = RM

        slVal = GPIO.input(24)
        # time.sleep(0.3)


def goRight(channel):
    global isStopped
    global config
    global result
    srVal = GPIO.input(27)
    scVal = GPIO.input(22)
    LM = config[0]
    RM = config[1]

    while (srVal == 1):
        if (scVal == 1):
            if (isStopped == True):
                LM.start(dc_forward)
                RM.start(dc_turn)
                isStopped = False
            elif (isStopped == False):
                LM.ChangeDutyCycle(dc_forward)
                RM.ChangeDutyCycle(dc_turn)
            config[0] = LM
            config[1] = RM

        elif (scVal == 0):
            if (isStopped == True):
                LM.start(dc_forward)
                RM.start(0)
                isStopped = False
            elif (isStopped == False):
                LM.ChangeDutyCycle(dc_forward)
                RM.ChangeDutyCycle(0)
            config[0] = LM
            config[1] = RM

        srVal = GPIO.input(27)


def goStraight(channel):
    global isStopped
    global config

    slVal = GPIO.input(24)
    scVal = GPIO.input(22)
    srVal = GPIO.input(27)
    LM = config[0]
    RM = config[1]
    while (scVal == 1):

        if (isStopped == True):
            LM.start(dc_forward)
            RM.start(dc_forward)
            isStopped = False
        elif (isStopped == False):
            LM.ChangeDutyCycle(dc_forward)
            RM.ChangeDutyCycle(dc_forward)
        config[0] = LM
        config[1] = RM
        scVal = GPIO.input(22)
        # time.sleep(0.3)


def steering():
    try:
        slVal = GPIO.input(24)
        scVal = GPIO.input(22)
        srVal = GPIO.input(27)
        goStraight(None)

        while (True):

            if (GPIO.event_detected(24)):
                print("left sensor event")

            elif (GPIO.event_detected(22)):
                print("center sensor event")

            elif (GPIO.event_detected(27)):
                print("right sensor event")


    except KeyboardInterrupt:
        cleanupGpio()


if __name__ == "__main__":
    gpioConfig()
    motorConfig()
    steering()
