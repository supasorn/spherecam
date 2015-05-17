import RPi.GPIO as GPIO
import wiringpi2 as wiringpi
import time
class Servo:
    def __init__(self, base = 26):
        wiringpi.wiringPiSetupGpio()
        wiringpi.pinMode(18,2)
        wiringpi.pwmSetMode(0)
        wiringpi.pwmSetClock(400)
        wiringpi.pwmSetRange(1024)
        wiringpi.pwmWrite(18, 0)
        self.base = base
        self.setAngle(90)

    def setAngle(self, deg):
        #print (self.base + 93 *deg / 180)
        wiringpi.pwmWrite(18, self.base + 93 * deg / 180)
    def done(self):
        wiringpi.pinMode(18, 0)

class Stepper:
    seq = [ [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1],
            [1,0,0,1]];
    s = 0
    coil_A_1_pin = 31 
    coil_A_2_pin = 33 
    coil_B_1_pin = 35 
    coil_B_2_pin = 37 

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.coil_A_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_A_2_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_1_pin, GPIO.OUT)
        GPIO.setup(self.coil_B_2_pin, GPIO.OUT)

    def move(self, direction, steps, delay = 0.005): #512 is full rev
        for i in range(steps):
            for k in range(len(self.seq)):
                if direction > 0:
                    self.s = (self.s+1) % 8
                else:
                    self.s = (self.s+7) % 8
                #print self.s
                self.setStep(self.seq[self.s][0], self.seq[self.s][1], self.seq[self.s][2], self.seq[self.s][3])
                time.sleep(delay)
        self.setStep(0, 0, 0, 0)

    def setStep(self, w1, w2, w3, w4):
        GPIO.output(self.coil_A_1_pin, w1)
        GPIO.output(self.coil_A_2_pin, w2)
        GPIO.output(self.coil_B_1_pin, w3)
        GPIO.output(self.coil_B_2_pin, w4)

    def done(self):
        GPIO.cleanup()
 


