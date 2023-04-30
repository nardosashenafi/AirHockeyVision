# AirHockeyVision
## Author Information
- GUI
    - Roscoe Ambrose
- OpenCV Camera Manipulation and Configuration
    - Haston LaGrone
- OpenCV Camera Calibration
    - Daniel Pullicar
    - Mason Cannon

## Required files to run are:
- AirHockeyIcon.ico
- Calibrate.py
- Calibrationfunc.py
- Caller.py
- ConvertToWorldFunc.py
- HoughCirclesClass.py


## Known issues:
- Start Program button temporarily freezes GUI until camera window is closed with 'q'.
    - Fix: Maybe issue with threading.
- Spamming of Start Program button is not accounted for
    - Fix: if(camera.ret) 
