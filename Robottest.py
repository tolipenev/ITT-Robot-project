import RPi.GPIO as GPIO
from threading import Thread, ThreadError


class Robot:
    left = None
    right = None
    center = None
    duty = 50  # optimal speed
    multiplier = 2
    mot_left = None
    mot_right = None

    def init_gpio(self):
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
        except:
            GPIO.cleanup()
            self.mot_left = GPIO.PWM(15, self.duty)  # left motor
            self.mot_right = GPIO.PWM(2, self.duty)  # right motor

    def read_ios(self):  # thread1
        self.left = GPIO.input(24)
        self.center = GPIO.input(22)
        self.right = GPIO.input(27)

    def move(self, left, right):
        self.mot_left.start(left) # left motor
        self.mot_right.start(right)  # right motor

    def move_correction(self, left, right):
        self.mot_left.ChangeDutyCycle(left)
        self.mot_right.ChangeDutyCycle(right)

    def correct_path(self):  # thread2
        while True:
            self.move(self.duty, self.duty)
            if self.left is 1 and self.center is 0:
                self.move_correction(self.duty, self.duty * self.multiplier)
                while self.left is 1 and self.center is 0:
                    pass
            elif self.right is 1 and self.center is 0:
                self.move_correction(self.duty * self.multiplier, self.duty)
                while self.right is 1 and self.center is 0:
                    pass

    def start_threads(self):
        reading = Thread(name='readIos', target=self.read_ios)
        correction = Thread(name='correctPath', target=self.correct_path)
        try:
            reading.start()
            correction.start()
        except ThreadError as e:
            print(e)


if __name__ == "__main__":
    robot = Robot()
    robot.init_gpio()
    robot.start_threads()
