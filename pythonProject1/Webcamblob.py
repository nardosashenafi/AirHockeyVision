# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:09:48 2022

@author: DanTehMan
"""

import cv2
import numpy as np

cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Cannot open camera")
    exit()

params = cv2.SimpleBlobDetector_Params()
# Set Area filtering parameters
# Info for Parameters here: https://docs.opencv.org/3.4/d8/da7/structcv_1_1SimpleBlobDetector_1_1Params.html
params.filterByArea = True
params.minArea = 5000
params.maxArea = 20000

# Set Circularity filtering parameters
params.filterByCircularity = False
params.minCircularity = 0.9

# Set Convexity filtering parameters
params.filterByConvexity = True
params.minConvexity = 0.8

# Set Threshold filtering parameters
params.minThreshold = 0.1

# Set inertia filtering parameters
params.filterByInertia = False

params.minInertiaRatio = 0.01
detector = cv2.SimpleBlobDetector_create(params)
cv2.namedWindow("Webcam")

img_counter = 0

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
        # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    keypoints = detector.detect(gray)
    gray_with_keypoints = cv2.drawKeypoints(gray, keypoints, np.array([]), (0, 0, 255),
                                          cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    # Display the resulting frame
    cv2.imshow('Detection', gray_with_keypoints)
    cv2.imshow("Webcam", frame)
    k = cv2.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break

cam.release()
cv2.destroyAllWindows()