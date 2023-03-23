# -*- coding: utf-8 -*-
import time as t
import cv2 as cv
import numpy as np
import math
import sys
import customtkinter
import ConvertToWorldFunc as ctw

class CircleDetectionTestModeWindows():
	def __init__(camera,cameraNumber,width,height,tog_autoF,tog_autoE,exposure,focus,contrast,brightness,fps):
		camera.cameraNumber = cameraNumber	# Serial port for camera
		camera.width = width	# Width of frame for capture
		camera.height = height	# Height of frame for capture
		camera.tog_autoF = tog_autoF	# Toggle autofocus of capture
		camera.tog_autoE = tog_autoE	# Toggle autoexposure of capture
		camera.exposure = exposure	# Exposure of capture
		camera.focus = focus	# Focus of capture
		camera.contrast = contrast	# Contrast of capture
		camera.brightness = brightness	# Brightness of capture
		camera.fps = fps	# Framerate of capture
        
	def detectionProgram(camera, testMode):
		criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
		# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
		chessh = 7
		chessw = 9
		[camMtx, newCamMtx, distMtx, roi, s, extMtx, camZ] = ctw.getCalibrationValues("origindirectfull")

		# Arrays to store object points and image points from all the images.
		frames = []  # Frames take from camera

		fourcc = cv.VideoWriter_fourcc('M','J','P','G')	# four character code for video encoding
		videoCapture = cv.VideoCapture(camera.cameraNumber, cv.CAP_DSHOW)

		if testMode:
			print("\nParameters BEFORE assignment: ")
			print(f"WIDTH: {videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)}")
			print(f"HEIGHT: {videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)}")
			print(f"FPS: {videoCapture.get(cv.CAP_PROP_FPS)}")
			print(f"FOURCC: {videoCapture.get(cv.CAP_PROP_FOURCC)}")
        
		videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, camera.width)
		videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, camera.height)
		videoCapture.set(cv.CAP_PROP_AUTOFOCUS,camera.tog_autoF)
		videoCapture.set(cv.CAP_PROP_AUTO_EXPOSURE, camera.tog_autoE)
		videoCapture.set(cv.CAP_PROP_EXPOSURE, camera.exposure)
		videoCapture.set(cv.CAP_PROP_CONTRAST, camera.contrast)
		videoCapture.set(cv.CAP_PROP_BRIGHTNESS,camera.brightness)
		videoCapture.set(cv.CAP_PROP_FOCUS, camera.focus) 
		videoCapture.set(cv.CAP_PROP_FPS, camera.fps)
		videoCapture.set(cv.CAP_PROP_FOURCC,fourcc)

		if testMode:
			print("\nParameters AFTER assignment: ")
			print(f"WIDTH: {videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)}")
			print(f"HEIGHT: {videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)}")
			print(f"FPS: {videoCapture.get(cv.CAP_PROP_FPS)}")
			print(f"FOURCC: {videoCapture.get(cv.CAP_PROP_FOURCC)}")
			print(f"Settings {videoCapture.get(cv.CAP_PROP_SETTINGS)}")
            
		prevCircle = None	# Circle from the previous frame (will represent the current detected circle)
		dist = lambda x1, y1, x2, y2: math.dist([x1, x2], [y1, y2])	# Calculate the square of the distance between two points in a frame
		runtime = 0	# Runtime of individual loop (each frame)
		runtime_counter = 0	# Total runtime of all loops added up
		start_time =0	# Starting time of each loop
		frame_counter =0	# Total number of frames detected by the program during runtime
		circle_counter =0	# Total number of circles detected by the program during runtime
        
		while True:
			start_time = t.perf_counter()	# Time how long the loop will take to run
	    
			ret, frame = videoCapture.read()	# ret is a boolean: was it able to capture the frame successfully
			if not ret: print("Couldn't read frame\n");break	# If frame is not read successfully, end program
	    
			frame_counter += 1	# Frame is read successfully, so increment frame counter

			undistortedFrame = ctw.deWarp(frame, camMtx, distMtx, newCamMtx, roi)
			grayFrame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)	# Make a copy of frame where the color has been converted to grayscale
			blurFrame = cv.GaussianBlur(grayFrame,(17,17),0)	# Make a copy of grayFrame where the frame has been blurred
            
			circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT,1.2 , 10000, 			# Find circles within the frame given these parameters
                                     param1 = 100, param2 = 40, minRadius=10, maxRadius=28)	# The result will be a list of circles found
			if circles is not None:	# Are there circles detected in the frame
				circles = np.uint16(np.around(circles))	# Convert circles to a numpy array
				chosen = None   # Chosen circle from the frame
				for i in circles[0,:]:	# Iterate through array of circles
					if chosen is None:	# If there is no circle chosen yet,
						chosen = i		# set the chosen circle equal to the first circle in the array
					if prevCircle is not None:	# Is there is a current circle stored
						if (dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])\
	  							<= dist(i[0],i[1],prevCircle[0],prevCircle[1])):
							chosen = i
							camera.coordinates = (chosen[0], chosen[1], chosen[2]) # I think chosen[0] is the radius so it can be ommited 
							#TODO: publish ros topic
						[objpos,imgMtx] = ctw.img2world(chosen[0],chosen[1],camMtx,extMtx,s,camZ)
					cv.circle(frame, (chosen[0], chosen[1]), 1, (0,0,255), 3)	# Draw a circle at the centerpoint of the chosen circle
					cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,0), 3)	# Draw a circle around the circumference of the chosen circle
					prevCircle = chosen	# Set the previous circle equal to the chosen circle at the end of the loop
                   
					circle_counter += 1	# Circle is drawn, so increment circle counter
			runtime = t.perf_counter() - start_time 	# Time how long the loop took to run
			runtime_counter += runtime	# Get a total runtime of all loops
			framerate = frame_counter / runtime_counter	# Calculate framerate

			if cv.waitKey(1)  == 32:
				print(f'Chosen[0]: {chosen[0]} Chosen[1]:', end=' ')
				print(f'{chosen[1]} Chosen[2]: {chosen[2]}')
				print(f'Image Matrix: {imgMtx}')
				print(f'Object Position: {objpos}')

			if testMode:
				cv.imshow("circles",frame)	# Show the original frame with the drawn circles to the user
				cv.imshow("CameraVision",undistortedFrame)
			if cv.waitKey(1) & 0xFF == ord('q'):	# Quit program if user presses the 'q' key while in the imshow window
				if testMode:
					print(f"Total Runtime: {runtime_counter:.3f} seconds")
					print(f"Total Frames: {frame_counter:.0f}")
					print(f"FPS: {framerate:.3f}")
					if circle_counter != 0:
						print(f"Processing speed {(runtime_counter/circle_counter):.3f} seconds")
					if frame_counter != 0:
						print(f"Accuracy: {(100*(circle_counter/frame_counter)):.3f}%")
				break
		videoCapture.release()	# Release webcam and close all windows
		cv.destroyAllWindows()	# Close all OpenCV windows (does not close the GUI)
		sys.exit()	# Terminate the program
        
	def getCoords(camera):
		return camera.coordinates