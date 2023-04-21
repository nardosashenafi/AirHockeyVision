# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 10:33:44 2023

@author: lagro
"""
from HoughCirclesClass import *
from threading import Thread
import time as t

def startup():
	#camera,cameraNumber,width,height,tog_autoF,tog_autoE,exposure,focus,contrast,brightness,fps,blur,dp,minDist,minRadius,maxRadius,circleSensitivity,circleEdgePoints,saturation,hue,gain
	camera = CircleDetectionTestModeWindows(0,1280,720,0,0,-7,255,75,175,60,17,1.2,10000,5,50,100,40,125,0,10)

	mode = 1 # 0 - run mode, 1 - test mode
	Thread(target = camera.createGUI).start()
	redo = camera.detectionProgram(mode)

	if redo:
		print("Program is going to restart")
		#t.sleep(10)
		#restart(camera.newParams, mode)

def restart(newParams, mode):
	#camera,cameraNumber,width,height,tog_autoF,tog_autoE,exposure,focus,contrast,brightness,fps,blur,dp,minDist,minRadius,maxRadius,circleSensitivity,circleEdgePoints,saturation,hue,gain
	camera2 = CircleDetectionTestModeWindows(newParams[0],newParams[1],newParams[2],newParams[3],newParams[4],newParams[5],newParams[6],newParams[7],newParams[8],newParams[9],newParams[10],newParams[11],newParams[12],newParams[13],newParams[14],newParams[15],newParams[16],newParams[17],newParams[18],newParams[19])

	Thread(target = camera2.createGUI).start()
	camera2.detectionProgram(mode)


def main():
	startup()

if __name__ == "__main__":
	main()
