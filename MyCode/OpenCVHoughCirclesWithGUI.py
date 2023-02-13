import cv2 as cv
import numpy as np
import sys
from threading import Thread
import customtkinter
import time
import math

## Initialize global variables
# Circle Detecting Algorithm (intial conditions)
blurLevel = 17					# Level of blur applied to filter(must be odd)
gradient = cv.HOUGH_GRADIENT	# Type of gradient to use
dp = 1.2						# Inverse ratio of resolution
minDist = 500					# Minimum distance between the center of two circles
minRadiusVar = 1				# Minimum radius for circle
maxRadiusVar = 200				# Max radius for circle
circleSensitivity = 100			# Sensitivity to circle detection
circleEdgePoints = 50			# Number of edge points necessary to declare a circle(more is a better circle)

# Camera Settings (initial conditions)
brightness = 100	# Set brightness parameter of camera
contrast = 100		# Set contrast parameter of camera
saturation = 125	# Set saturation parameter of camera
hue = 0				# Set hue parameter of camera
gain = 10			# Set gain parameter of camera
exposure = 0		# Set exposure parameter of camera
autoExposure = 0	# Set auto exposure parameter of camera
autoFocus = 1		# Set auto focus parameter of camera

# Camera initialization
videoCapture = cv.VideoCapture(0, cv.CAP_DSHOW) # Set port number for camera (DSHOW → DirectShow)
videoCapture.set(cv.CAP_PROP_FRAME_WIDTH, 1280) # Set camera frame width
videoCapture.set(cv.CAP_PROP_FRAME_HEIGHT, 720) # Set camera frame height
videoCapture.set(cv.CAP_PROP_FPS, 60)			# Set camera fps
# videoCapture.set(cv.CAP_PROP_FOURCC, 			# Compression format of camera
# 	cv.VideoWriter_fourcc('M','J','P','G'))		# Set using 4 character code

