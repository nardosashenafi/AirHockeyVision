# AirHockeyVision
## Author Information
- GUI
    - Roscoe Ambrose
- Camera
    - Haston LaGrone
- Calibration
    - Daniel Pullicar
    - Mason Cannon

## Needed functions to run are:
- Calibrate.py
- Calibrationfunc.py
- Caller.py
- ConvertToWorldFunc.py
- HoughCirclesClass.py


## Known issues:
- Start Program button temporarily freezes GUI until camera window is closed with 'q'.
    - Fix: maybe issue with threading
- Spamming of Start Program button is not accounted for
    - Fix: if(camera.ret) 
