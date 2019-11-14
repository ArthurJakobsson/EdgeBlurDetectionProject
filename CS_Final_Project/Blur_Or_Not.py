
from imutils import paths
#parses the file path and allows
import argparse
#
import cv2

import numpy as np

import matplotlib.pyplot as plt

#sets a scale for displaying images
SCALE = 0.5


def show(img):
    plt.axis('off')
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))



def variance_of_laplacian(img):
    # compute the Laplacian of the image and then return the focus
    # measure, which is simply the variance of the Laplacian
    return cv2.Laplacian(img, cv2.CV_64F).var()
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument('-i','--images', required=True,
    help="path to input directory of images")
ap.add_argument("-t", "--threshold", type=float, default=100.0,
    help="focus measures that fall below this value will be considered 'blurry'")
args = vars(ap.parse_args())

# loop over the input images
for imagePath in paths.list_images(args["images"]):
    # load the image, convert it to grayscale, and compute the
    # focus measure of the image using the Variance of Laplacian
    # method
    img = cv2.imread(imagePath)
    img = cv2.resize(img, None, fx=SCALE, fy=SCALE)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    height, width, channels = img.shape
    print (height, width, channels)
    text = "Not Blurry"
    
    # if the focus measure is less than the supplied threshold,
    # then the image should be considered "blurry"
    if fm < args['threshold']:
        text = "Blurry"
 
    #outline edges of shape
    edges = cv2.Canny(img,10,250)
    cv2.imshow("Edges", edges)
    # plt.subplot(121),plt.imshow(img,cmap = 'gray')
    # plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122),plt.imshow(edges,cmap = 'gray')
    # plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
    # plt.show()

    # show the image
    cv2.putText(img, "{}: {:.2f}".format(text, 10000/fm), (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    




