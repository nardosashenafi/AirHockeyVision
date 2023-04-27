# AirHockeyVision

## Needed functions to run are:
- Calibrate.py
- Calibrationfunc.py
- Caller.py
- ConvertToWorldFunc.py
- HoughCirclesClass.py


## Known issues:
- Start Program button temporarily freezes GUI until camera window is closed with 'q'.
- Spamming of Start Program button is not accounted for
    - Fix: if(camera.ret) 
