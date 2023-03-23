# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:33:44 2023

@author: lagro
"""
from HoughCirclesClass import *

#cameraNumber,fourcc,width,height,tog_autoF,tog_autoE,exposure,focus,contrast,brightness,fps):
camera1 = CircleDetectionTestModeWindows(0,1280,720,0,0,-3,0.5,75,175,30)

camera1.detectionProgram(1)