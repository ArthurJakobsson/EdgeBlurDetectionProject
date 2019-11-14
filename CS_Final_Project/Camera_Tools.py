#imports open cv for video stream handling
import cv2

#from imutils.video import FPS

#class to handle camera actions
class Cameras:
    #reads and sends stream data
    def readStream():
        #begins stream
        stream = cv2.VideoCapture(0)
        #fps = FPS().start()
        #creates the frame from stream data
        _, frame = stream.read()
        #sends frames and stream object
        return frame, stream

    #kills the feed
    #Parameter: Stream object
    def killFeed(stream):
        #stream object is killed
        stream.release()
        #windows are closed
        cv2.destroyAllWindows()
#class to handle cropping options
class Cut:
    #function to crop image
    #Parameters: image to crop, lines to crop around, and the number appendix to the cropped image file
    def crop(image, cnts, num):
        
        idx = 0
        #cycles through all the contours to crop all
        for c in cnts:
            #creates an approximate rectangle around contour
            x,y,w,h = cv2.boundingRect(c)
            #If cropping rectangle is not tiny then cropping happens
            if w>50 and h>50:
                idx+=1
                #crops the image out of the image
                new_img=image[y:y+h,x:x+w]
                #writes the new file in the Crops folder
                cv2.imwrite('Crops/'+str(num)+'_'+str(idx) + '.png', new_img)
                num=num+1
        #returns a number incremented up for the next file name
        return num+1