import cv2 as cv
import numpy as np

def findCircles():
	# Access webcam(# is the port of webcam)
	videoCapture = cv.VideoCapture(0)

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
		blurFrame = cv.GaussianBlur(grayFrame, (17,17), 0)
		#cv.imshow("Blurred Frame", blurFrame)

		# HoughCircles tranform is not great at tracking objects quickly. An elliptical transform
		# will be better for our use, because it can track objects more quickly and we will need
		# to track objects that might not be perfect circles when viewed at an angle(elliptical).
		# Provide a frame, what gradient to use, inverse ratio of resolution, min distance between the center of 
		# two circles, sensitivity to circle detection, # of edge points necessary to declare a circle(more is a better circle),
		# minimum radius for circle, max radius for circle. The result will be a list of circles found
		circles = cv.HoughCircles(blurFrame, cv.HOUGH_GRADIENT, 1.2, 100, param1=100, param2=50, minRadius=75, maxRadius=400)
		
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
			break

	# Release webcam and close all windows
	videoCapture.release()
	cv.destroyAllWindows()

if __name__ == "__main__":
	# Opening message as user starts program
	print("\nFind circles within camera's frame and draw a circle around it's circumference. Press 'q' key at any time to exit.\n")

	findCircles()