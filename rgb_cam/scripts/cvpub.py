#!/usr/bin/env python
"""
defines class for publishing cv images in ros, with the intent that they will be
picked up by the cv_bridge app
"""
__author__ = 'Robert Cofield'

import roslib
roslib.load_manifest('rgb_cam')
import rospy