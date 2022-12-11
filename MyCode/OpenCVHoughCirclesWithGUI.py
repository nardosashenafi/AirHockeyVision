import cv2 as cv
import numpy as np
import sys
from threading import Thread
import customtkinter
import time

## Initialize global variables:
# Access webcam(# is the port of webcam)
videoCapture = cv.VideoCapture(0)

# Circle Detecting Algorithm
blur = 17
dp = 1.2
minDist = 500
minRadiusVar = 1
maxRadiusVar = 200
circleSensitivity = 100
circleEdgePoints = 50

# Camera Settings
brightness = 100
contrast = 100
saturation = 125
hue = 0
gain = 10
exposure = 0

def createGUI():
	customtkinter.set_appearance_mode('System')
	customtkinter.set_default_color_theme('blue')

	root = customtkinter.CTk()
	root.title('Light/Camera Settings')
	root.iconbitmap('C:/Users/rosco/OneDrive/Documents/ECE 480/Main Project/AirHockeyVision/MyCode/AirHockeyIcon.ico')
	root.geometry('1366x768')
	root.resizable(0,0)

	frame = customtkinter.CTkFrame(master=root)
	frame.grid(row=0,column=0,padx=50,pady=50)

	## Definitions for updating value in GUI and variables
	def set_blur(value):
		global blur
		blur = int(value)
		blur_label_value.configure(text=int(value))

	def set_dp(value):
		global dp
		dp = round(value, 1)
		dp_label_value.configure(text=round(value, 1))

	def set_minDist(value):
		global minDist
		minDist = int(value)
		minDist_label_value.configure(text=int(value))

	def set_minRadius(value):
		global minRadiusVar
		minRadiusVar = int(value)
		minRadius_label_value.configure(text=int(value))

	def set_maxRadius(value):
		global maxRadiusVar
		maxRadiusVar = int(value)
		maxRadius_label_value.configure(text=int(value))

	def set_circleSensitivity(value):
		global circleSensitivity
		circleSensitivity = int(value)
		circleSensitivity_label_value.configure(text=int(value))

	def set_circleEdgePoints(value):
		global circleEdgePoints
		circleEdgePoints = int(value)
		circleEdgePoints_label_value.configure(text=int(value))

	def set_brightness(value):
		global brightness
		brightness = int(value)
		videoCapture.set(cv.CAP_PROP_BRIGHTNESS, value)
		cameraBrightness_label_value.configure(text=int(value))

	def set_contrast(value):
		global contrast
		contrast = int(value)
		videoCapture.set(cv.CAP_PROP_CONTRAST, value)
		cameraContrast_label_value.configure(text=int(value))

	def set_saturation(value):
		global saturation
		saturation = int(value)
		videoCapture.set(cv.CAP_PROP_SATURATION, value)
		cameraSaturation_label_value.configure(text=int(value))

	def set_hue(value):
		global hue
		hue = int(value)
		videoCapture.set(cv.CAP_PROP_HUE, value)
		cameraHue_label_value.configure(text=int(value))

	def set_gain(value):
		global gain
		gain = int(value)
		videoCapture.set(cv.CAP_PROP_GAIN, value)
		cameraGain_label_value.configure(text=int(value))

	def set_exposure(value):
		global exposure
		exposure = int(value)
		videoCapture.set(cv.CAP_PROP_EXPOSURE, value)
		cameraExposure_label_value.configure(text=int(value))

	## Sliders for circle detecting algorithm
	# Blur level of frame
	blur_label = customtkinter.CTkLabel(master=frame, text="Blur")
	blur_label.grid(row=0, column=0, pady=10, padx=10)
	blur_slider = customtkinter.CTkSlider(master=frame, from_=1, to=55, width=400,
						number_of_steps=27, border_width=3, command=set_blur)
	blur_slider.set(blur)
	blur_slider.grid(row=0, column=1, pady=10, padx=10)
	blur_label_value = customtkinter.CTkLabel(master=frame, text=blur)
	blur_label_value.grid(row=0, column=2, pady=10, padx=10)	

	# dp inverse ratio of resolution
	dp_label = customtkinter.CTkLabel(master=frame, text="dp")
	dp_label.grid(row=1, column=0, pady=10, padx=10)
	dp_slider = customtkinter.CTkSlider(master=frame, from_=1, to=5, width=400,
						number_of_steps=80, border_width=3, command=set_dp)
	dp_slider.set(dp)
	dp_slider.grid(row=1, column=1, pady=10, padx=10)
	dp_label_value = customtkinter.CTkLabel(master=frame, text=dp)
	dp_label_value.grid(row=1, column=2, pady=10, padx=10)
	
	# Minimum distance between circles
	minDist_label = customtkinter.CTkLabel(master=frame, text="MinDist")
	minDist_label.grid(row=2, column=0, pady=10, padx=10)
	minDist_slider = customtkinter.CTkSlider(master=frame, from_=1, to=100, width=400,
						number_of_steps=999, border_width=3, command=set_minDist)
	minDist_slider.set(minDist)
	minDist_slider.grid(row=2, column=1, pady=10, padx=10)
	minDist_label_value = customtkinter.CTkLabel(master=frame, text=minDist)
	minDist_label_value.grid(row=2, column=2, pady=10, padx=10)

	# Minimum radius of circle
	minRadius_label = customtkinter.CTkLabel(master=frame, text="MinRadius")
	minRadius_label.grid(row=3, column=0, pady=10, padx=10)
	minRadius_slider = customtkinter.CTkSlider(master=frame, from_=1, to=200, width=400,
						number_of_steps=199, border_width=3, command=set_minRadius)
	minRadius_slider.set(minRadiusVar)
	minRadius_slider.grid(row=3, column=1, pady=10, padx=10)
	minRadius_label_value = customtkinter.CTkLabel(master=frame, text=minRadiusVar)
	minRadius_label_value.grid(row=3, column=2, pady=10, padx=10)

	# Maximum radius of circle
	maxRadius_label = customtkinter.CTkLabel(master=frame, text="MaxRadius")
	maxRadius_label.grid(row=4, column=0, pady=10, padx=10)
	maxRadius_slider = customtkinter.CTkSlider(master=frame, from_=1, to=400, width=400,
						number_of_steps=399, border_width=3, command=set_maxRadius)
	maxRadius_slider.set(maxRadiusVar)
	maxRadius_slider.grid(row=4, column=1, pady=10, padx=10)
	maxRadius_label_value = customtkinter.CTkLabel(master=frame, text=maxRadiusVar)
	maxRadius_label_value.grid(row=4, column=2, pady=10, padx=10)

	# Sensitivity to circle detection
	circleSensitivity_label = customtkinter.CTkLabel(master=frame, text="Circle Sensitivity")
	circleSensitivity_label.grid(row=5, column=0, pady=10, padx=10)
	circleSensitivity_slider = customtkinter.CTkSlider(master=frame, from_=1, to=200, width=400,
						number_of_steps=199, border_width=3, command=set_circleSensitivity)
	circleSensitivity_slider.set(circleSensitivity)
	circleSensitivity_slider.grid(row=5, column=1, pady=10, padx=10)
	circleSensitivity_label_value = customtkinter.CTkLabel(master=frame, text=circleSensitivity)
	circleSensitivity_label_value.grid(row=5, column=2, pady=10, padx=10)

	# Minimum # of edge points to declare a circle
	circleEdgePoints_label = customtkinter.CTkLabel(master=frame, text="# of edge points")
	circleEdgePoints_label.grid(row=6, column=0, pady=10, padx=10)
	circleEdgePoints_slider = customtkinter.CTkSlider(master=frame, from_=4, to=100, width=400,
						number_of_steps=96, border_width=3, command=set_circleEdgePoints)
	circleEdgePoints_slider.set(circleEdgePoints)
	circleEdgePoints_slider.grid(row=6, column=1, pady=10, padx=10)
	circleEdgePoints_label_value = customtkinter.CTkLabel(master=frame, text=circleEdgePoints)
	circleEdgePoints_label_value.grid(row=6, column=2, pady=10, padx=10)

	## Sliders for camera settings
	# Brightness of capture
	cameraBrightness_label = customtkinter.CTkLabel(master=frame, text="Camera Brightness")
	cameraBrightness_label.grid(row=0, column=3, pady=10, padx=10)
	cameraBrightness_slider = customtkinter.CTkSlider(master=frame, from_=0, to=255, width=400,
						number_of_steps=255, border_width=3, command=set_brightness)
	cameraBrightness_slider.set(brightness)
	cameraBrightness_slider.grid(row=0, column=4, pady=10, padx=10)
	cameraBrightness_label_value = customtkinter.CTkLabel(master=frame, text=brightness)
	cameraBrightness_label_value.grid(row=0, column=5, pady=10, padx=10)

	# Contrast of capture
	cameraContrast_label = customtkinter.CTkLabel(master=frame, text="Camera Contrast")
	cameraContrast_label.grid(row=1, column=3, pady=10, padx=10)
	cameraContrast_slider = customtkinter.CTkSlider(master=frame, from_=0, to=255, width=400,
						number_of_steps=255, border_width=3, command=set_contrast)
	cameraContrast_slider.set(contrast)
	cameraContrast_slider.grid(row=1, column=4, pady=10, padx=10)
	cameraContrast_label_value = customtkinter.CTkLabel(master=frame, text=contrast)
	cameraContrast_label_value.grid(row=1, column=5, pady=10, padx=10)
	
	# Saturation of capture
	cameraSaturation_label = customtkinter.CTkLabel(master=frame, text="Camera Saturation")
	cameraSaturation_label.grid(row=2, column=3, pady=10, padx=10)
	cameraSaturation_slider = customtkinter.CTkSlider(master=frame, from_=0, to=255, width=400,
						number_of_steps=255, border_width=3, command=set_saturation)
	cameraSaturation_slider.set(saturation)
	cameraSaturation_slider.grid(row=2, column=4, pady=10, padx=10)
	cameraSaturation_label_value = customtkinter.CTkLabel(master=frame, text=saturation)
	cameraSaturation_label_value.grid(row=2, column=5, pady=10, padx=10)

	# Hue of capture (not applicable to camera?)
	cameraHue_label = customtkinter.CTkLabel(master=frame, text="Camera Hue")
	cameraHue_label.grid(row=3, column=3, pady=10, padx=10)
	cameraHue_slider = customtkinter.CTkSlider(master=frame, from_=0, to=255, width=400,
						number_of_steps=255, border_width=3, command=set_hue)
	cameraHue_slider.set(hue)
	cameraHue_slider.grid(row=3, column=4, pady=10, padx=10)
	cameraHue_label_value = customtkinter.CTkLabel(master=frame, text=hue)
	cameraHue_label_value.grid(row=3, column=5, pady=10, padx=10)
	

	# Gain of capture
	cameraGain_label = customtkinter.CTkLabel(master=frame, text="Camera Gain")
	cameraGain_label.grid(row=4, column=3, pady=10, padx=10)
	cameraGain_slider = customtkinter.CTkSlider(master=frame, from_=0, to=255, width=400,
						number_of_steps=255, border_width=3, command=set_gain)
	cameraGain_slider.set(gain)
	cameraGain_slider.grid(row=4, column=4, pady=10, padx=10)
	cameraGain_label_value = customtkinter.CTkLabel(master=frame, text=gain)
	cameraGain_label_value.grid(row=4, column=5, pady=10, padx=10)

	# Exposure of capture (not applicable to camera?)
	cameraExposure_label = customtkinter.CTkLabel(master=frame, text="Camera Exposure")
	cameraExposure_label.grid(row=5, column=3, pady=10, padx=10)
	cameraExposure_slider = customtkinter.CTkSlider(master=frame, from_=0, to=255, width=400,
						number_of_steps=255, border_width=3, command=set_exposure)
	cameraExposure_slider.set(exposure)
	cameraExposure_slider.grid(row=5, column=4, pady=10, padx=10)
	cameraExposure_label_value = customtkinter.CTkLabel(master=frame, text=exposure)
	cameraExposure_label_value.grid(row=5, column=5, pady=10, padx=10)

	# Buttons
	customtkinter.CTkButton(master=frame, text='Quit', command=root.quit).grid(row=7, column=1, pady=10, padx=10)
	
	root.mainloop()

