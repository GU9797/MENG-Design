import numpy as np
import cv2

im = cv2.imread('./images/playground/pinj100mpacontrast.jpg')
'''
ret,thresh = cv2.threshold(im,127,255,0)
image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
img = cv2.drawContours(image, contours, -1, (0,255,0), 3)
'''
bilateral_filtered_image = cv2.bilateralFilter(im, 5, 175, 175)
#cv2.imshow('Bilateral', bilateral_filtered_image)
edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 200)
#cv2.imshow('Edge', edge_detected_image)
_, contours, _= cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contour_mlist = []
contour_slist = []
contour_llist = []
for contour in contours:
    approx = cv2.approxPolyDP(contour,0.01*cv2.arcLength(contour,True),True)
    area = cv2.contourArea(contour)
    if ((len(approx) > 8) & (area > 30)):
        contour_mlist.append(contour)
cv2.drawContours(im, contour_mlist,  -1, (0,0,255), 2)
#cv2.drawContours(im, contour_slist,  -1, (255,0,0), 2)
cv2.imshow('Objects Detected',im)
cv2.imwrite('./images/playground/pinj100mpashapes.jpg',im)
