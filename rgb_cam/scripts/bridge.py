#!/usr/bin/env python
__author__ = 'Robert Cofield'

import roslib
roslib.load_manifest('rgb_cam')
import sys, os
import rospy
import cv2.cv as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import find_tennisball as find_ball

# cv.NamedWindow("rgb", 2)
# cv.NamedWindow("gray", 2)
# cv.NamedWindow("thold - gray", 2)
# cv.NamedWindow("red", 2)
# cv.NamedWindow("blue", 2)
# cv.NamedWindow("green", 2)

class WebcamBridge:
    """
    class for moving webcam images from opencv to ros
    """
    def __init__(self):
        # self.image_pub = rospy.Publisher("from_bridge", Image)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("to_bridge", Image, self.callback)
        
        rospy.sleep(1)
        
        self.capture = cv.CaptureFromCAM(-1)
        self.size = cv.GetSize(cv.QueryFrame(self.capture))
        
        # cv.NamedWindow("rgb", 2)
        # cv.NamedWindow("gray", 2)
        # cv.NamedWindow("thold - gray", 2)
        # cv.NamedWindow("red", 2)
        # cv.NamedWindow("blue", 2)
        # cv.NamedWindow("green", 2)
       
    def callback(self, data):
        # cvimg = cv.QueryFrame(self.capture)

        # result = self.find_tennisball()
        print('In callback')
        # cv.WaitKey(3)
        try:
            msg = self.bridge.cv_to_imgmsg(data, 'bgr8')
            self.img_pub.publish(msg)
        except CvBridgeError, e:
            print e

    # def find_tennisball(self):
    #     """use hough circles to locate tennisball"""
    #     # capture = cv.CaptureFromCAM(-1)
        
    #     while True:
    #         img = cv.QueryFrame(self.capture)
            
    #         ### RGB - show hough on thresholded grayscale ###
    #         rgb = cv.CreateImage(self.size, 8, 3)
    #         cv.Copy(img, rgb)
    #         gray = cv.CreateImage(self.size, 8, 1)
    #         # edges = cv.CreateImage(cv.GetSize(rgb), 8, 1)
    #         cv.CvtColor(rgb, gray, cv.CV_BGR2GRAY)
    #         cv.ShowImage("gray", gray)
    #         cv.Threshold(gray, gray, 205, 255, cv.CV_THRESH_BINARY)
    #         cv.ShowImage("thold - gray", gray)
    #         cv.Smooth(gray, gray, cv.CV_GAUSSIAN, 15, 15)
    #         storage = cv.CreateMat(1, rgb.height * rgb.width, cv.CV_32FC3)
    #         cv.HoughCircles(gray, storage, cv.CV_HOUGH_GRADIENT, \
    #             1, 5, 200, 30, min_radius=0, max_radius=240)
    #         red = cv.CreateImage(self.size, 8, 1)
    #         blu = cv.CreateImage(self.size, 8, 1)
    #         grn = cv.CreateImage(self.size, 8, 1)
    #         cv.Split(rgb, red, blu, grn, None)
    #         cv.ShowImage("red", red)
    #         cv.ShowImage("blue", blu)
    #         cv.ShowImage("green", grn)

    #         for i in range(storage.width - 1):
    #             center = (int(storage[0,i][0]), int(storage[0,i][1]))
    #             radius = int(storage[0,i][2])
    #             cv.Circle(rgb, center, radius, (0, 0, 255), thickness=2)
            
    #         cv.ShowImage("rgb", rgb)

    #         return rgb


def main():
    # print 'hello'
    # cv.NamedWindow("CV Input", 2)
    # capture = cv.CaptureFromCAM(-1)
    br = WebcamBridge()
    rospy.init_node('webcam_bridge')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('Shutting Down')
    # cv.DestroyAllWindows()


if __name__ == '__main__':
    os.system('bash /home/gavlab/devel/ros_package_path.bash')
    # cv.NamedWindow("CV Input", 2)
    main()

# cv.NamedWindow("Fuck", 1)