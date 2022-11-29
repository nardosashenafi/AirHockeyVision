import cv2 as cv
import numpy as np
import sys
from threading import Thread
from tkinter import *


def createGUI():
	global blur_slider, dp_slider, minDist_slider, minRadius_slider, maxRadius_slider
	global circleSensitivity_slider, circleEdgePoints_slider
	global cameraBrightness_slider, cameraContrast_slider, cameraSaturation_slider
	global cameraHue_slider, cameraGain_slider, cameraExposure_slider

	root = Tk()
	root.title('Light/Camera Settings')
	root.iconbitmap('C:/Users/rosco/OneDrive/Documents/ECE 480/Main Project/Code/AirHockeyIcon.ico')
	root.geometry('1150x768')
	root.resizable(0,0)

	## Sliders for circle detecting algorithm
	# Blur level of frame
	blur_label = Label(root, text="Blur")
	blur_label.grid(row=0, column=0, pady=1, padx=1)
	blur_slider = Scale(root, from_=1, to=55, length=400, tickinterval=18, resolution=2,
						troughcolor='#ff00ff', bd=3, orient=HORIZONTAL)
	blur_slider.set(17)
	blur_slider.grid(row=0, column=1, pady=10, padx=10)

	# dp inverse ratio of resolution
	dp_label = Label(root, text="dp")
	dp_label.grid(row=1, column=0, pady=1, padx=1)
	dp_slider = Scale(root, from_=1, to=5, length=400, tickinterval=0.4, resolution=0.05,
					  troughcolor='#ff00ff', bd=3, orient=HORIZONTAL)
	dp_slider.set(1.2)
	dp_slider.grid(row=1, column=1, pady=10, padx=1)

	# Minimum distance between circles
	minDist_label = Label(root, text="MinDist")
	minDist_label.grid(row=2, column=0, pady=1, padx=1)
	minDist_slider = Scale(root, from_=1, to=1001, length=400, tickinterval=100, resolution=1,
						   troughcolor='#ff00ff', bd=3, orient=HORIZONTAL)
	minDist_slider.set(501)
	minDist_slider.grid(row=2, column=1, pady=10, padx=1)

	# Minimum radius of circle
	minRadius_label = Label(root, text="MinRadius")
	minRadius_label.grid(row=3, column=0, pady=1, padx=1)
	minRadius_slider = Scale(root, from_=1, to=201, length=400, tickinterval=20, resolution=1,
						   troughcolor='#ff00ff', bd=3, orient=HORIZONTAL)
	minRadius_slider.set(1)
	minRadius_slider.grid(row=3, column=1, pady=10, padx=1)

	# Maximum radius of circle
	maxRadius_label = Label(root, text="MaxRadius")
	maxRadius_label.grid(row=4, column=0, pady=1, padx=1)
	maxRadius_slider = Scale(root, from_=1, to=401, length=400, tickinterval=40, resolution=1,
						   troughcolor='#ff00ff', bd=3, orient=HORIZONTAL)
	maxRadius_slider.set(200)
	maxRadius_slider.grid(row=4, column=1, pady=10, padx=1)

	# Sensitivity to circle detection
	circleSensitivity_label = Label(root, text="Circle Sensitivity")
	circleSensitivity_label.grid(row=5, column=0, pady=1, padx=1)
	circleSensitivity_slider = Scale(root, from_=1, to=201, length=400, tickinterval=20, resolution=1,
						   troughcolor='#ff00ff', bd=3, orient=HORIZONTAL)
	circleSensitivity_slider.set(100)
	circleSensitivity_slider.grid(row=5, column=1, pady=10, padx=1)

	# Minimum # of edge points to declare a circle
	circleEdgePoints_label = Label(root, text="# of edge points")
	circleEdgePoints_label.grid(row=6, column=0, pady=1, padx=1)
	circleEdgePoints_slider = Scale(root, from_=4, to=104, length=400, tickinterval=10, resolution=1,
						   troughcolor='#ff00ff', bd=3, orient=HORIZONTAL)
	circleEdgePoints_slider.set(50)
	circleEdgePoints_slider.grid(row=6, column=1, pady=10, padx=1)

	## Sliders for camera settings
	# Brightness of capture (might be to 255 but can't tell a difference between 250 and 255)
	cameraBrightness_label = Label(root, text="Camera Brightness")
	cameraBrightness_label.grid(row=0, column=2, pady=1, padx=1)
	cameraBrightness_slider = Scale(root, from_=0, to=250, length=400, tickinterval=25,
						resolution=1, troughcolor='#12ddff', bd=3, orient=HORIZONTAL)
	cameraBrightness_slider.set(100)
	cameraBrightness_slider.grid(row=0, column=3, pady=10, padx=10)

	# Contrast of capture (might be to 255 but can't tell a difference between 250 and 255)
	cameraContrast_label = Label(root, text="Camera Contrast")
	cameraContrast_label.grid(row=1, column=2, pady=1, padx=1)
	cameraContrast_slider = Scale(root, from_=0, to=250, length=400, tickinterval=25,
						resolution=1, troughcolor='#12ddff', bd=3, orient=HORIZONTAL)
	cameraContrast_slider.set(75)
	cameraContrast_slider.grid(row=1, column=3, pady=10, padx=10)
	
	# Saturation of capture (might be to 255 but can't tell a difference between 250 and 255)
	cameraSaturation_label = Label(root, text="Camera Saturation")
	cameraSaturation_label.grid(row=2, column=2, pady=1, padx=1)
	cameraSaturation_slider = Scale(root, from_=0, to=250, length=400, tickinterval=25,
						resolution=1, troughcolor='#12ddff', bd=3, orient=HORIZONTAL)
	cameraSaturation_slider.set(125)
	cameraSaturation_slider.grid(row=2, column=3, pady=10, padx=10)

	# Hue of capture (not applicable to camera?)
	cameraHue_label = Label(root, text="Camera Hue")
	cameraHue_label.grid(row=3, column=2, pady=1, padx=1)
	cameraHue_slider = Scale(root, from_=0, to=250, length=400, tickinterval=25,
						resolution=1, troughcolor='#12ddff', bd=3, orient=HORIZONTAL)
	cameraHue_slider.set(0)
	cameraHue_slider.grid(row=3, column=3, pady=10, padx=10)

	# Gain of capture (might be to 255 but can't tell a difference between 250 and 255)
	cameraGain_label = Label(root, text="Camera Gain")
	cameraGain_label.grid(row=4, column=2, pady=1, padx=1)
	cameraGain_slider = Scale(root, from_=0, to=250, length=400, tickinterval=25,
						resolution=1, troughcolor='#12ddff', bd=3, orient=HORIZONTAL)
	cameraGain_slider.set(0)
	cameraGain_slider.grid(row=4, column=3, pady=10, padx=10)

	# Exposure of capture (not applicable to camera?)
	cameraExposure_label = Label(root, text="Camera Exposure")
	cameraExposure_label.grid(row=5, column=2, pady=1, padx=1)
	cameraExposure_slider = Scale(root, from_=0, to=250, length=400, tickinterval=25,
						resolution=1, troughcolor='#12ddff', bd=3, orient=HORIZONTAL)
	cameraExposure_slider.set(0)
	cameraExposure_slider.grid(row=5, column=3, pady=10, padx=10)

	# Buttons
	Button(root, text='Quit', command=root.quit).grid(row=7, column=1, sticky=SW, pady=10, padx=1)

	root.mainloop()

