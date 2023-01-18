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
objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)
frameNum=0;
# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
frames = []  # Frames take from camera
cam = cv.VideoCapture(0)

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
    # Turn image gray
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    # Return chessboard corner locations
    ret, corners = cv.findChessboardCorners(gray, (7, 7), None)
    if ret:  # if corners are returned

        # Create corner objects at corner locations
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

        # Draw and display the corners to original frame
        frame = cv.drawChessboardCorners(frame, (7, 7), corners2, ret)

    # Display the resulting frame
    cv.imshow("Webcam", frame)
    k = cv.waitKey(1)
    if k%256 == 32:  # If space is pressed,
        if ret:  # If corners have been returned

            # Save frame to app folder
            cv.imwrite('calibration_img' + str(frameNum) + 'CameraName' + '.png', gray)
            print("img saved")

            # Add data from current frame to arrays
            objpoints.append(objp)
            imgpoints.append(corners2)

            frameNum = frameNum+1
        else:  # If no corners were returned
            print("Chessboard not detected in image")
    if k%256 == 27:  # If ESC is pressed

        print("Frame collection complete..")
        break

# Use chessboard corners to get camera matrix, distortion coefficients, rotation and translation vectors etc.
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# prepare image for undistortion
ret, frame = cam.read()
h,  w = frame.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    if ret:
        # undistort
        dst = cv.undistort(frame, mtx, dist, None, newcameramtx)
        # crop the image
        x, y, w, h = roi
        dst = dst[y:y + h, x:x + w]
    cv.imshow("Webcam", dst)

    k = cv.waitKey(1)
    if k%256 == 27:
        # ESC pressed
        print("Escape hit, closing...")
        break
cam.release()
cv.destroyAllWindows()