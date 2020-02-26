#coding:utf-8
#from PIL import Image
import os
import cv2
import numpy as np
from scipy import signal


""" 
"""

""" Read image file """ 
IM_FN = "C:\\Users\\songhu1x\\Pictures\\Pillow\\Untitled.png"


# Origin image
im = cv2.imread(IM_FN)
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(im)) )
print( "shape:   " + str(im.shape) )
print( "len:     " + str(len(im)) )

#print(im[0][0])
#print(im[64][64])
#[255 255 255]
#[0 0 0]

shape = im.shape
cv2.imshow('image', im)

# Gray image convertion.
gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
print( "# " + "-" * 20 + " #" )
print( "type:    " + str(type(gray)) )
print( "shape:   " + str(gray.shape) )
print( "len:     " + str(len(gray)) )

#print(gray[0][0])
#print(gray[64][64])
#255
#0

cv2.imshow('Gray image', gray)


# Conv handler
f = np.array([
    [0, 2, 0],
    [2,2,2],
    [0,2,0]
    ])
g = np.array([
    [   1,  1,  1   ],
    [   1,  -7, 1   ],
    [   1,  1,  1   ]
    ])

print(g.shape)
grad = signal.convolve2d(f, g, boundary='symm', mode='same')

print(grad)

""" Write image file """
#IM_FN = "C:\\Users\\songhu1x\\Pictures\\Pillow\\Untitled.png"


# cv2 needs destroy window
cv2.waitKey(0)
cv2.destroyAllWindows()
