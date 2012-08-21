#!/usr/bin/env python
"""
Bridge for sending opencv images around. 
designed for use with find_tennisball.py

puts out:
    
"""
__author__ = 'Robert Cofield'

import roslib
roslib.load_manifest('rgb_cam')
import sys, os
import rospy
import cv2.cv as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class WebcamBridge:
    """
    class for moving webcam images from opencv to ros
    """
    def __init__(self):
        self.image_pub = rospy.Publisher("/tennisballs", Image)
        self.pose_pub = rospy.Publisher("")
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/image_raw", Image, self.callback)       
        self.size = None
        rospy.sleep(1)
                  
    def callback(self, data):
        """When the camera publishes a new frame, it sends through the cv 
        processing, and publishes a new output image
        """
        print('In WebcamBridge.callback')
        # cv.WaitKey(3)
        try:
            raw = self.bridge.imgmsg_to_cv(data, 'bgr8')
            found = self.find_tennisball(raw)
            msg = self.bridge.cv_to_imgmsg(found, 'bgr8')
            self.image_pub.publish(msg)
        except CvBridgeError, e:
            print e

    def find_tennisball(self, img):
        """ROS implementation of whatever is done in script find_tennisball.py
        """
        if not self.size:
            self.size = cv.GetSize(img)
              
        ### RGB - show hough on thresholded grayscale ###
        rgb = cv.CreateImage(self.size, 8, 3)
        cv.Copy(img, rgb)
        gray = cv.CreateImage(self.size, 8, 1)
        cv.CvtColor(rgb, gray, cv.CV_BGR2GRAY)
        cv.Threshold(gray, gray, 205, 255, cv.CV_THRESH_BINARY)
        cv.Smooth(gray, gray, cv.CV_GAUSSIAN, 15, 15)
        storage = cv.CreateMat(1, rgb.height * rgb.width, cv.CV_32FC3)
        cv.HoughCircles(gray, storage, cv.CV_HOUGH_GRADIENT, \
            1, 5, 200, 30, min_radius=0, max_radius=240)
        red = cv.CreateImage(self.size, 8, 1)
        blu = cv.CreateImage(self.size, 8, 1)
        grn = cv.CreateImage(self.size, 8, 1)
        cv.Split(rgb, red, blu, grn, None)

        for i in range(storage.width - 1):
            center = (int(storage[0,i][0]), int(storage[0,i][1]))
            radius = int(storage[0,i][2])
            cv.Circle(rgb, center, radius, (0, 0, 255), thickness=2)

        return rgb


def main():
    br = WebcamBridge()
    rospy.init_node('webcam_bridge')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('Shutting Down')
    cv.DestroyAllWindows()


if __name__ == '__main__':
    main()

