# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:09:48 2022
@author: DanTehMan
Run the program, then press Spacebar to capture frames with a chessboard. Repeat from 20 different positions and angles.
Try to cover a variety of angles from positions that utilize all the space in view of camera
Once finished, press ESC to undistort image.
Programmed for used with 7x7 chessboard.(9x9 including outside ring) # FIXME: This has changed
TODO:
    2.75 cm/85 holes =2.44 cm
    Transform 2D coordinates to 3D
"""
import Calibrationfunc as cf

#camPortNum,gridwidth,startingX,startingY,chessh,chessw,cameraName,camZ
cf.runCalibration(0,3,0,0,14,9,"origindirectfull",139)