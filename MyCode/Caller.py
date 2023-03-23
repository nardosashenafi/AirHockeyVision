# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:33:44 2023

@author: lagro
"""
from HoughCirclesClass import *
from threading import Thread

#cameraNumber,width,height,tog_autoF,tog_autoE,exposure,focus,contrast,brightness,fps
camera = CircleDetectionTestModeWindows(0,1280,720,0,0,-3,0.5,75,175,30)    # TODO: extract these variables from a stored file
                                                                            # TODO: these variables will be saved to a file from the GUI

Thread(target = camera.createGUI).start()
Thread(target = camera.detectionProgram(1)).start()
