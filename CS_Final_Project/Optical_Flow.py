#import openCv for image/video handling
import cv2 as cv
#import math functions
import numpy as np
#creates video feed
cap = cv.VideoCapture(0)
#imports frame
ret, frame1 = cap.read()
#converts to gray
prvs = cv.cvtColor(frame1,cv.COLOR_BGR2GRAY)
#creates a blank array of the size of the image
hsv = np.zeros_like(frame1)
hsv[...,1] = 255
#Keeps processing until user turns off
while(1):
    #creates a second frame
    ret, frame2 = cap.read()
    next = cv.cvtColor(frame2,cv.COLOR_BGR2GRAY)
    #compares old frame with new frame for discrepancies
    flow = cv.calcOpticalFlowFarneback(prvs,next, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    #processes image comparison
    mag, ang = cv.cartToPolar(flow[...,0], flow[...,1])
    hsv[...,0] = ang*180/np.pi/2
    hsv[...,2] = cv.normalize(mag,None,0,255,cv.NORM_MINMAX)
    bgr = cv.cvtColor(hsv,cv.COLOR_HSV2BGR)
    #shows frame of optical flow
    cv.imshow('frame2',bgr)
    #sets up escape sequence
    k = cv.waitKey(30) & 0xff
    #breaks if escape sequence is triggered
    if k == 27:
        break
    #saves files if commanded to
    elif k == ord('s'):
        cv.imwrite('opticalfb.png',frame2)
        cv.imwrite('opticalhsv.png',bgr)
    #sets the new frame to the old frame so that the comparison can be done again
    prvs = next
#releases the film feed
cap.release()
#kills all of the windows
cv.destroyAllWindows()