import numpy as np
import cv2 as cv
import glob

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6 * 8, 3), np.float32)
objp[:, :2] = np.mgrid[0:8, 0:6].T.reshape(-1, 2)
# Arrays to store object points and image points from all the images.
objpoints = []  # 3d point in real world space
imgpoints = []  # 2d points in image plane.
images = glob.glob(r"C:\Users\DanTehMan\Downloads\hockeytabletopdown.jpg")

for fname in images:
    img = cv.imread(fname)
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, (8, 6), None) #
    # If found, add object points, image points (after refining them)
    if ret == True:
        print("Debug: ret true")
        objpoints.append(objp)
        corners2 = cv.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)
        # Draw and display the corners
        cv.drawChessboardCorners(img, (8, 6), corners2, ret)
        cv.namedWindow('img', cv.WINDOW_NORMAL)
        cv.imshow('img', img)
        cv.waitKey(0)
        cv.waitKey(1)
    else:
        print("Debug: ret not found")
        exit()

# Use chessboard corners to get camera matrix, distortion coefficients, rotation and translation vectors etc.
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

# prepare image for undistortion
img = cv.imread(r"C:\Users\DanTehMan\Downloads\hockeytabletopdown.jpg")
h,  w = img.shape[:2]
newcameramtx, roi = cv.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)

# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.namedWindow('undistorted img', cv.WINDOW_NORMAL)
cv.imshow('undistorted img', dst)
cv.waitKey(0)
cv.destroyAllWindows()
cv.waitKey(1)

#M = cv.getPerspectiveTransform(pts1,pts2)
#dst = cv.warpPerspective(img, M, (cols, rows))