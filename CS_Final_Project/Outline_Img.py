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
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edged = cv2.Canny(image, 10, 250)
    (_,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    idx = 0
    for c in cnts:
        x,y,w,h = cv2.boundingRect(c)
        if w>50 and h>50:
            idx+=1
            new_img=image[y:y+h,x:x+w]
            cv2.imwrite(str(idx) + '.png', new_img)
    cv2.imshow("im",image)
    cv2.waitKey(0)