def findCircles():
	# Circle from the previous frame (will represent the current detected circle)
	prevCircle = None

	# Function that calculates the square of the distance between two points in a frame
	dist = lambda x1, y1, x2, y2: (x1-x2)**2+(y1-y2)**2

	# Make sure webcam/image is accessible
	while True:
		# ret is a boolean value for whether it was able to read the frame successfully
		# frame is the captured image from the camera
		ret, frame = videoCapture.read()
			
		# If frame is not read successfully, end program
		if not ret:
			print("Couldn't read frame\n")
			break

		# Show initial frame to user on the screen
		#cv.imshow("Frame", frame)

		# Make a copy of frame where the color has been converted to grayscale
		# (Can use different color settings, but cv.HoughCircles requires a grayscale image)
		grayFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
		#cv.imshow("Grayed Frame", grayFrame)

		# Make a copy of grayFrame where the frame has been blurred
		# (Can use different blurring filters and adjust the level of blurring)
		blurFrame = cv.GaussianBlur(grayFrame, (blur,blur), 0)
		#cv.imshow("Blurred Frame", blurFrame)

		# HoughCircles tranform is not great at tracking objects quickly. An elliptical transform
		# will be better for our use, because it can track objects more quickly and we will need
		# to track objects that might not be perfect circles when viewed at an angle(elliptical).
		# Provide a frame, what gradient to use, inverse ratio of resolution, min distance between
		# the center of two circles, sensitivity to circle detection, # of edge points necessary
		# to declare a circle(more is a better circle), minimum radius for circle, max radius for
		# circle. The result will be a list of circles found
		circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, dp, minDist, param1=circleSensitivity,
								  param2=circleEdgePoints, minRadius=minRadiusVar, maxRadius=maxRadiusVar)
		
		# Are there circles detected in the frame
		if circles is not None:
			
			# Convert circles to a numpy array
			circles = np.uint16(np.around(circles))
			
			# Chosen circle from the frame 
			chosen = None

			# Iterate through array of circles
			for i in circles[0, :]:

				# If there is no circle chosen yet, set the chosen circle equal to the first circle in the array
				if chosen is None:
					chosen = i
				
				# If there is a previous circle then:
				# If the distance from the chosen circle to the previous circle is less than or equal
				# to the distance from the next circle in the array to the previous circle then
				# set the chosen circle to the next circle in the array
				if prevCircle is not None:
					if dist(chosen[0], chosen[1], prevCircle[0], prevCircle[1]) <= dist(i[0], i[1], prevCircle[0], prevCircle[1]):
						chosen = i
			
			# Draw a circle at the centerpoint of the chosen circle
			cv.circle(frame, (chosen[0], chosen[1]), 1, (0,100,100), 3)

			# Draw a circle around the circumference of the chosen circle
			cv.circle(frame, (chosen[0], chosen[1]), chosen[2], (255, 0, 255), 3)

			# Set the previous circle equal to the chosen circle at the end of the loop
			prevCircle = chosen

		# Show the original frame with the drawn circles to the user
		cv.imshow("Circles", frame)

		# Quit program if user presses the 'q' key
		if cv.waitKey(1) & 0xFF == ord('q'):
			print("Exiting program(Executed by user)\n")

			# Release webcam and close all windows
			videoCapture.release()
			cv.destroyAllWindows()
			
			sys.exit()


if __name__ == "__main__":
	# Opening message as user starts program
	print("\nFind circles within camera's frame and draw a circle around it's circumference. Press 'q' key at any time to exit.\n")
	
	t1 = Thread(target = createGUI)
	t2 = Thread(target = findCircles)

	t1.start()
	t2.start()