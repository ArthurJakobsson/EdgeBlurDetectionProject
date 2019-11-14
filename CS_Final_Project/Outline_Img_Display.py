#this file is an older version. The newest version is Outline_Img_Display+Video.py

import cv2 
from imutils import paths
import argparse
from matplotlib.widgets import Slider

SCALE = 0.5
max_lowThreshold = 200
window_name = 'Edge Dragger'
title_trackbar = 'Min Threshold:'
ratio = 3
slider_low = 0
slider_val = 10
edged=0


def displayImages():
    
    for imagePath in paths.list_images(args["images"]):
        lastSliderVal=0
        image = cv2.imread(imagePath)
        image = cv2.resize(image, None, fx=SCALE, fy=SCALE)
        while True:
            slider_val = cv2.getTrackbarPos(title_trackbar, window_name)
            print (slider_val)
            edged = cv2.Canny(image, slider_val, 250)
            #cv2.imshow("Edges", edged)
            print("dif", slider_val-lastSliderVal)
            if (slider_val-lastSliderVal)>=4:
                #applying closing function 
                kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
                closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
                dilation = cv2.dilate(closed.copy(),kernel,iterations = 1)
                #cv2.imshow("Dilated", dilation)
                #cv2.imshow("Closed", closed)


                (_,cnts, _) = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for c in cnts:
                    #approximates visualization arcs
                    peri = cv2.arcLength(c, True)
                    approx = cv2.approxPolyDP(c, 0.001 * peri, True)
                    #draws the arcs on image
                    image_copy=image.copy()
                    cv2.drawContours(image_copy, [approx], -1, (0, 255, 0), 2)
                cv2.imshow("im",image_copy)
            lastSliderVal=slider_val
            k= cv2.waitKey(30) & 0xFF
            if k == 27:
                break
        cv2.waitKey(0)


def defineVal(val):
    slider_val = val
    print ("Slider_val", slider_val)




# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--images', required=True,
    help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
    help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())


#creates slider
cv2.namedWindow(window_name)
cv2.createTrackbar(title_trackbar, window_name , slider_low, max_lowThreshold, defineVal)

#runs image displaying
displayImages()