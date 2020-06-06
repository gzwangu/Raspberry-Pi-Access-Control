import json
import time
import cv2
# import RPi.GPIO as GPIO
#from controller.utils.camera import VideoCamera
#from picamera import PiCamera

pin_4 = 4,    #蜂鸣器       
pin_10 = 10,  #开关      
pin_5 = 5,      #电机
pin_6 = 6,
pin_12 = 12,
pin_13 = 13
class ControlMotor:
    def __init__(self):       
        self.mt_path = '/home/pi/monitors/faces/'
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin_4, GPIO.OUT)
        GPIO.setup(pin_10, GPIO.IN)
        GPIO.setup(pin_5, GPIO.OUT)
        GPIO.setup(pin_6, GPIO.OUT)
        GPIO.setup(pin_12, GPIO.OUT)
        GPIO.setup(pin_13, GPIO.OUT)

    def __del__(self):
        GPIO.cleanup()

    def setStep(self,w1, w2, w3, w4):
        GPIO.output(pin_5, w1)
        GPIO.output(pin_6, w2)
        GPIO.output(pin_12, w3)
        GPIO.output(pin_13, w4)

    def forward(self,delay,step):   #开门
        for i in range(0, step):
            self.setStep(1, 0, 0, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 0)
            time.sleep(delay)
            self.setStep(0, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 0, 0, 1)
            time.sleep(delay)

    def backward(self,delay,step):   #关门
        for i in range(0, step):
            self.setStep(0, 0, 0, 1)
            time.sleep(delay)
            self.setStep(0, 0, 1, 0)
            time.sleep(delay)
            self.setStep(0, 1, 0, 0)
            time.sleep(delay)
            self.setStep(1, 0, 0, 0)
            time.sleep(delay)

    def camera_pi(self):
        video_camera = VideoCamera()
        frame = video_camera.get_photo()
        time_now = time.time()
        name_face = str(int(time_now))
        path_face = self.mt_path + name_face +'.jpg'
        cv2.imwrite(path_face,frame)
        return name_face,path_face
            
    def ocdoor(self,confidence):
        if confidence > 90:
            self.forward(0.002,300)
            time.sleep(3)
            self.backward(0.002,300)
        else:
            GPIO.output(pin_4,1)
            time.sleep(3)
            GPIO.output(pin_4,0)
            
    def been(self):
        GPIO.output(pin_4,1)
        time.sleep(3)
        GPIO.output(pin_4,0)

