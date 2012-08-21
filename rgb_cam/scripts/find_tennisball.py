#!/usr/bin/env python
"""
1.  Obtain image containing tennis ball in live feed
2.  Identify circles in feed
3.  Draw Identified circles in output video
"""
__author__ = 'Robert Cofield'

import sys, os
import cv2.cv as cv
import pdb


def main():
    print 'In find_tennisball'
    cv.NamedWindow("rgb", 2)
    cv.NamedWindow("gray", 2)
    cv.NamedWindow("thold - gray", 2)
    cv.NamedWindow("red", 2)
    cv.NamedWindow("blue", 2)
    cv.NamedWindow("green", 2)

    capture = cv.CaptureFromCAM(-1)
    size = cv.GetSize(cv.QueryFrame(capture))
    while True:
        img = cv.QueryFrame(capture)
        
        ### RGB - show hough on thresholded grayscale ###
        rgb = cv.CreateImage(size, 8, 3)
        cv.Copy(img, rgb)
        gray = cv.CreateImage(size, 8, 1)
        # edges = cv.CreateImage(cv.GetSize(rgb), 8, 1)
        cv.CvtColor(rgb, gray, cv.CV_BGR2GRAY)
        cv.ShowImage("gray", gray)
        cv.Threshold(gray, gray, 205, 255, cv.CV_THRESH_BINARY)
        cv.ShowImage("thold - gray", gray)
        cv.Smooth(gray, gray, cv.CV_GAUSSIAN, 15, 15)
        storage = cv.CreateMat(1, rgb.height * rgb.width, cv.CV_32FC3)
        cv.HoughCircles(gray, storage, cv.CV_HOUGH_GRADIENT, \
            1, 5, 200, 30, min_radius=0, max_radius=240)
        red = cv.CreateImage(size, 8, 1)
        blu = cv.CreateImage(size, 8, 1)
        grn = cv.CreateImage(size, 8, 1)
        cv.Split(rgb, red, blu, grn, None)
        cv.ShowImage("red", red)
        cv.ShowImage("blue", blu)
        cv.ShowImage("green", grn)

        for i in range(storage.width - 1):
            center = (int(storage[0,i][0]), int(storage[0,i][1]))
            radius = int(storage[0,i][2])
            cv.Circle(rgb, center, radius, (0, 0, 255), thickness=2)


        # ### HSV - show hough on hue ###
        # hsv = cv.CreateImage(size, 8, 3)
        # cv.CvtColor(img, hsv, cv.CV_BGR2HSV)
        # # cv.ShowImage("hsv", hsv)
        # hue = cv.CreateImage(size, 8, 1)
        # sat = cv.CreateImage(size, 8, 1)
        # # val = cv.CreateImage(size, 8, 1)
        # cv.Split(hsv, hue, None, None, None)
        # hue_t = cv.CreateImage(size, 8, 1)
        # # cv.Not(hue_t, hue_t)
        # # If these params are wrong, overload will occur
        # cv.Threshold(hue, hue_t, 150, 255, cv.CV_THRESH_BINARY)
        # # storage = cv.CreateMat(1, img.height * img.width, cv.CV_32FC3)
        # # cv.HoughCircles(hue_t, storage, cv.CV_HOUGH_GRADIENT, \
        # #     1, 5, 200, 30, min_radius=0, max_radius=240)
        # # # Draw solution on hue
        # # for i in range(storage.width - 1):
        # #     center = (int(storage[0,i][0]), int(storage[0,i][1]))
        # #     radius = int(storage[0,i][2])
        # #     cv.Circle(rgb, center, radius, (255, 0, 0), thickness=2)
        # cv.ShowImage("hue", hue)
        # cv.ShowImage("hue_t", hue_t)
        # # cv.ShowImage("saturation", sat)
        # # cv.ShowImage("value", val)


        cv.ShowImage("rgb", rgb)

        if cv.WaitKey(10) == 27:
            # shut down the camera (hack from ros)
            os.system('bash xn_sensor_server_cleanup.sh')
            cv.DestroyAllWindows()
            break


    return rgb


if __name__ == '__main__':
    main()
