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
		# TODO: have these variables passed in from Caller.py
		camera.blur = 17
		camera.dp = 1.2
		camera.minDist = 10000
		camera.minRadius = 5
		camera.maxRadius = 50
		camera.circleSensitivity = 100
		camera.circleEdgePoints = 40
		camera.saturation = 125
		camera.hue = 0
		camera.gain = 10

		camera.fourcc = cv.VideoWriter_fourcc('M','J','P','G')	# four character code for video encoding
		camera.videoCapture = cv.VideoCapture(camera.cameraNumber, cv.CAP_DSHOW)	# Set port number for camera (DSHOW → DirectShow)
        
	def detectionProgram(camera, testMode):
		criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001) 	# NOT USED
		# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)		# NOT USED
		chessh = 7																	# NOT USED
		chessw = 9																	# NOT USED
		[camMtx, newCamMtx, distMtx, roi, s, extMtx, camZ] = ctw.getCalibrationValues("origindirectfull")

		# Arrays to store object points and image points from all the images. 		# NOT USED
		frames = []  # Frames take from camera										# NOT USED

		if testMode:
			print("\nParameters BEFORE assignment: ")
			print(f"WIDTH: {camera.videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)}")
			print(f"HEIGHT: {camera.videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)}")
			print(f"FPS: {camera.videoCapture.get(cv.CAP_PROP_FPS)}")
			print(f"FOURCC: {camera.videoCapture.get(cv.CAP_PROP_FOURCC)}")
        
		camera.videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, camera.width)	# Set camera frame width
		camera.videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, camera.height)	# Set camera frame height
		camera.videoCapture.set(cv.CAP_PROP_AUTOFOCUS,camera.tog_autoF)	# Set camera autofocus
		camera.videoCapture.set(cv.CAP_PROP_AUTO_EXPOSURE, camera.tog_autoE)	# Set camera autoexposure
		camera.videoCapture.set(cv.CAP_PROP_EXPOSURE, camera.exposure)	# Set camera exposure
		camera.videoCapture.set(cv.CAP_PROP_CONTRAST, camera.contrast)	# Set camera contrast
		camera.videoCapture.set(cv.CAP_PROP_BRIGHTNESS,camera.brightness)	# Set camera brightness
		camera.videoCapture.set(cv.CAP_PROP_FOCUS, camera.focus) 	# Set camera focus
		camera.videoCapture.set(cv.CAP_PROP_FPS, camera.fps)	# Set camera fps
		camera.videoCapture.set(cv.CAP_PROP_FOURCC,camera.fourcc)	# Set camera compression format

		if testMode:
			print("\nParameters AFTER assignment: ")
			print(f"WIDTH: {camera.videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)}")
			print(f"HEIGHT: {camera.videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)}")
			print(f"FPS: {camera.videoCapture.get(cv.CAP_PROP_FPS)}")
			print(f"FOURCC: {camera.videoCapture.get(cv.CAP_PROP_FOURCC)}")
			print(f"Settings {camera.videoCapture.get(cv.CAP_PROP_SETTINGS)}")
            
		prevCircle = None	# Circle from the previous frame (will represent the current detected circle)
		dist = lambda x1, y1, x2, y2: math.dist([x1, x2], [y1, y2])	# Calculate the square of the distance between two points in a frame
		runtime = 0	# Runtime of individual loop (each frame)
		runtime_counter = 0	# Total runtime of all loops added up
		start_time = 0	# Starting time of each loop
		frame_counter = 0	# Total number of frames detected by the program during runtime
		circle_counter = 0	# Total number of circles detected by the program during runtime
        
		while True:
			start_time = t.perf_counter()	# Time how long the loop will take to run
	    
			ret, frame = camera.videoCapture.read()	# ret is a boolean: was it able to capture the frame successfully
			if not ret: break	# If frame is not read successfully, end program
	    
			frame_counter += 1	# Frame is read successfully, so increment frame counter

			undistortedFrame = ctw.deWarp(frame, camMtx, distMtx, newCamMtx, roi)
			grayFrame = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)	# Make a copy of frame where the color has been converted to grayscale
			blurFrame = cv.GaussianBlur(grayFrame,(camera.blur,camera.blur),0)	# Make a copy of grayFrame where the frame has been blurred
            
			circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT,camera.dp , camera.minDist, 			# Find circles within the frame given these parameters
                                     param1 = camera.circleSensitivity, param2 = camera.circleEdgePoints,
									 minRadius=camera.minRadius, maxRadius=camera.maxRadius)	# The result will be a list of circles found
			if circles is not None:	# Are there circles detected in the frame
				circles = np.uint16(np.around(circles))	# Convert circles to a numpy array
				chosen = None   # Chosen circle from the frame
				for i in circles[0,:]:	# Iterate through array of circles
					if chosen is None:	# If there is no circle chosen yet,
						chosen = i		# set the chosen circle equal to the first circle in the array
					if prevCircle is not None:	# Is there is a current circle stored
						if (dist(chosen[0],chosen[1],prevCircle[0],prevCircle[1])\
	  							<= dist(i[0],i[1],prevCircle[0],prevCircle[1])):
							chosen = i	# set the chosen circle equal to the next circle in the array
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
				cv.imshow("circles", frame)	# Show the original frame with the drawn circles to the user
				cv.imshow("CameraVision", undistortedFrame) # Show the calibrated frame to the user
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
		camera.videoCapture.release()	# Release webcam and close all windows
		cv.destroyAllWindows()	# Close all OpenCV windows (does not close the GUI)
		sys.exit()	# Terminate the program
        
	def getCoords(camera):			# NOT USED
		return camera.coordinates	# NOT USED
	
	def createGUI(camera):
		customtkinter.set_appearance_mode('System')
		customtkinter.set_default_color_theme('blue')

		root = customtkinter.CTk()
		root.title('Light/Camera Settings')
		#root.iconbitmap('AirHockeyIcon.ico')
		#root.geometry('1366x768')
		#root.resizable(0,0)

		algorithmFrame = customtkinter.CTkFrame(master=root)
		algorithmFrame.grid(row=0,column=0,padx=50,pady=50)

		cameraFrame = customtkinter.CTkFrame(master=root)
		cameraFrame.grid(row=0,column=1,padx=50,pady=50)

		buttonFrame = customtkinter.CTkFrame(master=root)
		buttonFrame.grid(row=1,column=0,padx=50,pady=50)

		## Definitions for updating value in GUI and variables
		def setBlurLevel(value):
			camera.blur = int(value)
			blurLevel_label_value.configure(text=camera.blur)

		def setDp(value):
			camera.dp = round(value, 1)
			dp_label_value.configure(text=camera.dp)

		def setMinDist(value):
			camera.minDist = int(value)
			minDist_label_value.configure(text=camera.minDist)

		def setMinRadius(value):
			camera.minRadius = int(value)
			minRadius_label_value.configure(text=camera.minRadius)

		def setMaxRadius(value):
			camera.maxRadius = int(value)
			maxRadius_label_value.configure(text=camera.maxRadius)

		def setCircleSensitivity(value):
			camera.circleSensitivity = int(value)
			circleSensitivity_label_value.configure(text=camera.circleSensitivity)

		def setCircleEdgePoints(value):
			camera.circleEdgePoints = int(value)
			circleEdgePoints_label_value.configure(text=camera.circleEdgePoints)

		def setBrightness(value):
			camera.brightness = int(value)
			camera.videoCapture.set(cv.CAP_PROP_BRIGHTNESS, camera.brightness)
			cameraBrightness_label_value.configure(text=camera.brightness)

		def setContrast(value):
			camera.contrast = int(value)
			camera.videoCapture.set(cv.CAP_PROP_CONTRAST, camera.contrast)
			cameraContrast_label_value.configure(text=camera.contrast)

		def setSaturation(value):
			camera.saturation = int(value)
			camera.videoCapture.set(cv.CAP_PROP_SATURATION, camera.saturation)
			cameraSaturation_label_value.configure(text=camera.saturation)

		def setHue(value):
			camera.hue = int(value)
			camera.videoCapture.set(cv.CAP_PROP_HUE, camera.hue)
			cameraHue_label_value.configure(text=camera.hue)

		def setGain(value):
			camera.gain = int(value)
			camera.videoCapture.set(cv.CAP_PROP_GAIN, camera.gain)
			cameraGain_label_value.configure(text=camera.gain)

		def setExposure(value):
			camera.exposure = int(value)
			camera.videoCapture.set(cv.CAP_PROP_EXPOSURE, camera.exposure)
			cameraExposure_label_value.configure(text=camera.exposure)

		def setAutoExposure(value):
			camera.tog_autoE = int(value)
			camera.videoCapture.set(cv.CAP_PROP_AUTO_EXPOSURE, camera.tog_autoE)
			cameraAutoExposure_label_value.configure(text=camera.tog_autoE)

		def setAutoFocus(value):
			camera.tog_autoF = int(value)
			camera.videoCapture.set(cv.CAP_PROP_AUTOFOCUS, camera.tog_autoF)
			cameraAutoFocus_label_value.configure(text=camera.tog_autoF)

		## Sliders for circle detecting algorithm
		# Blur level of frame
		blurLevel_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="Blur", font=('Arial', 22))
		blurLevel_label.grid(row=0, column=0, pady=10, padx=10)
		blurLevel_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=55, width=400, number_of_steps=27,
			border_width=3, command=setBlurLevel)
		blurLevel_slider.set(camera.blur)
		blurLevel_slider.grid(row=0, column=1, pady=10, padx=10)
		blurLevel_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.blur, font=('Arial', 22))
		blurLevel_label_value.grid(row=0, column=2, pady=10, padx=10)	

		# dp inverse ratio of resolution
		dp_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="dp", font=('Arial', 22))
		dp_label.grid(row=1, column=0, pady=10, padx=10)
		dp_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=5, width=400, number_of_steps=80,
			border_width=3, command=setDp)
		dp_slider.set(camera.dp)
		dp_slider.grid(row=1, column=1, pady=10, padx=10)
		dp_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.dp, font=('Arial', 22))
		dp_label_value.grid(row=1, column=2, pady=10, padx=10)
		
		# Minimum distance between circles
		minDist_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="MinDist", font=('Arial', 22))
		minDist_label.grid(row=2, column=0, pady=10, padx=10)
		minDist_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=100, width=400, number_of_steps=999,
			border_width=3, command=setMinDist)
		minDist_slider.set(camera.minDist)
		minDist_slider.grid(row=2, column=1, pady=10, padx=10)
		minDist_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.minDist, font=('Arial', 22))
		minDist_label_value.grid(row=2, column=2, pady=10, padx=10)

		# Minimum radius of circle
		minRadius_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="MinRadius", font=('Arial', 22))
		minRadius_label.grid(row=3, column=0, pady=10, padx=10)
		minRadius_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=200, width=400, number_of_steps=199,
			border_width=3, command=setMinRadius)
		minRadius_slider.set(camera.minRadius)
		minRadius_slider.grid(row=3, column=1, pady=10, padx=10)
		minRadius_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.minRadius, font=('Arial', 22))
		minRadius_label_value.grid(row=3, column=2, pady=10, padx=10)

		# Maximum radius of circle
		maxRadius_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="MaxRadius", font=('Arial', 22))
		maxRadius_label.grid(row=4, column=0, pady=10, padx=10)
		maxRadius_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=400, width=400, number_of_steps=399,
			border_width=3, command=setMaxRadius)
		maxRadius_slider.set(camera.maxRadius)
		maxRadius_slider.grid(row=4, column=1, pady=10, padx=10)
		maxRadius_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.maxRadius, font=('Arial', 22))
		maxRadius_label_value.grid(row=4, column=2, pady=10, padx=10)

		# Sensitivity to circle detection
		circleSensitivity_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="Circle Sensitivity", font=('Arial', 22))
		circleSensitivity_label.grid(row=5, column=0, pady=10, padx=10)
		circleSensitivity_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=200, width=400, number_of_steps=199,
			border_width=3, command=setCircleSensitivity)
		circleSensitivity_slider.set(camera.circleSensitivity)
		circleSensitivity_slider.grid(row=5, column=1, pady=10, padx=10)
		circleSensitivity_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.circleSensitivity, font=('Arial', 22))
		circleSensitivity_label_value.grid(row=5, column=2, pady=10, padx=10)

		# Minimum # of edge points to declare a circle
		circleEdgePoints_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="# of edge points", font=('Arial', 22))
		circleEdgePoints_label.grid(row=6, column=0, pady=10, padx=10)
		circleEdgePoints_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=4, to=100, width=400, number_of_steps=96,
			border_width=3, command=setCircleEdgePoints)
		circleEdgePoints_slider.set(camera.circleEdgePoints)
		circleEdgePoints_slider.grid(row=6, column=1, pady=10, padx=10)
		circleEdgePoints_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.circleEdgePoints, font=('Arial', 22))
		circleEdgePoints_label_value.grid(row=6, column=2, pady=10, padx=10)

		## Sliders for camera settings
		# Brightness of capture
		cameraBrightness_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Brightness", font=('Arial', 22))
		cameraBrightness_label.grid(row=0, column=3, pady=10, padx=10)
		cameraBrightness_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
			border_width=3, command=setBrightness)
		cameraBrightness_slider.set(camera.brightness)
		cameraBrightness_slider.grid(row=0, column=4, pady=10, padx=10)
		cameraBrightness_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.brightness, font=('Arial', 22))
		cameraBrightness_label_value.grid(row=0, column=5, pady=10, padx=10)

		# Contrast of capture
		cameraContrast_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Contrast", font=('Arial', 22))
		cameraContrast_label.grid(row=1, column=3, pady=10, padx=10)
		cameraContrast_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
			border_width=3, command=setContrast)
		cameraContrast_slider.set(camera.contrast)
		cameraContrast_slider.grid(row=1, column=4, pady=10, padx=10)
		cameraContrast_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.contrast, font=('Arial', 22))
		cameraContrast_label_value.grid(row=1, column=5, pady=10, padx=10)
		
		# Saturation of capture
		cameraSaturation_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Saturation", font=('Arial', 22))
		cameraSaturation_label.grid(row=2, column=3, pady=10, padx=10)
		cameraSaturation_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
			border_width=3, command=setSaturation)
		cameraSaturation_slider.set(camera.saturation)
		cameraSaturation_slider.grid(row=2, column=4, pady=10, padx=10)
		cameraSaturation_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.saturation, font=('Arial', 22))
		cameraSaturation_label_value.grid(row=2, column=5, pady=10, padx=10)

		# Hue of capture (not applicable to my camera?)
		cameraHue_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Hue", font=('Arial', 22))
		cameraHue_label.grid(row=3, column=3, pady=10, padx=10)
		cameraHue_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
			border_width=3, command=setHue)
		cameraHue_slider.set(camera.hue)
		cameraHue_slider.grid(row=3, column=4, pady=10, padx=10)
		cameraHue_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.hue, font=('Arial', 22))
		cameraHue_label_value.grid(row=3, column=5, pady=10, padx=10)
		

		# Gain of capture
		cameraGain_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Gain", font=('Arial', 22))
		cameraGain_label.grid(row=4, column=3, pady=10, padx=10)
		cameraGain_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
			border_width=3, command=setGain)
		cameraGain_slider.set(camera.gain)
		cameraGain_slider.grid(row=4, column=4, pady=10, padx=10)
		cameraGain_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.gain, font=('Arial', 22))
		cameraGain_label_value.grid(row=4, column=5, pady=10, padx=10)

		# Exposure of capture (not applicable to my camera?)
		cameraExposure_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Exposure", font=('Arial', 22))
		cameraExposure_label.grid(row=5, column=3, pady=10, padx=10)
		cameraExposure_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=-11, to=-1, width=400, number_of_steps=10,
			border_width=3, command=setExposure)
		cameraExposure_slider.set(camera.exposure)
		cameraExposure_slider.grid(row=5, column=4, pady=10, padx=10)
		cameraExposure_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.exposure, font=('Arial', 22))
		cameraExposure_label_value.grid(row=5, column=5, pady=10, padx=10)

		# Auto Exposure of capture
		cameraExposure_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Auto Exposure", font=('Arial', 22))
		cameraExposure_label.grid(row=6, column=3, pady=10, padx=10)
		cameraExposure_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=1, width=400, number_of_steps=1,
			border_width=3, command=setAutoExposure)
		cameraExposure_slider.set(camera.tog_autoE)
		cameraExposure_slider.grid(row=6, column=4, pady=10, padx=10)
		cameraAutoExposure_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.tog_autoE, font=('Arial', 22))
		cameraAutoExposure_label_value.grid(row=6, column=5, pady=10, padx=10)

		# Auto Focus of capture
		cameraExposure_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Auto Focus", font=('Arial', 22))
		cameraExposure_label.grid(row=7, column=3, pady=10, padx=10)
		cameraExposure_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=1, width=400, number_of_steps=1,
			border_width=3, command=setAutoFocus)
		cameraExposure_slider.set(camera.tog_autoF)
		cameraExposure_slider.grid(row=7, column=4, pady=10, padx=10)
		cameraAutoFocus_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.tog_autoF, font=('Arial', 22))
		cameraAutoFocus_label_value.grid(row=7, column=5, pady=10, padx=10)

		# Buttons
		customtkinter.CTkButton(
			master=buttonFrame, text='Quit', command=root.quit).grid(
				row=7, column=1, pady=10, padx=10)
		
		root.mainloop()