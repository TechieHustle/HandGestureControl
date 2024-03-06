import numpy as np
import cv2
import time
import ctypes
from ctypes import wintypes
from keybord_event import *

####Find the approperiate limit values for masking using the HSV trackbar function
parameter1_red = [164,143,137]#####Upper limit for HSV for Red pass filter
parameter2_red = [179,255,255]#####Lower limit for HSV for Red pass filter

parameter1_green = [ 64,202, 98]#####Upper limit for HSV for Green pass filter
parameter2_green = [ 92,255,148]#####Lower limit for HSV for Green pass filter

lower_red = np.array(parameter1_red)
upper_red = np.array(parameter2_red)

lower_green = np.array(parameter1_green)
upper_green = np.array(parameter2_green)

count_r = 0
count_l = 0

cx_red = 0
cy_red = 0

cx_green = 0
cy_green = 0

green_found = 0 ####Flag to find for Zoom in

zoom_out_val = 0
zoom_in_val = 0
cap = cv2.VideoCapture(1)

##Getting dummy images from camera
for i in range (5):
    ret, img = cap.read()#get image from camera
    time.sleep(0.5)
   
def centroid():
    global cx_red
    global cy_red
    global cx_green
    global cy_green
    global green_found
    print '__________________________________________'
    
    ret, img = cap.read()   ####Reading the images
    img = cv2.resize(img ,(0,0),fx = 0.3,fy = 0.3)  ####Decresing Resolution for fast computation
    height,width,channel = img.shape
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)       ####Filtering the Red part of image
    mask_green = cv2.inRange(hsv, lower_green, upper_green) ####Filtering the Green part of image

    temp1_red = 0
    temp2_red = 0
    count_red = 0

    temp1_green = 0
    temp2_green = 0
    count_green = 0
    for i in range(height):
        for j in range(width):
            if mask_red[i][j] >240:
                count_red = count_red +1
                temp1_red=temp1_red+i
                temp2_red=temp2_red+j
            if mask_green[i][j] >240:
                green_found = 1
                count_green = count_green +1
                temp1_green=temp1_green+i
                temp2_green=temp2_green+j
            elif count_green is 0:
                green_found = 0
    if count_red is not 0:
        cx_red=temp1_red/count_red 
        cy_red=temp2_red/count_red 

    if count_green is not 0:
        cx_green=temp1_green/count_green 
        cy_green=temp2_green/count_green 
    
    print cy_red,cx_red
    print cy_green,cx_green
    cv2.circle(img,(cy_red,cx_red), 4, (0,0,255), -1)
    cv2.circle(img,(cy_green,cx_green), 4, (0,255,0), -1)
    cv2.imshow('Centroid',img)
    print '__________________________________'

while(1):
    if cv2.waitKey(1) == 27:  #### 27 - ASCII value for escape key
        print 'See you again'
        break
    
    (previous_cx_red, previous_cy_red) = (cx_red, cy_red)
    (previous_cx_green, previous_cy_green) = (cx_green, cy_green)

    difference_x_previous = cx_red - cx_green
    difference_y_previous = cy_red - cy_green
    if difference_x_previous < 0:
        difference_x_previous = (-1)*difference_x_previous
    if difference_y_previous < 0:
        difference_y_previous = (-1)*difference_y_previous

    centroid()
    if count_r <10 and count_l < 10:
        if cy_red < previous_cy_red :
            count_r = count_r+1
            count_l = 0
        elif cy_red > previous_cy_red :
            count_l = count_l+1
            count_r = 0
        else:
            count_l = 0
            count_r = 0
    elif count_r is 10 and green_found is 0:
        print 'Right'
        PressKey(VK_RIGHT)
        ReleaseKey(VK_RIGHT)
        count_r = 0
        count_l = 0
    elif count_l is 10 and green_found is 0:
        print 'Left'
        PressKey(VK_LEFT)
        ReleaseKey(VK_LEFT)
        count_r = 0
        count_l = 0

    difference_x = cx_green - cx_red
    difference_y = cy_green - cy_red
    if difference_x < 0:
        difference_x = (-1) * (difference_x)
    if difference_y < 0:
        difference_y = (-1) * (difference_y)
        
    if green_found is 1:
        print 'green found'
        if (difference_x+difference_y) >  \
           (difference_x_previous+difference_y_previous):
            print 'zoom in'
            zoom_in_val += 1
            zoom_out_val = 0
            if zoom_in_val > 10:
                PressKey(VK_LCONTROL)
                PressKey(VK_ADD)
                ReleaseKey(VK_ADD)
                ReleaseKey(VK_LCONTROL)
                zoom_in_val = 0
        elif (difference_x+difference_y)< \
             (difference_x_previous+difference_y_previous):
            print 'zoom out'
            zoom_out_val += 1
            zoom_in_val = 0
            if zoom_out_val > 10:
                PressKey(VK_LCONTROL)
                PressKey(VK_SUB)
                ReleaseKey(VK_SUB)
                ReleaseKey(VK_LCONTROL)
                zoom_out_val = 0

            
cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()

