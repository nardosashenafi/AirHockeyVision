# -*- coding: utf-8 -*-
import time as t
import cv2 as cv
import numpy as np
import math
import os
import sys
import customtkinter
import ConvertToWorldFunc as ctw
import Calibrationfunc as cf

from threading import Thread

class CircleDetectionTestModeWindows():
	def getCoords(camera):			# NOT USED
		return camera.coordinates	# NOT USED

	def __init__(camera,cameraNumber,width,height,tog_autoF,tog_autoE,exposure,focus,contrast,brightness,fps,blur,dp,minDist,minRadius,maxRadius,circleSensitivity,circleEdgePoints,saturation,hue,gain):
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
		camera.saturation = saturation # Saturation of capture
		camera.hue = hue # Hue of capture
		camera.gain = gain # Gain of capture
		camera.blur = blur # Blur level of Gaussian filter
		camera.dp = dp # Inverse ratio of resolution of capture
		camera.minDist = minDist # minimum distance between circles
		camera.minRadius = minRadius # minimum radius of circle to be detected
		camera.maxRadius = maxRadius # maximum radius of circle to be detected
		camera.circleSensitivity = circleSensitivity # sensitivity of circles to be detected
		camera.circleEdgePoints = circleEdgePoints # number of edge points necessary to declare a circle


		camera.fourcc = cv.VideoWriter_fourcc('M','J','P','G')	# four character code for video encoding
		camera.videoCapture = cv.VideoCapture(camera.cameraNumber, cv.CAP_DSHOW)	# Set port number for camera (DSHOW → DirectShow)
        
	def detectionProgram(camera, testMode):
		#[camMtx, newCamMtx, distMtx, roi, s, extMtx, camZ] = ctw.getCalibrationValues("origindirectfull")

		def fourccTranslator(fourccDec):
			if(fourccDec == 844715353):
				return 'YUY2'
			elif(fourccDec == 1196444237):
				return 'MJPG'
			else:
				return (f'{fourccDec} not recognized')
		
		if testMode:
			print("\nParameters BEFORE assignment: ")
			print(f"WIDTH: {camera.videoCapture.get(cv.CAP_PROP_FRAME_WIDTH)}")
			print(f"HEIGHT: {camera.videoCapture.get(cv.CAP_PROP_FRAME_HEIGHT)}")
			print(f"FPS: {camera.videoCapture.get(cv.CAP_PROP_FPS)}")
			print(f"FOURCC: {fourccTranslator(camera.videoCapture.get(cv.CAP_PROP_FOURCC))}")
        
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
			print(f"FPS: {round(camera.videoCapture.get(cv.CAP_PROP_FPS),1)}")
			print(f"FOURCC: {fourccTranslator(camera.videoCapture.get(cv.CAP_PROP_FOURCC))}")
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

			#undistortedFrame = ctw.deWarp(frame, camMtx, distMtx, newCamMtx, roi)
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
						#[objpos,imgMtx] = ctw.img2world(chosen[0],chosen[1],camMtx,extMtx,s,camZ)
					cv.circle(frame, (chosen[0], chosen[1]), 1, (0,0,255), 3)	# Draw a circle at the centerpoint of the chosen circle
					cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255,0,0), 3)	# Draw a circle around the circumference of the chosen circle
					
					prevCircle = chosen	# Set the previous circle equal to the chosen circle at the end of the loop
					circle_counter += 1	# Circle is drawn, so increment circle counter

			runtime = t.perf_counter() - start_time 	# Time how long the loop took to run
			runtime_counter += runtime	# Get a total runtime of all loops
			framerate = frame_counter / runtime_counter	# Calculate framerate

			if cv.waitKey(1) == 32:
				print(f'Chosen[0]: {chosen[0]} Chosen[1]:', end=' ')
				print(f'{chosen[1]} Chosen[2]: {chosen[2]}')
				print(f'Image Matrix: {imgMtx}')
				print(f'Object Position: {objpos}')

			if testMode:
				cv.imshow("circles", frame)	# Show the original frame with the drawn circles to the user
				#cv.imshow("CameraVision", undistortedFrame) # Show the calibrated frame to the user
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
	
	def createGUI(camera):
		customtkinter.set_appearance_mode('System')
		customtkinter.set_default_color_theme('blue')

		root = customtkinter.CTk()
		root.title('Program Settings')
		root.iconbitmap('./AirHockeyIcon.ico')
		#root.geometry('1438x900')
		root.resizable(1,1)

		algorithmFrame = customtkinter.CTkFrame(master=root)
		algorithmFrame.grid(row=0,column=0,padx=10,pady=10)

		cameraFrame = customtkinter.CTkFrame(master=root)
		cameraFrame.grid(row=0,column=1,padx=10,pady=10)

		calibrationFrame = customtkinter.CTkFrame(master=root)
		calibrationFrame.grid(row=1,column=0,padx=10,pady=10)

		buttonFrame = customtkinter.CTkFrame(master=root)
		buttonFrame.grid(row=1,column=1,padx=10,pady=10)

		## Definitions for updating value in GUI and variables
		def setBlurLevel(value):
			camera.blur = int(value)
			blurLevel_slider.set(camera.blur)
			blurLevel_label_value.configure(text=camera.blur)

		def setDp(value):
			camera.dp = round(float(value), 1)
			dp_slider.set(camera.dp)
			dp_label_value.configure(text=camera.dp)

		def setMinDist(value):
			camera.minDist = int(value)
			minDist_slider.set(camera.minDist)
			minDist_label_value.configure(text=camera.minDist)

		def setMinRadius(value):
			camera.minRadius = int(value)
			minRadius_slider.set(camera.minRadius)
			minRadius_label_value.configure(text=camera.minRadius)

		def setMaxRadius(value):
			camera.maxRadius = int(value)
			maxRadius_slider.set(camera.maxRadius)
			maxRadius_label_value.configure(text=camera.maxRadius)

		def setCircleSensitivity(value):
			camera.circleSensitivity = int(value)
			circleSensitivity_slider.set(camera.circleSensitivity)
			circleSensitivity_label_value.configure(text=camera.circleSensitivity)

		def setCircleEdgePoints(value):
			camera.circleEdgePoints = int(value)
			circleEdgePoints_slider.set(camera.circleEdgePoints)
			circleEdgePoints_label_value.configure(text=camera.circleEdgePoints)

		def setBrightness(value):
			camera.brightness = int(value)
			camera.videoCapture.set(cv.CAP_PROP_BRIGHTNESS, camera.brightness)
			cameraBrightness_slider.set(camera.brightness)
			cameraBrightness_label_value.configure(text=camera.brightness)

		def setContrast(value):
			camera.contrast = int(value)
			camera.videoCapture.set(cv.CAP_PROP_CONTRAST, camera.contrast)
			cameraContrast_slider.set(camera.contrast)
			cameraContrast_label_value.configure(text=camera.contrast)

		def setSaturation(value):
			camera.saturation = int(value)
			camera.videoCapture.set(cv.CAP_PROP_SATURATION, camera.saturation)
			cameraSaturation_slider.set(camera.saturation)
			cameraSaturation_label_value.configure(text=camera.saturation)

		def setHue(value):
			camera.hue = int(value)
			camera.videoCapture.set(cv.CAP_PROP_HUE, camera.hue)
			cameraHue_slider.set(camera.hue)
			cameraHue_label_value.configure(text=camera.hue)

		def setGain(value):
			camera.gain = int(value)
			camera.videoCapture.set(cv.CAP_PROP_GAIN, camera.gain)
			cameraGain_slider.set(camera.gain)
			cameraGain_label_value.configure(text=camera.gain)

		def setExposure(value):
			camera.exposure = int(value)
			camera.videoCapture.set(cv.CAP_PROP_EXPOSURE, camera.exposure)
			cameraExposure_slider.set(camera.exposure)
			cameraExposure_label_value.configure(text=camera.exposure)

		def setAutoExposure(value):
			camera.tog_autoE = int(value)
			camera.videoCapture.set(cv.CAP_PROP_AUTO_EXPOSURE, camera.tog_autoE)
			cameraAutoExposure_slider.set(camera.tog_autoE)
			cameraAutoExposure_label_value.configure(text=camera.tog_autoE)

		def setFocus(value):
			camera.focus = round(float(value),1)
			camera.videoCapture.set(cv.CAP_PROP_FOCUS, camera.focus)
			cameraFocus_slider.set(camera.focus)
			cameraFocus_label_value.configure(text=camera.focus)

		def setAutoFocus(value):
			camera.tog_autoF = int(value)
			camera.videoCapture.set(cv.CAP_PROP_AUTOFOCUS, camera.tog_autoF)
			cameraAutoFocus_slider.set(camera.tog_autoF)
			cameraAutoFocus_label_value.configure(text=camera.tog_autoF)

		def setCamPortNum(value):
			camera.cameraNumber = int(value)
			camera.videoCapture = cv.VideoCapture(camera.cameraNumber, cv.CAP_DSHOW)	# Set port number for camera (DSHOW → DirectShow)
			camPortNumber_entry.delete(0,"end")
			camPortNumber_entry.insert(0,camera.cameraNumber)

		def saveVariables():
			np.savez("ProgramVariables" + cameraName_entry.get(), 
	    			 int(camPortNumber_entry.get()),camera.width,camera.height,
					 camera.tog_autoF,camera.tog_autoE,camera.exposure,camera.focus,
					 camera.contrast,camera.brightness,camera.fps,camera.blur,
					 camera.dp,camera.minDist,camera.minRadius,camera.maxRadius,
					 camera.circleSensitivity,camera.circleEdgePoints,
					 camera.saturation,camera.hue,camera.gain)
			
		def loadVariables(value):
			# TODO - load all variables (calibraiton fields) from file name (value)
			programVariables = np.load("ProgramVariables" + value + ".npz", allow_pickle=True)

			setCamPortNum(programVariables['arr_0'])
			# width - 'arr_1'
			# height - 'arr_2'
			setAutoFocus(programVariables['arr_3'])
			setAutoExposure(programVariables['arr_4'])
			setExposure(programVariables['arr_5'])
			setFocus(programVariables['arr_6'])
			setContrast(programVariables['arr_7'])
			setBrightness(programVariables['arr_8'])
			# fps - 'arr_9'
			setBlurLevel(programVariables['arr_10'])
			setDp(programVariables['arr_11'])
			setMinDist(programVariables['arr_12'])
			setMinRadius(programVariables['arr_13'])
			setMaxRadius(programVariables['arr_14'])
			setCircleSensitivity(programVariables['arr_15'])
			setCircleEdgePoints(programVariables['arr_16'])
			setSaturation(programVariables['arr_17'])
			setHue(programVariables['arr_18'])
			setGain(programVariables['arr_19'])
		
		def runCalibration():
			cf.runCalibration(int(camPortNumber_entry.get()),int(calGridWidth_entry.get()),
		     				  int(calStartingX_entry.get()),int(calStartingY_entry.get()),
							  int(calChessH_entry.get()),int(calChessW_entry.get()),
							  cameraName_entry.get(),int(calCameraZ_entry.get()))
		
		def startProgram():
			# FIXME When moving focus to GUI it crashes
			#Thread(target = camera.detectionProgram(1)).start()

			#camera.videoCapture.release()	# Release webcam and close all windows
			#cv.destroyAllWindows()	# Close all OpenCV windows (does not close the GUI)
			return
		
		def killCameraWindows():
			camera.videoCapture.release()
			cv.destroyAllWindows()
					
		def getNpzFiles():
			npzFiles = []
			for file in os.listdir("./"):
				if file.endswith(".npz"):
					file = file[:-4] # Remove .npz from end of name
					file = file.removeprefix('ProgramVariables') # Strip all but camera name
					npzFiles.append(file)
			return npzFiles

		## Components of algorithm frame
		# Blur level of frame
		blurLevel_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="Blur", font=('Arial', 22)).grid(
				row=0, column=0, pady=10, padx=10)
		blurLevel_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=55, width=400, number_of_steps=27, border_width=3, command=setBlurLevel)
		blurLevel_slider.set(camera.blur)
		blurLevel_slider.grid(row=0, column=1, pady=10, padx=10)
		blurLevel_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.blur, font=('Arial', 22))
		blurLevel_label_value.grid(row=0, column=2, pady=10, padx=10)	

		# dp inverse ratio of resolution
		dp_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="dp", font=('Arial', 22)).grid(
				row=1, column=0, pady=10, padx=10)
		dp_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=5, width=400, number_of_steps=80, border_width=3, command=setDp)
		dp_slider.set(camera.dp)
		dp_slider.grid(row=1, column=1, pady=10, padx=10)
		dp_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.dp, font=('Arial', 22))
		dp_label_value.grid(row=1, column=2, pady=10, padx=10)
		
		# Minimum distance between circles
		minDist_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="MinDist", font=('Arial', 22)).grid(
				row=2, column=0, pady=10, padx=10)
		minDist_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=100, width=400, number_of_steps=999, border_width=3, command=setMinDist)
		minDist_slider.set(camera.minDist)
		minDist_slider.grid(row=2, column=1, pady=10, padx=10)
		minDist_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.minDist, font=('Arial', 22))
		minDist_label_value.grid(row=2, column=2, pady=10, padx=10)

		# Minimum radius of circle
		minRadius_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="MinRadius", font=('Arial', 22)).grid(
				row=3, column=0, pady=10, padx=10)
		minRadius_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=200, width=400, number_of_steps=199, border_width=3, command=setMinRadius)
		minRadius_slider.set(camera.minRadius)
		minRadius_slider.grid(row=3, column=1, pady=10, padx=10)
		minRadius_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.minRadius, font=('Arial', 22))
		minRadius_label_value.grid(row=3, column=2, pady=10, padx=10)

		# Maximum radius of circle
		maxRadius_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="MaxRadius", font=('Arial', 22)).grid(
				row=4, column=0, pady=10, padx=10)
		maxRadius_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=400, width=400, number_of_steps=399,	border_width=3, command=setMaxRadius)
		maxRadius_slider.set(camera.maxRadius)
		maxRadius_slider.grid(row=4, column=1, pady=10, padx=10)
		maxRadius_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.maxRadius, font=('Arial', 22))
		maxRadius_label_value.grid(row=4, column=2, pady=10, padx=10)

		# Sensitivity to circle detection
		circleSensitivity_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="Circle Sensitivity", font=('Arial', 22)).grid(
				row=5, column=0, pady=10, padx=10)
		circleSensitivity_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=1, to=200, width=400, number_of_steps=199, border_width=3, command=setCircleSensitivity)
		circleSensitivity_slider.set(camera.circleSensitivity)
		circleSensitivity_slider.grid(row=5, column=1, pady=10, padx=10)
		circleSensitivity_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.circleSensitivity, font=('Arial', 22))
		circleSensitivity_label_value.grid(row=5, column=2, pady=10, padx=10)

		# Minimum # of edge points to declare a circle
		circleEdgePoints_label = customtkinter.CTkLabel(
			master=algorithmFrame, text="# of edge points", font=('Arial', 22)).grid(
				row=6, column=0, pady=10, padx=10)
		circleEdgePoints_slider = customtkinter.CTkSlider(
			master=algorithmFrame, from_=4, to=100, width=400, number_of_steps=96, border_width=3, command=setCircleEdgePoints)
		circleEdgePoints_slider.set(camera.circleEdgePoints)
		circleEdgePoints_slider.grid(row=6, column=1, pady=10, padx=10)
		circleEdgePoints_label_value = customtkinter.CTkLabel(
			master=algorithmFrame, text=camera.circleEdgePoints, font=('Arial', 22))
		circleEdgePoints_label_value.grid(row=6, column=2, pady=10, padx=10)

		## Components of camera frame
		# Brightness of capture
		cameraBrightness_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Brightness", font=('Arial', 22)).grid(
				row=0, column=3, pady=10, padx=10)
		cameraBrightness_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255, border_width=3, command=setBrightness)
		cameraBrightness_slider.set(camera.brightness)
		cameraBrightness_slider.grid(row=0, column=4, pady=10, padx=10)
		cameraBrightness_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.brightness, font=('Arial', 22))
		cameraBrightness_label_value.grid(row=0, column=5, pady=10, padx=10)

		# Contrast of capture
		cameraContrast_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Contrast", font=('Arial', 22)).grid(
				row=1, column=3, pady=10, padx=10)
		cameraContrast_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255, border_width=3, command=setContrast)
		cameraContrast_slider.set(camera.contrast)
		cameraContrast_slider.grid(row=1, column=4, pady=10, padx=10)
		cameraContrast_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.contrast, font=('Arial', 22))
		cameraContrast_label_value.grid(row=1, column=5, pady=10, padx=10)
		
		# Saturation of capture
		cameraSaturation_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Saturation", font=('Arial', 22)).grid(
				row=2, column=3, pady=10, padx=10)
		cameraSaturation_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255, border_width=3, command=setSaturation)
		cameraSaturation_slider.set(camera.saturation)
		cameraSaturation_slider.grid(row=2, column=4, pady=10, padx=10)
		cameraSaturation_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.saturation, font=('Arial', 22))
		cameraSaturation_label_value.grid(row=2, column=5, pady=10, padx=10)

		# Hue of capture (not applicable to my camera?)
		cameraHue_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Hue", font=('Arial', 22)).grid(
				row=3, column=3, pady=10, padx=10)
		cameraHue_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255, border_width=3, command=setHue)
		cameraHue_slider.set(camera.hue)
		cameraHue_slider.grid(row=3, column=4, pady=10, padx=10)
		cameraHue_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.hue, font=('Arial', 22))
		cameraHue_label_value.grid(row=3, column=5, pady=10, padx=10)
		
		# Gain of capture
		cameraGain_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Gain", font=('Arial', 22)).grid(
				row=4, column=3, pady=10, padx=10)
		cameraGain_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255, border_width=3, command=setGain)
		cameraGain_slider.set(camera.gain)
		cameraGain_slider.grid(row=4, column=4, pady=10, padx=10)
		cameraGain_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.gain, font=('Arial', 22))
		cameraGain_label_value.grid(row=4, column=5, pady=10, padx=10)

		# Exposure of capture
		cameraExposure_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Exposure", font=('Arial', 22)).grid(
				row=5, column=3, pady=10, padx=10)
		cameraExposure_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=-11, to=-1, width=400, number_of_steps=10, border_width=3, command=setExposure)
		cameraExposure_slider.set(camera.exposure)
		cameraExposure_slider.grid(row=5, column=4, pady=10, padx=10)
		cameraExposure_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.exposure, font=('Arial', 22))
		cameraExposure_label_value.grid(row=5, column=5, pady=10, padx=10)

		# Auto Exposure of capture
		cameraAutoExposure_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Auto Exposure", font=('Arial', 22)).grid(
				row=6, column=3, pady=10, padx=10)
		cameraAutoExposure_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=1, width=400, number_of_steps=1, border_width=3, command=setAutoExposure)
		cameraAutoExposure_slider.set(camera.tog_autoE)
		cameraAutoExposure_slider.grid(row=6, column=4, pady=10, padx=10)
		cameraAutoExposure_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.tog_autoE, font=('Arial', 22))
		cameraAutoExposure_label_value.grid(row=6, column=5, pady=10, padx=10)

		# Focus of capture
		cameraFocus_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Focus", font=('Arial', 22)).grid(
				row=7, column=3, pady=10, padx=10)
		cameraFocus_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=1, width=400, number_of_steps=10, border_width=3, command=setFocus)
		cameraFocus_slider.set(camera.focus)
		cameraFocus_slider.grid(row=7, column=4, pady=10, padx=10)
		cameraFocus_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.focus, font=('Arial', 22))
		cameraFocus_label_value.grid(row=7, column=5, pady=10, padx=10)

		# Auto Focus of capture
		cameraAutoFocus_label = customtkinter.CTkLabel(
			master=cameraFrame, text="Camera Auto Focus", font=('Arial', 22)).grid(
				row=8, column=3, pady=10, padx=10)
		cameraAutoFocus_slider = customtkinter.CTkSlider(
			master=cameraFrame, from_=0, to=1, width=400, number_of_steps=1, border_width=3, command=setAutoFocus)
		cameraAutoFocus_slider.set(camera.tog_autoF)
		cameraAutoFocus_slider.grid(row=8, column=4, pady=10, padx=10)
		cameraAutoFocus_label_value = customtkinter.CTkLabel(
			master=cameraFrame, text=camera.tog_autoF, font=('Arial', 22))
		cameraAutoFocus_label_value.grid(row=8, column=5, pady=10, padx=10)

		## Components of calibration frame
		# Calibration Grid Width (Default 3.0 (cm))
		calGridWidth_label = customtkinter.CTkLabel(
			master=calibrationFrame, text="Cal grid width", font=('Arial', 22)).grid(
				row=1, column=0, pady=10, padx=10)
		calGridWidth_entry = customtkinter.CTkEntry(
			master=calibrationFrame, placeholder_text='Default: 2.44 (cm)', width=435, height=25, corner_radius=10)
		calGridWidth_entry.grid(row=1, column=1, pady=10, padx=10)

		# Calibration starting X (measured in holes from 0,0 hole)
		calStartingX_label = customtkinter.CTkLabel(
			master=calibrationFrame, text="Cal starting X", font=('Arial', 22)).grid(
				row=2, column=0, pady=10, padx=10)
		calStartingX_entry = customtkinter.CTkEntry(
			master=calibrationFrame, placeholder_text='Default: 0 (Measured in holes from 0,0 hole)', width=435, height=25, corner_radius=10)
		calStartingX_entry.grid(row=2, column=1, pady=10, padx=10)

		# Calibration starting Y (measured in holes from 0,0 hole)
		calStartingY_label = customtkinter.CTkLabel(
			master=calibrationFrame, text="Cal starting Y", font=('Arial', 22)).grid(
				row=3, column=0, pady=10, padx=10)
		calStartingY_entry = customtkinter.CTkEntry(
			master=calibrationFrame, placeholder_text='Default: 0 (Measured in holes from 0,0 hole)', width=435, height=25, corner_radius=10)
		calStartingY_entry.grid(row=3, column=1, pady=10, padx=10)

		# Calibration chess height (default 14)
		calChessH_label = customtkinter.CTkLabel(
			master=calibrationFrame, text="Cal chess height", font=('Arial', 22)).grid(
				row=4, column=0, pady=10, padx=10)
		calChessH_entry = customtkinter.CTkEntry(
			master=calibrationFrame, placeholder_text='Default: 7 (squares)', width=435, height=25, corner_radius=10)
		calChessH_entry.grid(row=4, column=1, pady=10, padx=10)

		# Calibration chess width (default 9)
		calChessW_label = customtkinter.CTkLabel(
			master=calibrationFrame, text="Cal chess width", font=('Arial', 22)).grid(
				row=5, column=0, pady=10, padx=10)
		calChessW_entry = customtkinter.CTkEntry(
			master=calibrationFrame, placeholder_text='Default: 9 (squares)', width=435, height=25, corner_radius=10)
		calChessW_entry.grid(row=5, column=1, pady=10, padx=10)

		# Calibration camera z distance (Measured by hand, the distance from camera to startingX, startingY location (cm))
		calCameraZ_label = customtkinter.CTkLabel(
			master=calibrationFrame, text="Cal Z distance", font=('Arial', 22)).grid(
				row=6, column=0, pady=10, padx=10)
		calCameraZ_entry = customtkinter.CTkEntry(
			master=calibrationFrame, placeholder_text='Measured: Distance from camera to startingX,startingY location (cm)', width=435, height=25, corner_radius=10)
		calCameraZ_entry.grid(row=6, column=1, pady=10, padx=10)

		## Components of button frame
		# Camera Port Number (Serial Port)
		camPortNumber_label = customtkinter.CTkLabel(
			master=buttonFrame, text="Camera Port #", font=('Arial', 22)).grid(
				row=0, column=0, pady=10, padx=10)
		camPortNumber_entry = customtkinter.CTkEntry(
			master=buttonFrame, placeholder_text='Default: 0 or 1', font=('Arial', 18), width=200, height=25, corner_radius=10)
		camPortNumber_entry.grid(row=0, column=1, pady=10, padx=10)

		# Camera name (used in filename of stored variable files)
		cameraNameSave_label = customtkinter.CTkLabel(
			master=buttonFrame, text="Camera Name", font=('Arial', 22)).grid(
				row=1, column=0, pady=10, padx=10)
		cameraName_entry = customtkinter.CTkEntry(
			master=buttonFrame, placeholder_text='Default', font=('Arial', 18), width=200, height=25, corner_radius=10)
		cameraName_entry.grid(row=1, column=1, pady=10, padx=10)
		customtkinter.CTkButton(
			master=buttonFrame, text='Save Variables', font=('Arial', 18), height=80, command=saveVariables).grid(
				row=0, column=2, rowspan=2, pady=10, padx=10)

		# Load variables from files shown in option menu
		loadVariables_label = customtkinter.CTkLabel(
			master=buttonFrame, text="Load Variables", font=('Arial', 22)).grid(
				row=2, column=0, pady=10, padx=10)
		customtkinter.CTkOptionMenu(
			master=buttonFrame, values=getNpzFiles(), font=('Arial', 18), width=362, command=loadVariables).grid(
				row=2, column=1, columnspan=2, padx=10, pady=10)

		customtkinter.CTkButton(
			master=buttonFrame, text='Close GUI', font=('Arial', 18), height=135, command=root.quit).grid(
				row=0, column=3, rowspan=3, pady=10, padx=10)
		
		customtkinter.CTkButton(
			master=buttonFrame, text='End Program', font=('Arial', 18), height=80, command=killCameraWindows).grid(
				row=3, column=3, rowspan=2, pady=10, padx=10)
		
		customtkinter.CTkButton(
			master=buttonFrame, text='Run Calibration', font=('Arial', 18), width=530, command=runCalibration).grid(
				row=3, column=0, columnspan=3, pady=10, padx=10)

		customtkinter.CTkButton(
			master=buttonFrame, text='Start Program', font=('Arial', 18), width=530, command=startProgram).grid(
				row=4, column=0, columnspan=3, pady=10, padx=10)
		
		root.mainloop()