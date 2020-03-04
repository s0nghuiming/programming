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
IM_FN = "2.png"


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
#3tunnel picture print("Origin image(  0,  0): \n" + str(im[0:10, 0:10]) )

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
print("Gray image(  0,  0): \n" + str(gray[0:10, 0:10]) )


#
gray2_1 = shift(gray, 1, cval=np.NaN)
gray2 = gray2_1
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(gray2)) )
print( "shape:   " + str(gray2.shape) )
print( "len:     " + str(len(gray2)) )
print( "Data type: " + str(gray2.dtype))

cv2.imshow('Gray2 image', gray2)

print("Moved Gray image(  0,  0): \n" + str(gray2[0:10, 0:10]) )


# gray2 - gray
gray3 = gray2 - gray
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(gray3)) )
print( "shape:   " + str(gray3.shape) )
print( "len:     " + str(len(gray3)) )
print( "Data type: " + str(gray3.dtype))

cv2.imshow('Gray3 image', gray3)

print("Image plus(  0,  0): \n" + str(gray3[0:10, 0:10]) )


# gray - gray
gray2_2 = shift(gray, -1, cval=np.NaN)
gray4 = gray2_2 - gray
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(gray4)) )
print( "shape:   " + str(gray4.shape) )
print( "len:     " + str(len(gray4)) )
print( "Data type: " + str(gray4.dtype))

cv2.imshow('Gray4 image', gray4)

print("Image plus 2(  0,  0): \n" + str(gray4[0:10, 0:10]) )


""" Write image file """
cv2.imwrite("outline.png", gray3)


# combine gray3 and gray4
# [ [ 0 if j <= 127 else 255 for j in i ] for i in B ]
outline = np.array(
        [ [ 0 if j <= 127 else 255 for j in i ] for i in gray3 + gray4 ],
        dtype='uint8'
        )

print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(outline)) )
print( "shape:   " + str(     outline.shape) )
print( "len:     " + str( len(outline)) )
print( "Data type: " + str(   outline.dtype))

print("Image plus 2(  0,  0): \n" + str(outline[0:10, 0:10]) )
cv2.imshow('Outline image', outline)


# cv2 needs destroy window
cv2.waitKey(0)
cv2.destroyAllWindows()
