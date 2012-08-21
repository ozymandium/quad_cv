#!/usr/bin/env python
import sys
import cv2.cv as cv

class Webcam(object):
    """
    Class for camera stream
    """
    def __init__(self, device, parent=None):
        self.device = device
        self.capture = cv.CaptureFromCAM(self.device)
        self.size = cv.GetSize(cv.QueryFrame(self.capture))

    def main(self):
        """main loop for displaying desired feeds from the queue"""
        if cv.WaitKey(10) == 27:
            break

    def showRaw(self):
        cv.NamedWindow("Raw Stream", 2)
        cv.


if __name__ == '__main__':
    if len(sys.argv) == 1:
        device = 0
    else:
        device = sys.argv[1]
    cam = Webcam(device)