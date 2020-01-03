#! /usr/bin/python
import cv2
import numpy as np
import sys


#define image dimensions
IMG_WIDTH = 320
IMG_HEIGHT = 240
CAMID = 0

# create named window, set position
cv2.namedWindow('img',2)
cv2.moveWindow('img',0,0)

###########################################################
# With help of this class the correct HSV values can be
# selected from a picture color space
# this values can be further used i.e. for skin detection.
# Track-bars will appear if debug mode is activated!
###########################################################
class clPreProcessing():
    def __init__(self,debug=True, h=122,s=22,v=0):
        self.img = []
        self.debug = debug
        self.h = h
        self.s = s
        self.v = v

        if self.debug == True:
            # create trackbars for color change
            cv2.createTrackbar('h', 'img', 0, 255, self.nothing)
            cv2.createTrackbar('s', 'img', 0, 255, self.nothing)
            cv2.createTrackbar('v', 'img', 0, 255, self.nothing)

    def nothing(self,x):
        pass

    ##################################
    # Make color space transformation
    ##################################
    def processImg(self, img):

        if self.debug == True:
            self.h = cv2.getTrackbarPos('h', 'img')
            self.s = cv2.getTrackbarPos('s', 'img')
            self.v = cv2.getTrackbarPos('v', 'img')

        # snoth the image
        self.img = cv2.medianBlur(img, 7)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        # set color space domain
        lower_color = np.array([self.h, self.s, self.v])
        upper_color = np.array([self.h + 80, 255, 255])

        # filter HSV image
        mask = cv2.inRange(self.img, lower_color, upper_color)

        # apply mask on the original image
        self.img = cv2.bitwise_and(img, img, mask=mask)

        return self.img


# main loop
if __name__ == "__main__":

    #simple arg processor
    # 1 - sys[1] is the camera ID
    if len(sys.argv)>1:

        #we have additional argument(s)
        for i in range(1,len(sys.argv)):
            # process argument(s)
            
            # set 1 cam ID
            if i == 1:
                CAMID = int(sys.argv[i])
    else:
        # we ahve a single argument, do nothing
        pass

    # create cam instance
    cam0 = cv2.VideoCapture(CAMID)

    # resize, to spare CPU load
    cam0.set(3,IMG_WIDTH)
    cam0.set(4,IMG_HEIGHT)


    # create preprocessing class
    objPP = clPreProcessing(True)

    while (True):

        #grab a frame
        _, img0 = cam0.read()

        # test cam instance
        if (cam0):

            img1 = objPP.processImg(img0)

            #show image
            cv2.imshow('img', img1)

        # quit on keypress
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
          break

    # release cam
    cam0.release()
    cv2.destroyAllWindows()
