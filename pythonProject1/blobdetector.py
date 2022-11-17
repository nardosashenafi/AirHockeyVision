# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:21:51 2022

@author: DanTehMan
"""

# Standard imports
import cv2
import numpy as np;

# Read image
im = cv2.imread("blobs.jpg", cv2.IMREAD_GRAYSCALE)

cv2.imshow('Image', im)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create()

# Detect blobs.
keypoints = detector.detect(im)

# Draw detected blobs as red circles.
# cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255),
                                      cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints", im_with_keypoints)
cv2.waitKey(0)
cv2.destroyAllWindows()
cv2.waitKey(1)
