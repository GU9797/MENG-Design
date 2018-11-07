import numpy as np
import cv2
from lib_images import *

def maxdim(shapes):
    maxh = 0
    maxw = 0
    for shape in shapes:
        if shape.h > maxh:
            maxh = shape.h
        if shape.w > maxw:
            maxw = shape.w
    return(maxh,maxw)

def kmeans(shapes,k=2):
    #prepare shapes
    maxh,maxw = maxdim(shapes)
    for shape in shapes:
        shape.pad(maxh,maxw)
        shape.flatten()
    rows = [shape.flat for shape in shapes]
 
    Z = np.stack(rows)
    Z = np.float32(Z)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)    
    ret,label,center=cv2.kmeans(Z,k,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)
   
    #assign a label to each shape
    for i in range(len(shapes)):
        shapes[i].setLabel(label[i])

    return(ret,label,center)
