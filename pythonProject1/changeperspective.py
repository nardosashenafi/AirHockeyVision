import numpy as np
import cv2 as cv

im = cv.imread(r"C:\Users\DanTehMan\Downloads\hockeytablefull.jpg")

cv.imshow('img', im)
cv.waitKey(0)
cv.waitKey(1)

rows, cols, ch = im.shape
height = 755  # (780+730)/2
width = 390  # 780/2
pts1 = np.float32(
    [[408, 197],
     [746, 202],
     [116, 626],
     [1011, 626]]
)
pts2 = np.float32(
    [[0, 0],
     [width,     0],
     [0,        height],
     [width,     height]]
)
M = cv.getPerspectiveTransform(pts1,pts2)
dst = cv.warpPerspective(im, M, (width, height))
cv.imshow('My Zen Garden', dst)
cv.waitKey()
cv.waitKey(0)
cv.destroyAllWindows()
cv.waitKey(1)