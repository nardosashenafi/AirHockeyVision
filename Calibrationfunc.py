# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:09:48 2022
@author: DanTehMan
Saves a files with all necassary files to perform function in ConvertToWorldFunc
Run the program, then press Spacebar to capture frames with a chessboard. Repeat from 20 different positions and angles.
Try to cover a variety of angles from positions that utilize all the space in view of camera
Once finished, press ESC to undistort image.
"""
def runCalibration(camPortNum,gridwidth,startingX,startingY,chessh,chessw,cameraName,camZ):
    """
    See Documentation for instructios
    :param gridwidth: Default 2.44 (cm)
    :param startingX: Default 0 (measured in holes from 0,0 hole)
    :param startingY: Default 0 (measured in holes from 0,0 hole)
    :param chessh: Default 14
    :param chessw: Default 9
    :param cameraName: ***Used in filename***
    :param camZ:  Measured by hand, distance from camera to startingX,startingY location (cm)
    :return:
    """
    import cv2 as cv
    import numpy as np

    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    objp = np.zeros((chessh * chessw, 3), np.float32)
    objp[0:, :2] = np.mgrid[startingX:startingX+chessh, startingY:startingY+chessw].T.reshape(-1, 2)
    objp = objp*gridwidth
    #print(objp)
    #s is solved for later
    s = 0

    #Enter different values for calibCornerLocation based on known location available region
    #This value uses the holes distance
    calibCornerLocation = [[startingX*2.44],[startingY*2.44],[1],[1]]

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d point in real world space
    imgpoints = []  # 2d points in image plane.
    frames = []  # Frames taken from camera
    cam = cv.VideoCapture(camPortNum,cv.CAP_DSHOW)

    #TODO: Edit this to match GUI settings (the 1280 and 720 params)
    cam.set(cv.CAP_PROP_FRAME_WIDTH, 1280)  # Set camera frame width
    cam.set(cv.CAP_PROP_FRAME_HEIGHT, 720)  # Set camera frame height

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
        ret, corners = cv.findChessboardCorners(gray, (chessh, chessw), None)
        if ret:  # if corners are returned
            # Create corner objects at corner locations
            corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)

            # Draw and display the corners to original frame
            frame = cv.drawChessboardCorners(frame, (chessh, chessw), corners2, ret)

        # Display the resulting frame
        cv.imshow("Webcam", frame)
        k = cv.waitKey(1)
        if k%256 == 32:  # If space is pressed,
            if ret:  # If corners have been returned
                # Add data from current frame to arrays
                objpoints.append(objp)
                #print(objpoints)
                imgpoints.append(corners2)
                print("Image Taken")

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
            cameramtx=mtx
            # crop the image
            x, y, w, h = roi
            dst = dst[y:y + h, x:x + w]
        cv.imshow("Webcam", dst)

        k = cv.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("Escape hit, closing...")
            uv1 = [[corners2[0][0][0]],[corners2[0][0][1]],[1]]

            rotMtx, m = cv.Rodrigues(rvecs[-1])
            transVec = tvecs[-1]
            extMtx1 = [[rotMtx[0][0], rotMtx[0][1], rotMtx[0][2], transVec[0][0]],
                      [rotMtx[1][0], rotMtx[1][1], rotMtx[1][2], transVec[1][0]],
                      [rotMtx[2][0], rotMtx[2][1], rotMtx[2][2], transVec[2][0]]]

            extMtx2 = [[rotMtx[0][0], rotMtx[0][1], rotMtx[0][2], transVec[0][0]],
                       [rotMtx[1][0], rotMtx[1][1], rotMtx[1][2], transVec[1][0]],
                       [rotMtx[2][0], rotMtx[2][1], rotMtx[2][2], transVec[2][0]],
                       [0, 0, 0, 1]]
            rightSide = np.linalg.multi_dot([newcameramtx, extMtx1, calibCornerLocation])
            s = camZ

            np.savez("CameraArrays" +cameraName, cameramtx, newcameramtx, dist, roi, s, extMtx2, camZ)
            break
    cam.release()
    cv.destroyAllWindows()