def findCircles():
	# Access webcam(# is the port of webcam)
	videoCapture = cv.VideoCapture(0)

	# Circle from the previous frame (will represent the current detected circle)
	prevCircle = None

	# Function that calculates the square of the distance between two points in a frame
	dist = lambda x1, y1, x2, y2: (x1-x2)**2+(y1-y2)**2

	# Make sure webcam/image is accessible
	while True:
		#Global variables from sliders in GUI
		global blur_slider, dp_slider, minDist_slider, minRadius_slider, maxRadius_slider
		global circleSensitivity_slider, circleEdgePoints_slider
		global cameraBrightness_slider, cameraContrast_slider, cameraSaturation_slider
		global cameraHue_slider, cameraGain_slider, cameraExposure_slider

		#Assign variables from respective slider position
		blur = blur_slider.get()
		dp = dp_slider.get()
		minDist = minDist_slider.get()
		minRadiusVar = minRadius_slider.get()
		maxRadiusVar = maxRadius_slider.get()
		circleSensitivity = circleSensitivity_slider.get()
		circleEdgePoints = circleEdgePoints_slider.get()

		# Update settings of capture device
		videoCapture.set(cv.CAP_PROP_BRIGHTNESS, cameraBrightness_slider.get())
		videoCapture.set(cv.CAP_PROP_CONTRAST, cameraContrast_slider.get())
		videoCapture.set(cv.CAP_PROP_SATURATION, cameraSaturation_slider.get())
		videoCapture.set(cv.CAP_PROP_HUE, cameraHue_slider.get())
		videoCapture.set(cv.CAP_PROP_GAIN, cameraGain_slider.get())
		videoCapture.set(cv.CAP_PROP_EXPOSURE, cameraExposure_slider.get())

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
		
		#Are there circles detected in the frame
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