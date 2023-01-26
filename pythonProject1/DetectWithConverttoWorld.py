# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:09:48 2022

@author: DanTehMan

Run the program, then press Spacebar to capture frames with a chessboard. Repeat from 20 different positions and angles.
Try to cover a variety of angles from positions that utilize all the space in view of camera
Once finished, press ESC to undistort image.

Programmed for used with 7x7 chessboard. (9x9 including outside ring)

TODO: Create seperate program that get undistort values from saved images
    Apply undistortion to current puck detection program
"""

import cv2 as cv
import numpy as np
import glob


criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
chessh = 7
chessw = 7
calibrationArrays = np.load("CameraArraysCameraName.npz", allow_pickle=True)
print(calibrationArrays.files)
camMtx = calibrationArrays['arr_0']
distMtx = calibrationArrays['arr_1']
rotVec = calibrationArrays['arr_2']
transVec = calibrationArrays['arr_3']
print(camMtx)
print(distMtx)
print(rotVec)
print(transVec)

objp = np.zeros((chessh * chessw, 3), np.float32)
objp[0:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)
frameNum = 0;

# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
frames = []  # Frames take from camera
cam = cv.VideoCapture(0)

am = cv.VideoCapture(0)

if not cam.isOpened():
    print("Cannot open camera")
    exit()
cv.namedWindow("Webcam")

img_counter = 0

while True:
    ret, frame = cam.read()  # Updates frame each camera frame
    if not ret:
        print("failed to grab frame")
        break
    undistortedFrame = cv.undistort(frame, camMtx, distMtx, None)
    gray = cv.cvtColor(undistortedFrame, cv.COLOR_BGR2GRAY)

    # Return chessboard corner locations
    ret, corners = cv.findChessboardCorners(gray, (chessh, chessw), None)

    if ret:  # if corners are returned
        # Create corner objects at corner locations
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        # Draw and display the corners to original frame
        frame = cv.drawChessboardCorners(undistortedFrame, (chessh, chessw), corners2, ret)

    cv.imshow("Webcam", undistortedFrame)

    k = cv.waitKey(1)
    if k % 256 == 32:  # If space is pressed,
        if ret:  # If corners have been returned
            #Use Recover Pose for this part
            imgmtx = [[corners2[0][0][0]],[corners2[0][0][1]]]
            print(imgmtx)


            #print(objpoints)
        else:  # If no corners were returned
            print("Chessboard not detected in image")
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
cam.release()
cv.destroyAllWindows()