def createGUI():
	customtkinter.set_appearance_mode('System')
	customtkinter.set_default_color_theme('blue')

	root = customtkinter.CTk()
	root.title('Light/Camera Settings')
	root.iconbitmap('AirHockeyIcon.ico')
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
		global blurLevel
		blurLevel = int(value)
		blurLevel_label_value.configure(text=blurLevel)

	def setDp(value):
		global dp
		dp = round(value, 1)
		dp_label_value.configure(text=dp)

	def setMinDist(value):
		global minDist
		minDist = int(value)
		minDist_label_value.configure(text=minDist)

	def setMinRadius(value):
		global minRadiusVar
		minRadiusVar = int(value)
		minRadius_label_value.configure(text=minRadiusVar)

	def setMaxRadius(value):
		global maxRadiusVar
		maxRadiusVar = int(value)
		maxRadius_label_value.configure(text=maxRadiusVar)

	def setCircleSensitivity(value):
		global circleSensitivity
		circleSensitivity = int(value)
		circleSensitivity_label_value.configure(text=circleSensitivity)

	def setCircleEdgePoints(value):
		global circleEdgePoints
		circleEdgePoints = int(value)
		circleEdgePoints_label_value.configure(text=circleEdgePoints)

	def setBrightness(value):
		global brightness
		brightness = int(value)
		videoCapture.set(cv.CAP_PROP_BRIGHTNESS, brightness)
		cameraBrightness_label_value.configure(text=brightness)

	def setContrast(value):
		global contrast
		contrast = int(value)
		videoCapture.set(cv.CAP_PROP_CONTRAST, contrast)
		cameraContrast_label_value.configure(text=contrast)

	def setSaturation(value):
		global saturation
		saturation = int(value)
		videoCapture.set(cv.CAP_PROP_SATURATION, saturation)
		cameraSaturation_label_value.configure(text=saturation)

	def setHue(value):
		global hue
		hue = int(value)
		videoCapture.set(cv.CAP_PROP_HUE, hue)
		cameraHue_label_value.configure(text=hue)

	def setGain(value):
		global gain
		gain = int(value)
		videoCapture.set(cv.CAP_PROP_GAIN, gain)
		cameraGain_label_value.configure(text=gain)

	def setExposure(value):
		global exposure
		exposure = int(value)
		videoCapture.set(cv.CAP_PROP_EXPOSURE, exposure)
		cameraExposure_label_value.configure(text=exposure)

	def setAutoExposure(value):
		global autoExposure
		autoExposure = int(value)
		videoCapture.set(cv.CAP_PROP_AUTO_EXPOSURE, autoExposure)
		cameraAutoExposure_label_value.configure(text=autoExposure)

	def setAutoFocus(value):
		global autoFocus
		autoFocus = int(value)
		videoCapture.set(cv.CAP_PROP_AUTOFOCUS, autoFocus)
		cameraAutoFocus_label_value.configure(text=autoFocus)

	## Sliders for circle detecting algorithm
	# Blur level of frame
	blurLevel_label = customtkinter.CTkLabel(
		master=algorithmFrame, text="Blur", font=('Arial', 22))
	blurLevel_label.grid(row=0, column=0, pady=10, padx=10)
	blurLevel_slider = customtkinter.CTkSlider(
		master=algorithmFrame, from_=1, to=55, width=400, number_of_steps=27,
		border_width=3, command=setBlurLevel)
	blurLevel_slider.set(blurLevel)
	blurLevel_slider.grid(row=0, column=1, pady=10, padx=10)
	blurLevel_label_value = customtkinter.CTkLabel(
		master=algorithmFrame, text=blurLevel, font=('Arial', 22))
	blurLevel_label_value.grid(row=0, column=2, pady=10, padx=10)	

	# dp inverse ratio of resolution
	dp_label = customtkinter.CTkLabel(
		master=algorithmFrame, text="dp", font=('Arial', 22))
	dp_label.grid(row=1, column=0, pady=10, padx=10)
	dp_slider = customtkinter.CTkSlider(
		master=algorithmFrame, from_=1, to=5, width=400, number_of_steps=80,
		border_width=3, command=setDp)
	dp_slider.set(dp)
	dp_slider.grid(row=1, column=1, pady=10, padx=10)
	dp_label_value = customtkinter.CTkLabel(
		master=algorithmFrame, text=dp, font=('Arial', 22))
	dp_label_value.grid(row=1, column=2, pady=10, padx=10)
	
	# Minimum distance between circles
	minDist_label = customtkinter.CTkLabel(
		master=algorithmFrame, text="MinDist", font=('Arial', 22))
	minDist_label.grid(row=2, column=0, pady=10, padx=10)
	minDist_slider = customtkinter.CTkSlider(
		master=algorithmFrame, from_=1, to=100, width=400, number_of_steps=999,
		border_width=3, command=setMinDist)
	minDist_slider.set(minDist)
	minDist_slider.grid(row=2, column=1, pady=10, padx=10)
	minDist_label_value = customtkinter.CTkLabel(
		master=algorithmFrame, text=minDist, font=('Arial', 22))
	minDist_label_value.grid(row=2, column=2, pady=10, padx=10)

	# Minimum radius of circle
	minRadius_label = customtkinter.CTkLabel(
		master=algorithmFrame, text="MinRadius", font=('Arial', 22))
	minRadius_label.grid(row=3, column=0, pady=10, padx=10)
	minRadius_slider = customtkinter.CTkSlider(
		master=algorithmFrame, from_=1, to=200, width=400, number_of_steps=199,
		border_width=3, command=setMinRadius)
	minRadius_slider.set(minRadiusVar)
	minRadius_slider.grid(row=3, column=1, pady=10, padx=10)
	minRadius_label_value = customtkinter.CTkLabel(
		master=algorithmFrame, text=minRadiusVar, font=('Arial', 22))
	minRadius_label_value.grid(row=3, column=2, pady=10, padx=10)

	# Maximum radius of circle
	maxRadius_label = customtkinter.CTkLabel(
		master=algorithmFrame, text="MaxRadius", font=('Arial', 22))
	maxRadius_label.grid(row=4, column=0, pady=10, padx=10)
	maxRadius_slider = customtkinter.CTkSlider(
		master=algorithmFrame, from_=1, to=400, width=400, number_of_steps=399,
		border_width=3, command=setMaxRadius)
	maxRadius_slider.set(maxRadiusVar)
	maxRadius_slider.grid(row=4, column=1, pady=10, padx=10)
	maxRadius_label_value = customtkinter.CTkLabel(
		master=algorithmFrame, text=maxRadiusVar, font=('Arial', 22))
	maxRadius_label_value.grid(row=4, column=2, pady=10, padx=10)

	# Sensitivity to circle detection
	circleSensitivity_label = customtkinter.CTkLabel(
		master=algorithmFrame, text="Circle Sensitivity", font=('Arial', 22))
	circleSensitivity_label.grid(row=5, column=0, pady=10, padx=10)
	circleSensitivity_slider = customtkinter.CTkSlider(
		master=algorithmFrame, from_=1, to=200, width=400, number_of_steps=199,
		 border_width=3, command=setCircleSensitivity)
	circleSensitivity_slider.set(circleSensitivity)
	circleSensitivity_slider.grid(row=5, column=1, pady=10, padx=10)
	circleSensitivity_label_value = customtkinter.CTkLabel(
		master=algorithmFrame, text=circleSensitivity, font=('Arial', 22))
	circleSensitivity_label_value.grid(row=5, column=2, pady=10, padx=10)

	# Minimum # of edge points to declare a circle
	circleEdgePoints_label = customtkinter.CTkLabel(
		master=algorithmFrame, text="# of edge points", font=('Arial', 22))
	circleEdgePoints_label.grid(row=6, column=0, pady=10, padx=10)
	circleEdgePoints_slider = customtkinter.CTkSlider(
		master=algorithmFrame, from_=4, to=100, width=400, number_of_steps=96,
		border_width=3, command=setCircleEdgePoints)
	circleEdgePoints_slider.set(circleEdgePoints)
	circleEdgePoints_slider.grid(row=6, column=1, pady=10, padx=10)
	circleEdgePoints_label_value = customtkinter.CTkLabel(
		master=algorithmFrame, text=circleEdgePoints, font=('Arial', 22))
	circleEdgePoints_label_value.grid(row=6, column=2, pady=10, padx=10)

	## Sliders for camera settings
	# Brightness of capture
	cameraBrightness_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Brightness", font=('Arial', 22))
	cameraBrightness_label.grid(row=0, column=3, pady=10, padx=10)
	cameraBrightness_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
		border_width=3, command=setBrightness)
	cameraBrightness_slider.set(brightness)
	cameraBrightness_slider.grid(row=0, column=4, pady=10, padx=10)
	cameraBrightness_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=brightness, font=('Arial', 22))
	cameraBrightness_label_value.grid(row=0, column=5, pady=10, padx=10)

	# Contrast of capture
	cameraContrast_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Contrast", font=('Arial', 22))
	cameraContrast_label.grid(row=1, column=3, pady=10, padx=10)
	cameraContrast_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
		border_width=3, command=setContrast)
	cameraContrast_slider.set(contrast)
	cameraContrast_slider.grid(row=1, column=4, pady=10, padx=10)
	cameraContrast_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=contrast, font=('Arial', 22))
	cameraContrast_label_value.grid(row=1, column=5, pady=10, padx=10)
	
	# Saturation of capture
	cameraSaturation_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Saturation", font=('Arial', 22))
	cameraSaturation_label.grid(row=2, column=3, pady=10, padx=10)
	cameraSaturation_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
		border_width=3, command=setSaturation)
	cameraSaturation_slider.set(saturation)
	cameraSaturation_slider.grid(row=2, column=4, pady=10, padx=10)
	cameraSaturation_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=saturation, font=('Arial', 22))
	cameraSaturation_label_value.grid(row=2, column=5, pady=10, padx=10)

	# Hue of capture (not applicable to my camera?)
	cameraHue_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Hue", font=('Arial', 22))
	cameraHue_label.grid(row=3, column=3, pady=10, padx=10)
	cameraHue_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
		border_width=3, command=setHue)
	cameraHue_slider.set(hue)
	cameraHue_slider.grid(row=3, column=4, pady=10, padx=10)
	cameraHue_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=hue, font=('Arial', 22))
	cameraHue_label_value.grid(row=3, column=5, pady=10, padx=10)
	

	# Gain of capture
	cameraGain_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Gain", font=('Arial', 22))
	cameraGain_label.grid(row=4, column=3, pady=10, padx=10)
	cameraGain_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
		border_width=3, command=setGain)
	cameraGain_slider.set(gain)
	cameraGain_slider.grid(row=4, column=4, pady=10, padx=10)
	cameraGain_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=gain, font=('Arial', 22))
	cameraGain_label_value.grid(row=4, column=5, pady=10, padx=10)

	# Exposure of capture (not applicable to my camera?)
	cameraExposure_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Exposure", font=('Arial', 22))
	cameraExposure_label.grid(row=5, column=3, pady=10, padx=10)
	cameraExposure_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=255, width=400, number_of_steps=255,
		border_width=3, command=setExposure)
	cameraExposure_slider.set(exposure)
	cameraExposure_slider.grid(row=5, column=4, pady=10, padx=10)
	cameraExposure_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=exposure, font=('Arial', 22))
	cameraExposure_label_value.grid(row=5, column=5, pady=10, padx=10)

	# Auto Exposure of capture
	cameraExposure_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Auto Exposure", font=('Arial', 22))
	cameraExposure_label.grid(row=6, column=3, pady=10, padx=10)
	cameraExposure_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=1, width=400, number_of_steps=1,
		border_width=3, command=setAutoExposure)
	cameraExposure_slider.set(autoExposure)
	cameraExposure_slider.grid(row=6, column=4, pady=10, padx=10)
	cameraAutoExposure_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=autoExposure, font=('Arial', 22))
	cameraAutoExposure_label_value.grid(row=6, column=5, pady=10, padx=10)

	# Auto Focus of capture
	cameraExposure_label = customtkinter.CTkLabel(
		master=cameraFrame, text="Camera Auto Focus", font=('Arial', 22))
	cameraExposure_label.grid(row=7, column=3, pady=10, padx=10)
	cameraExposure_slider = customtkinter.CTkSlider(
		master=cameraFrame, from_=0, to=1, width=400, number_of_steps=1,
		border_width=3, command=setAutoFocus)
	cameraExposure_slider.set(autoFocus)
	cameraExposure_slider.grid(row=7, column=4, pady=10, padx=10)
	cameraAutoFocus_label_value = customtkinter.CTkLabel(
		master=cameraFrame, text=autoFocus, font=('Arial', 22))
	cameraAutoFocus_label_value.grid(row=7, column=5, pady=10, padx=10)

	# Buttons
	customtkinter.CTkButton(
		master=buttonFrame, text='Quit', command=root.quit).grid(
			row=7, column=1, pady=10, padx=10)
	
	root.mainloop()

