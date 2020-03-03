#coding:utf-8
#from PIL import Image
import os
import cv2
import numpy as np
from scipy import signal
from scipy.ndimage.interpolation import shift


""" 
"""

""" Read image file """ 
IM_FN = "C:/Users/songhu1x/Pictures/Pillow/Untitled2.png"


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


#
gray2 = shift(gray, 1, cval=np.NaN)
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(gray2)) )
print( "shape:   " + str(gray2.shape) )
print( "len:     " + str(len(gray2)) )
print( "Data type: " + str(gray2.dtype))

cv2.imshow('Gray2 image', gray2)


print("(  1,  1): \n" + str(gray2[1:4, 1:4]) )

""" Write image file """
#IM_FN = "C:\\Users\\songhu1x\\Pictures\\Pillow\\Untitled.png"

#cv2.imwrite("grad_norm.png", grad_norm)


# cv2 needs destroy window
cv2.waitKey(0)
cv2.destroyAllWindows()
