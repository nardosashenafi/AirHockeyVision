from HoughCirclesClass import *
from threading import Thread

def main():
	cameraPort = 0
	testMode = 1 # 0 = run mode, 1 = test mode
	#camera,blur,dp,minDist,minRadius,maxRadius,circleSensitivity,circleEdgePoints,brightness,contrast,saturation,hue,gain,exposure,tog_autoE,focus,tog_autoF,cameraNumber,width,height,fps
	camera = CircleDetectionTestModeWindows(17,1.2,10000,5,50,100,40,175,75,125,0,10,-7,0,255,1,cameraPort,1280,720,60)
	Thread(target = camera.createGUI).start()
	Thread(target = camera.detectionProgram(testMode)).start()

if __name__ == "__main__":
	main()