def findCircles():
	prevCircle = None 	# Circle from the previous frame (will represent the current detected circle)

	dist = lambda x1, y1, x2, y2: (math.dist([x1, x2], [y1, y2]))	# Function that calculates the square of the distance between two points in a frame

	# Variables used for measuring how algorithm is running
	runtime = 0			# Runtime of each individual loop (each frame)
	runtimeCounter = 0	# Total runtime of all loops added up
	startTime = 0		# Starting time of each loop
	frameCounter = 0	# Total number of frames detected by the program during runtime
	circleCounter = 0	# Total number of circles detected by the program during runtime

	while True:
		startTime = time.perf_counter()	# Time how long the loop will take to run

		ret, frame = videoCapture.read()	# ret is a boolean value for whether it was able to read the frame successfully
		# print(ret)						# frame is the captured image from the camera
			
		if not ret:							# If frame is not read successfully, end program
			print("Couldn't read frame\n")
			break
		
		frameCounter += 1	# Frame is read successfully, so increment frame counter

		# cv.imshow("Frame", frame)	# Show initial frame to user on the screen

		grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)	# Make a copy of frame where the color has been converted to grayscale
		# cv.imshow("Grayed Frame", grayFrame)				# (Can use different color settings, but cv.HoughCircles requires a grayscale image)

		blurFrame = cv.GaussianBlur(grayFrame, (blurLevel,blurLevel), 0)	# Make a copy of grayFrame where the frame has been blurred
		# cv.imshow("Blurred Frame", blurFrame)								# (Can use different blurring filters and adjust the level of blurring)

		circles = cv.HoughCircles(blurFrame,	# Find circles within the frame given these parameters.
								  gradient,		# The result will be a list of circles found.
								  dp,
								  minDist,
								  param1=circleSensitivity,
								  param2=circleEdgePoints,
								  minRadius=minRadiusVar,
								  maxRadius=maxRadiusVar)
		
		if circles is not None:	# Are there circles detected in the frame
			
			circles = np.uint16(np.around(circles))	# Convert circles to a numpy array
			 
			chosen = None	# Chosen circle from the frame

			for i in circles[0, :]:	# Iterate through array of circles

				if chosen is None:	# If there is no circle chosen yet, 
					chosen = i		# set the chosen circle equal to the first circle in the array
				
				if prevCircle is not None: 										# Is there is a current circle stored
					if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1])\
						 	<= dist(i[0], i[1], prevCircle[0], prevCircle[1]):	# If the distance from the chosen circles center to the current circles center
																				# is less than or equal to the distance from the next circles center in the
																				# array to the current circles center, then set the chosen circle equal to the
						chosen = i												# next circle in the array
						
						# print(f'Chosen[0]: {chosen[0]} Chosen[1]:', end=' ')
						# print(f'{chosen[1]} Chosen[2]: {chosen[2]}')
			
			cv.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)	# Draw a circle at the centerpoint of the chosen circle
			cv.circle(frame, (chosen[0], chosen[1]), chosen[2],			# Draw a circle around the circumference of the chosen circle
					  (255, 0, 255), 3)

			prevCircle = chosen	# Set the previous circle equal to the chosen circle at the end of the loop

			circleCounter += 1	# Circle is drawn, so increment circle counter

		cv.imshow("Circles", frame)	# Show the original frame with the drawn circles to the user

		runtime = time.perf_counter() - startTime 	# Time how long the loop took to run
		runtimeCounter += runtime					# Get a total runtime of all loops

		if cv.waitKey(1) & 0xFF == ord('q'):									# Quit program if user presses the 'q' key while in the imshow window
			print('Exiting program(Executed by user)\n')						# Outputs that the user decided to exit the program
			print(f'Total Runtime: {runtimeCounter:.3f} sec\n')					# Outputs total runtime of the program in seconds
			print(f'Total Frames: {frameCounter:.0f}\n')						# Outputs the total number of frames processed by the detection program
			print(f'FPS: {(frameCounter/runtimeCounter):.3f}\n')				# Outputs the number of frames per second the detection program ran at
			print(f'Processing speed: {runtimeCounter/circleCounter:.3f} sec\n')# Outputs the average time in seconds it took the program to process each circle
			print(f'Accuracy: {100*(circleCounter/frameCounter):.3f}%')			# Outputs the ratio of circles found to number of frames processed in percentage

			videoCapture.release()	# Release webcam and close all windows
			cv.destroyAllWindows()	# Close all OpenCV windows (does not close the GUI)	
			sys.exit()				# Terminate the program


if __name__ == "__main__":
	print("\nFind circles within camera's frame and draw a circle", end=" ")	# Opening message as user starts program
	print(" around it's circumference. Press 'q' key at any time to exit.\n")	# ↑		

	Thread(target = createGUI).start()		# Start the createGUI function in its own thread. Necessary to run simultaneously with findCircles function.
	Thread(target = findCircles).start()	# Start the findCircles function in its own thread. Necessary to run simultaneously with createGUI function.