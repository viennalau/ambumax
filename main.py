# importing things
from gpiozero import Motor
from gpiozero import DistanceSensor
from gpiozero.pins.pigpio import PiGPIOFactory
import time
import pygame
import sys
from picamera2 import Picamera2, Preview
from libcamera import Transform

global speed
speed = 0
left_speed = 0
right_speed = 0
factory = PiGPIOFactory()
dist_sensor = DistanceSensor(echo=10, trigger=5, pin_factory=factory)

#camera setup
def live_camera():
    cam = Picamera2()
    #cam.start_preview(Preview.QTGL)
    cam.start_preview(Preview.QTGL, x=910, y=100, width=600, height=600, transform=Transform(hflip=1, vflip=1))
    cam.start()
    #cam.capture_file("test.jpg")
    #cam.stop_preview()

# calling live_camera before the while loop
live_camera()

# pygame window opens
pygame.init()
display = pygame.display.set_mode((300, 300))

# creating robot class and adding definitions for movement
class Robot():
    def __init__(self, lm_1, lm_2, rm_1, rm_2):
        self.lm = Motor(lm_1, lm_2)
        self.rm = Motor(rm_1, rm_2)
        
    def straight(self, speed):
        self.lm.forward(speed)
        self.rm.forward(speed)
        #time.sleep(0.5)
        #self.rm.forward(speed=.25)
        #self.lm.forward(speed=.5)
        
    def straight_backward(self, speed):
        self.lm.backward(speed)
        self.rm.backward(speed)
        
    def stop(self):
        self.lm.stop()
        self.rm.stop()
        
    def turn_left(self, left_speed, right_speed):
        self.lm.backward(left_speed)
        self.rm.forward(right_speed)
        
    def turn_right(self, left_speed, right_speed):
        self.rm.backward(right_speed)
        self.lm.forward(left_speed)
    
#     def soft_left(self):
#         self.lm.forward(speed=.125)
#         self.rm.forward(speed=.25)
#         
#     def soft_right(self):
#         self.rm.forward(speed=.125)
#         self.lm.forward(speed=.5)
        
# inputting GPIO pins for movement
ambulance = Robot(18,22,27,17)

# while True:
#     print("Distance:", dist_sensor.distance*(100/2.54))
#     time.sleep(1)

#monitoring inputs/driving the car
while True:
    i = 0
    print("Distance:", round(dist_sensor.distance*(100/2.54), 2), "inches")
    time.sleep(1)
    #creating a loop to check events that are occuring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print("Key W has been pressed. moving forward")
                ambulance.straight_backward(1)
                
            if event.key == pygame.K_s:
                print("Key S has been pressed. moving backward")
                ambulance.straight(1)
                
            if event.key == pygame.K_a:
                i += 1
                if right_speed < 1:
                    left_speed += 0.1
                    right_speed += 0.2
                else:
                    left_speed = 0.5
                    right_speed = 1
                ambulance.turn_left(left_speed, right_speed)
                print(f"key press # {i}, left = {left_speed} right = {right_speed}")
                    
        
            if event.key == pygame.K_d:
                i += 1
                if left_speed < 1:
                    left_speed += 0.2
                    right_speed += 0.1
                else:
                    left_speed = 1
                    right_speed = 0.5     
                ambulance.turn_right(left_speed, right_speed)
                print(f"key press # {i}, left = {left_speed} right = {right_speed}")
                
#             if event.key == pygame.K_w and event.key == pygame.K_a:
#                 print("Key w/a has been pressed, going forward + left")
#                 ambulance.forward()
#                 time.sleep(.25)
#                 ambulance.soft_left()
#             if event.key == pygame.K_w and event.key == pygame.K_a:
#                 print("Key w/d has been pressed, going forward + right")
#                 ambulance.forward()
#                 time.sleep(.25)
#                 ambulance.soft_right()
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_s:
                print("Key W/S has been released. stopping the car")
                ambulance.stop()
            if event.key == pygame.K_a or event.key == pygame.K_d:
                print("Key A/D has been released, straightening the car")
                left_speed = 0.25
                right_speed = 0.25
                ambulance.straight_backward(.5)
    
