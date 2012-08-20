#!/usr/bin/env python
__author__ = 'Robert Cofield'
import roslib
roslib.load_manifest('rgb_cam')
import sys
import rospy
import cv2.cv as cv
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class WebcamBridge:
    """
    class for moving webcam images from opencv to ros
    """
    def __init__(self, capture):
        self.image_pub = rospy.Publisher("from_bridge", Image)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("to_bridge", Image, self.callback)

    def callback(self, data):
        cvimg = cv.QueryFrame(capture)
        cv.ShowImage('CV Input', cvimg)
        cv.WaitKey(3)

        try:
            msg = self.bridge.cv_to_imgmsg(cvimg, 'bgr8')
            self.img_pub.publish(msg)
        except CvBridgeError, e:
            print e


def main():
    cv.NamedWindow("CV Input", 2)
    capture = cv.CaptureFromCAM(0)
    br = WebcamBridge(capture)
    rospy.init_node('webcam_bridge')
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print('Shutting Down')
    cv.DestroyAllWindows()


if __name__ == '__main__':
    main()