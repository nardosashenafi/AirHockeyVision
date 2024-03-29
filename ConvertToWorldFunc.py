import numpy as np
import cv2 as cv

def getCalibrationValues(cameraName):
    """
    Loads CameraArrays_____.npz file
    :param cameraName ***Must be same as Camera Name used in Calibration***
    :return Arrays in files as arrays
    """
    calibrationArrays = np.load("CameraArrays"+cameraName+".npz", allow_pickle=True)
    camMtx = calibrationArrays['arr_0']
    newCamMtx = calibrationArrays['arr_1']
    distMtx = calibrationArrays['arr_2']
    roi = calibrationArrays['arr_3']
    s = calibrationArrays['arr_4']
    extMtx = calibrationArrays['arr_5']
    camZ = calibrationArrays['arr_6']


    return[camMtx,newCamMtx,distMtx,roi,s,extMtx,camZ]

def img2world(x, y, camMtx, extMtx, s, camZ):
    """
    Converts Camera pixel coordinates to Physical coordiantes
    :param x: Camera X Value
    :param y: Camera Y Value
    :param camMtx: from getCalibrationValues()
    :param extMtx: from getCalibrationValues()
    :param s: from getCalibrationValues()
    :param camZ: from getCalibrationValues()
    :return: X,Y,Z coordinates in world coordinates (cm)
    """
    imgMtx = [[s * x], [s * y], [s]]
    imgMtx = np.linalg.multi_dot([np.linalg.inv(camMtx), imgMtx])  # Double check 3x1.
    imgMtx = np.delete(imgMtx,2,0)
    #temp
    #camZ = 139
    #extMtx[3][2] = -139
    extMtx[3][2] = -camZ

    imgMtx = np.vstack([imgMtx,camZ, [1]])
    objpos = np.linalg.multi_dot([np.linalg.inv(extMtx), imgMtx])
    objpos = objpos/objpos[[3][0]]
    # Normal to plane is 139cm
    # Horizontal (y) offset to 00 is 24cm
    # x offset is 0 cm
    return [objpos,imgMtx]

def deWarp(frame,camMtx,distMtx,newCamMtx,roi):
    """
    Dewarps image using Intrinsic Camera Parameters
    :param frame: webcam image frame (unprocessed)
    :param camMtx: from getCalibrationValues()
    :param distMtx: from getCalibrationValues()
    :param newCamMtx: from getCalibrationValues()
    :return: Dewarped Frame (can be processed with Monochrome, Blur, etc...)
    """
    #Comment out if having Calibration issues..
    undistortedFrame = cv.undistort(frame, camMtx, distMtx, None, newCamMtx)
    x, y, w, h = roi
    #undistortedFrame = undistortedFrame[y:y + h, x:x + w]

    return undistortedFrame