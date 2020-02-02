#! /usr/bin/python
import cv2
import numpy as np
import argparse


#define image dimensions
IMG_WIDTH = 320
IMG_HEIGHT = 240
CAMID = 0

# create named window, set position
cv2.namedWindow('img',2)
cv2.moveWindow('img',0,0)


###########################################################
# With help of this class the correct HSV values ca be
# selected from a picture color space
# this values can be further used i.e. for skin detection.
# Track-bars will appear if debug mode is activated!
###########################################################
class clPreProcessing():

    def __init__(self,img, debug=True, hmin=77,smin=133,vmin=27, hmax=189,smax=170,vmax=153):
        '''
        Set the new hue, saturation, value from a color space
        :param hmin: new value
        :param smin: new value
        :param vmin: new value
        :param hmax: new value
        :param smax: new value
        :param vmax: new value
        :return: processed image
        '''
        self.img = img
        self.debug = debug
        self.hmin = hmin
        self.smin = smin
        self.vmin = vmin
        self.hmax = hmax
        self.smax = smax
        self.vmax = vmax

        if self.debug:
            # create trackbars for color change
            self.hmin = cv2.createTrackbar('hmin', 'img',hmin,255, self.nothing)
            self.smin = cv2.createTrackbar('smin', 'img',smin,255, self.nothing)
            self.vmin = cv2.createTrackbar('vmin', 'img',vmin,255, self.nothing)
            self.hmax = cv2.createTrackbar('hmax', 'img',hmax,255, self.nothing)
            self.smax = cv2.createTrackbar('smax', 'img',smax,255, self.nothing)
            self.vmax = cv2.createTrackbar('vmax', 'img',vmax,255, self.nothing)

    def nothing(self,x):
        pass

    def SetColorFilteringThresholds(self, hmin,smin,vmin,hmax,smax,vmax):
        '''
        Set the new hue, saturation, value from a color space
        :param hmin: new value
        :param smin: new value
        :param vmin: new value
        :param hmax: new value
        :param smax: new value
        :param vmax: new value
        :return: processed image
        '''
        self.hmin = hmin
        self.smin = smin
        self.vmin = vmin
        self.hmax = hmax
        self.smax = smax
        self.vmax = vmax

    def processImg(self, img):
        '''

        :param img: input img
        :return: processed img
        '''

        if self.debug == True:
            self.hmin = cv2.getTrackbarPos('hmin', 'img')
            self.smin = cv2.getTrackbarPos('smin', 'img')
            self.vmin = cv2.getTrackbarPos('vmin', 'img')
            self.hmax = cv2.getTrackbarPos('hmax', 'img')
            self.smax = cv2.getTrackbarPos('smax', 'img')
            self.vmax = cv2.getTrackbarPos('vmax', 'img')


        # smooth the image
        self.img = self.processImg1(img)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        # set colr space domain
        lower_skin = np.array([self.hmin, self.smin, self.vmin])
        upper_skin = np.array([self.hmax,self.smax, self.vmax])

        # filter HSV image
        mask = cv2.inRange(self.img, lower_skin, upper_skin)

        # apply mask on the original image
        self.img = cv2.bitwise_and(img, img, mask=mask)

        return self.img

    def processImg1(self, img):
        '''
        Prost processing for image
        :param img: input image
        :return: processed image
        '''

        kernel = np.ones((5, 5), np.uint8)
        # smooth the image
        self.img = cv2.medianBlur(img, 11)

        self.img = cv2.dilate(self.img, kernel, iterations=3)

        self.img = cv2.morphologyEx(self.img, cv2.MORPH_CLOSE, kernel)

        return self.img

    def procesYCrBr(self, img):
        '''

        :param img: input img
        :return: processed img
        '''

        if self.debug == True:
            self.hmin = cv2.getTrackbarPos('hmin', 'img')
            self.smin = cv2.getTrackbarPos('smin', 'img')
            self.vmin = cv2.getTrackbarPos('vmin', 'img')
            self.hmax = cv2.getTrackbarPos('hmax', 'img')
            self.smax = cv2.getTrackbarPos('smax', 'img')
            self.vmax = cv2.getTrackbarPos('vmax', 'img')




        # smooth the image
        self.img = self.processImg1(img)
        self.img = cv2.cvtColor(self.img, cv2.COLOR_BGR2YCR_CB)

        # set colr space domain
        lower_skin = np.array([self.hmin, self.smin, self.vmin])
        upper_skin = np.array([self.hmax,self.smax, self.vmax])

        # filter HSV image
        mask = cv2.inRange(self.img, lower_skin, upper_skin)

        # apply mask on the original image
        self.img = cv2.bitwise_and(img, img, mask=mask)

        return self.img


# main loop
if __name__ == "__main__":

    # process cmd line arguments
    parser = argparse.ArgumentParser()

    parser.add_argument('-camid', type=int, required=False, metavar='cameraid', default=0, choices=[0,1,2,3],
                        help='camera id for frame sampling, [0,1,2,3] default=0')

    parser.add_argument('-cs', type=int, required=False, metavar='colorspace', default=0, choices=[0,1],
                        help='choose the color space HSV or YCrCb, [0,1] default=0')

    args = parser.parse_args()

    #set camera id
    CAMID = args.camid

    # create cam instance
    cam0 = cv2.VideoCapture(CAMID)

    # resize, to spare CPU load
    cam0.set(3,IMG_WIDTH)
    cam0.set(4,IMG_HEIGHT)


    # create preprocessing class
    objPP = clPreProcessing(None,True)

    while (True):

        #grab a frame
        _, img0 = cam0.read()

        # test cam instance
        if (cam0):

            if args.cs ==0:
                img1 = objPP.processImg(img0)
            elif args.cs == 1:
                img1 = objPP.procesYCrBr(img0)

            #show image
            cv2.imshow('img', img1)

        # quit on keypress
        k = cv2.waitKey(1) & 0xFF
        if k == ord('q'):
          break

    # release cam
    cam0.release()
    cv2.destroyAllWindows()
