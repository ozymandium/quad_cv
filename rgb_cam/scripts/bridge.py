#!/usr/bin/env python
"""
Bridge for sending opencv images around. 
designed for use with find_tennisball.py
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
        self.image_pub = rospy.Publisher("from_cv_bridge", Image)
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("to_cv_bridge", Image, self.callback)
        
        rospy.sleep(1)
                    
    def callback(self, data):
        print('In WebcamBridge.callback')
        # cv.WaitKey(3)
        try:
            msg = self.bridge.cv_to_imgmsg(data, 'bgr8')
            self.img_pub.publish(msg)
        except CvBridgeError, e:
            print e


def main():
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