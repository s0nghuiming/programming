#coding:utf-8
#from PIL import Image
import os
import cv2
import numpy as np
from scipy import signal


""" 
"""

""" Read image file """ 
IM_FN = "C:/Users/songhu1x/Pictures/Pillow/Untitled.png"


# Origin image
#   with shape = 128 * 128 * 3
#        datatype = uint8
im = cv2.imread(IM_FN)
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(im)) )
print( "shape:   " + str(im.shape) )
print( "len:     " + str(len(im)) )
print( "Data type: " + str(im.dtype))

cv2.imshow('image', im)

# Gray image
#   with shape = 128 * 128
#        datatype = uint8
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(gray)) )
print( "shape:   " + str(gray.shape) )
print( "len:     " + str(len(gray)) )
print( "Data type: " + str(gray.dtype))

cv2.imshow('Gray image', gray)


# Conv handler

# g is for periphery of a image
g = np.array([
    [   1,  1,  1   ],
    [   1,  -7, 1   ],
    [   1,  1,  1   ]
    ])

scharr = np.array([[ -3-3j, 0-10j,  +3 -3j], # not tested successfully
                   [-10+0j, 0+ 0j, +10 +0j],
                   [ -3+3j, 0+10j,  +3 +3j]])


# Conv2d on gray image
grad = signal.convolve2d(gray, g, boundary='symm', mode='same')

print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(grad)) )
print( "shape:   " + str(grad.shape) )
print( "len:     " + str(len(grad)) )
print( "Data type: " + str(grad.dtype))

# Normalize the image with its depth
grad_norm = cv2.normalize(grad, None, 255, 0, cv2.NORM_MINMAX, cv2.CV_8UC1)

print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(grad_norm)) )
print( "shape:   " + str(grad_norm.shape) )
print( "len:     " + str(len(grad_norm)) )
print( "Data type: " + str(grad_norm.dtype))

cv2.imshow('Grad image', grad_norm)


""" Write image file """
#IM_FN = "C:\\Users\\songhu1x\\Pictures\\Pillow\\Untitled.png"

cv2.imwrite("grad_norm.png", grad_norm)


# cv2 needs destroy window
cv2.waitKey(0)
cv2.destroyAllWindows()
