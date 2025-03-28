import cv2
from picamera2 import Picamera2, Preview
from libcamera import Transform
import os
import time
from threading import Thread
import numpy as np

i = 0
i_string = ""
image_processing_file = ""
processed_file = ""
file_list = []

# starting camera
print("starting camera")
cam = Picamera2()
cam.start_preview(Preview.QTGL, transform=Transform(hflip=1, vflip=1), width=400, height=300)
cam.start()


def cameraLoop():
    global i
    global i_string
    global image_processing_file
    time.sleep(2)
    i += 1
    i_string = str(i)
    image_processing_file = str("picture" + i_string + ".jpg")
    cam.capture_file(image_processing_file)
    file_list.append(image_processing_file)
    
# cam.stop_preview()

def imageConversion():
    global image_processing_file
    global file_list
    global i
    global i_string
    print("processing image", i)
    # reads a picture taken from the camera
    image_processing_filepath = "/home/pi/" + image_processing_file
    
    frame = cv2.imread(image_processing_file) # imports camera's image into opencv
    
    frame = frame[0:240, 200:400] # crops image, (y-coord, x-coord)

    # rotates the sample image
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_180)

    # converts picture color format from RGB to HSV
    hsv_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2HSV)

    #extract only the color of the tape from the image
    blue_frame = cv2.inRange(hsv_frame, (100, 100, 100),(120, 200, 255))
    
    # reduce info in picture w/ edge detection
    edges = cv2.Canny(blue_frame, 100, 200)
    
    # looks for straight lines in image
    rho = 1
    angle = np.pi/180 # converts to radians
    min_threshold = 10
    lines = cv2.HoughLinesP(edges, rho, angle, min_threshold, None,
                            minLineLength=30, maxLineGap=3) # returns list of x,y coords of lines
    
    # processes HoughLine transformation to draw the detected line segments
    for j in range(0, len(lines)):
        line = lines[j][0]
        cv2.line(edges, (line[0], line[1]), (line[2], line[3]), (120, 0, 120), 2, cv2.LINE_AA)
    
    # saves adjustments to a processed file
    processed_file = "/home/pi/processed_lines" + i_string + ".jpg"
    file_list.append(processed_file)
    print("image", i, "processed")
    cv2.imwrite(processed_file, edges)

# cameraThread = Thread(target=cameraLoop)
# processThread = Thread(target=imageConversion)
# cameraThread.start()
# processThread.start()

# after 5 images have been processed, delete the last 5 images
def imageDeletion():
    global file_list
    global i
    if i == 5:
        for i in range(0,10):
            os.remove(file_list[i])
            print(f"{file_list[i]} has been deleted")
            file_list[i] = ""
        i = 0
    else:
        pass

while True:
    imageDeletion()
    cameraLoop()
    imageConversion()

