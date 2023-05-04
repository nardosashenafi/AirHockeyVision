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
- CameraArraysdefault.npz
- ProgramVariablesDefault.npz


## Known issues:
- Start Program button temporarily freezes GUI until camera window is closed with 'q'.
    - Fix: Issue with threading (GUI is waiting until camera window is closed, because it starts a while loop)
- Run Calibration button will crash the program if the camera window is open still
    - Workaround: Press End Program button first, then press Run Calibration button
    - Fix: Not sure yet
- Spamming of Start Program button is not accounted for
    - Fix: if(camera.ret) 
