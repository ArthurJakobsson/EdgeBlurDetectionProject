#this file is an older version. The newest version is Outline_Img_Display+Video.py

import cv2
from imutils import paths
import argparse

SCALE = 0.5

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--images', required=True,
    help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
    help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())


for imagePath in paths.list_images(args["images"]):

    image = cv2.imread(imagePath)
    image = cv2.resize(image, None, fx=SCALE, fy=SCALE)
    #reading the image 
    edged = cv2.Canny(image, 10, 250)
    cv2.imshow("Edges", edged)

 
    #applying closing function 
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7, 7))
    closed = cv2.morphologyEx(edged, cv2.MORPH_CLOSE, kernel)
    dilation = cv2.dilate(closed.copy(),kernel,iterations = 2)
    cv2.imshow("Dilated", dilation)
    cv2.imshow("Closed", closed)

    
    #finding_contours 
    (_, cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #name value of file
    idx = 0
    
    for c in cnts:
        #approximates visualization arcs
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.001 * peri, True)
        #draws the arcs on image
        cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
        #crops the parts of the files based on the contour
        x,y,w,h = cv2.boundingRect(c)
        if w>50 and h>50:
            idx+=1
            new_img=image[y:y+h,x:x+w]
            #writes the new file with the smaller image
            cv2.imwrite(str(idx) + '.png', new_img)


    cv2.imshow("Output", image)
    cv2.waitKey(0)