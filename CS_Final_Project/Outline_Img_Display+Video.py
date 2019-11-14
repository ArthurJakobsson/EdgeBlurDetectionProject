#import open cv for image handling
import cv2
#import camera stream functions from camera tools program
from Camera_Tools import Cameras
#import cropping functions from camera tools program
from Camera_Tools import Cut
#imports copy for copying objects
import copy

#sets "instance" variables for this program
SCALE = 0.5
max_lowThreshold = 15
window_name = 'Edge Dragger'
title_trackbar = 'Min Threshold:'
ratio = 3
slider_low = 0
slider_val = 10
edged=0

#function handles the slider value and sets the slider value globally (in this program/class)
def defineVal(val):
    slider_val = val
    print ("Slider_val", slider_val)

#function displays video stream as well as handles cropping and creating contours
def diplayVideo():
    #starting point for naming of the cropped files
    num=0
    #runs code until user escape sequence is hit. Hit "esc" key to exit
    while True:
        #imports the stream and individual image frames to this program
        frame, stream = Cameras.readStream()
        #convets the original frame to gray for easier viewing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #resizes the plain image for better processing
        grayResized = cv2.resize(gray, None, fx=SCALE, fy=SCALE)
        #displays plain, unchanged version of the image
        cv2.imshow("Frame", grayResized)
        #resizes the image to reduce processing a bit
        image = cv2.resize(frame, None, fx=SCALE, fy=SCALE)
        #reading the image 
        lap = cv2.Laplacian(image, cv2.CV_64F)
        edged = cv2.Canny(image, 10, 250)
        #shows laplaced version of image (fuzzy and shows lines better)
        cv2.imshow("laplacian", lap)
        #show edged images
        cv2.imshow("Edges", edged)

    
        #applying closing function 
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
        #closes "plain" image based on iterations defined by slider
        plain = cv2.morphologyEx(edged, cv2.MORPH_TOPHAT, kernel, iterations=slider_val)
        #closes "closed" image two times for more accurate precision
        closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel, iterations=4)
        #expands the closing for images to expand approximation
        dilation = cv2.dilate(closed.copy(),kernel,iterations = 3)
        #show dilated closed image
        cv2.imshow("Dilated", dilation)
        #show plain closed image
        cv2.imshow("Closed", closed)
        #finding_contours 
        closedOpp = cv2.bitwise_not(closed)
        #defines the countours in an list
        (_, cntsClosed, _) = cv2.findContours(closedOpp.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #creates a copy of the image to crop file without contour lines
        chopImage = image.copy()
        #creates an image for closed contour cropping and display
        closedCntsImage = image.copy()
        #c means each closed figure
        for c in cntsClosed:
            #approximates visualization arcs
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)
            #draws the arcs on image
            cv2.drawContours(closedCntsImage, [approx], -1, (0, 255, 0), 2)
        #displays the image with countouring based off of closed version
        cv2.imshow("Output", closedCntsImage)
        

        #defines the countours in an list
        (_, cnts, _) = cv2.findContours(plain.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #cycles through all the countours
        for c in cnts:
            #approximates visualization arcs
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.01 * peri, True)
            #draws the arcs on image
            cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        #defines the countours based on the un-closed version
        cv2.imshow("Plain Output", image)
        #creates a step counter to change file names
        num = Cut.crop(chopImage, cnts, num)
        #escape sequence using "esc" key
        k= cv2.waitKey(30) & 0xFF
        if k == 27:
            break

    Cameras.killFeed(stream)



#creates slider
cv2.namedWindow(window_name)
cv2.createTrackbar(title_trackbar, window_name , slider_low, max_lowThreshold, defineVal)

#runs video displaying
diplayVideo()