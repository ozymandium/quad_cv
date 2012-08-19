#!/usr/bin/env python
"""
basic live rgb camera feed
"""
import cv2.cv as cv

cv.NamedWindow("camera", 2)
capture = cv.CaptureFromCAM(0)

while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("camera", img)
    if cv.WaitKey(10) == 27:
        break