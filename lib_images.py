import numpy as np
import cv2
import matplotlib.pyplot as plt
import json
import colorsys

with open('input.json') as f:
  data = json.load(f)

def write(img,location):
    cv2.imwrite(location,img)

def HSVToRGB(h, s, v):
    (r, g, b) = colorsys.hsv_to_rgb(h, s, v)
    return (int(255*r), int(255*g), int(255*b))
 
def getDistinctColors(n):
    huePartition = 1.0 / (n + 1)
    return (HSVToRGB(huePartition * value, 1.0, 1.0) for value in range(0, n))

class Image(object):

    def __init__(self, location): #location is str to image's directory
        self.location = location
        self.readImage()
        self.process()
        self.getShapes()
        self.drawShapes()

    def readImage(self):
        #read image as 2d array (grayscale)
        self.image = cv2.imread(self.location, 0)

    def process(self):
        #smooth the image with a bilateral filter
        blur = cv2.bilateralFilter(self.image,9,150,150)
        #turn everything below (limit) to black
        if data["Otsu"] == 1:
            ret,proc = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        else:
            ret,proc = cv2.threshold(blur,data["pixel_threshold"],255,cv2.THRESH_TOZERO)
            #turn everything above (limit) to white
            ret,proc = cv2.threshold(proc,data["pixel_threshold"],255,cv2.THRESH_TRUNC)
            ret,proc = cv2.threshold(proc,data["pixel_threshold"]-10,255,cv2.THRESH_BINARY)
        self.binary = proc

        #highlight the edges with Canny edge detection,may want to play around with upper/lower boundaries so edges are closed
        self.processed_image = cv2.Canny(proc,100,200)
        self.processed_image = proc
        #plt.imshow(proc)
        #plt.show()

    def getShapes(self):
        #find shapes in processed (binary) image
        #RETR_EXTERNAL worked on 30mpa image but not 100mpa? Should prevent finding duplicate shapes
        hierarchy, contours, _ = cv2.findContours(self.processed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.shapes = [Shape(contour) for contour in contours]
        #distinguish between "big" shapes
        big_shapes = []
        for shape in self.shapes:
            if shape.area>data["shape_area_pixel_minimum"] and shape.area<data["shape_area_pixel_maximum"] and (shape.h/float(shape.w)) < data["shape_side_ratio_maximum"] and (shape.w/float(shape.h)) < data["shape_side_ratio_maximum"]:
                #if cv2.isContourConvex(shape.contour) == True: #checks if contour is closed (commented bc it removes vast majority of shapes)
                big_shapes.append(shape)
        self.big_shapes = big_shapes

    def drawShapes(self):
        #draw big shapes over original image (or binary image)
        big_contours = [shape.contour for shape in self.big_shapes]        
        #shapes_image = np.copy(self.binary)
        shapes_image = np.copy(self.image)
        shapes_image = cv2.cvtColor(shapes_image, cv2.COLOR_GRAY2RGB) #change back to RGB for easier visualization
        self.shapes_image = cv2.drawContours(shapes_image, big_contours,  -1, (0,0,255), 1 )
        #plt.imshow(self.shapes_image)
        #plt.show()

    def splitShapes(self,shapedir):
        #crop each shape
        shapes_split = [bshape.crop(self.image) for bshape in self.big_shapes]
        idx = 0
        for shape in shapes_split:
            idx += 1
            name = self.location[-5] + "_" + str(len(self.big_shapes))+ "_" + str(idx)
            write(shape,shapedir+name+".jpg")

    def writeLabels(self,target):
        idx = 0
        for shape in self.big_shapes:
            idx+=1
            name = self.location[-5] + "_" + str(len(self.big_shapes))+ "_" + str(idx)
            loc = target+str(shape.label[0])+"/"+name+".jpg"
            write(shape.cropped, loc)

    def drawLabels(self):
        clusters_image = np.copy(self.image)
        clusters_image = cv2.cvtColor(clusters_image, cv2.COLOR_GRAY2RGB) #change back to RGB for easier visualization

        k = np.amax([shape.label[0] for shape in self.big_shapes])+1 
        cluster_contours = [[] for i in range(k)]
        colors = getDistinctColors(k)

        for shape in self.big_shapes:
            cluster_contours[shape.label[0]].append(shape.contour)
        
        for i in range(len(cluster_contours)):
            clusters_image = cv2.drawContours(clusters_image,cluster_contours[i],-1,next(colors),3)
        
        self.clusters_image = clusters_image

class Shape(object):

    def __init__(self, contour):
        self.contour = contour
        self.label = False
        self.getArea()
        self.getApprox()
        self.getBoundary()

    def getArea(self):
        self.area = cv2.contourArea(self.contour)

    def getApprox(self):
        self.approx = cv2.approxPolyDP(self.contour,0.01*cv2.arcLength(self.contour,True),True)

    def getBoundary(self):
        x,y,w,h = cv2.boundingRect(self.contour)
        self.h = h #height
        self.w = w #width
        self.boundary = [y,y+h,x,x+w]

    def crop(self,parent):
        peri = cv2.arcLength(self.contour, True)
        approx = cv2.approxPolyDP(self.contour, 0.02 * peri, True) #approximate shape of contour
        canvas = np.zeros(parent.shape).astype(parent.dtype) + 255 # create a single channel pixel white image
        fill = cv2.fillPoly(canvas, pts =[self.contour], color=0)
        anti_fill = cv2.bitwise_or(parent,fill) #keep shape in grayscale, turn background white
        self.cropped = anti_fill[self.boundary[0]:self.boundary[1],self.boundary[2]:self.boundary[3]]
        #also crop to slightly larger than boundary so shape isn't right at the edge of the image
        #this will be useful if we want to draw more contours on a shape after cropping it
        self.border = 2
        self.bordered = anti_fill[self.boundary[0]-self.border:self.boundary[1]+self.border,self.boundary[2]-self.border:self.boundary[3]+self.border]
        return(self.cropped)

    def pad(self,maxh,maxw):
        self.padded = np.pad(self.cropped,((0, maxh - self.h), (0, maxw - self.w)), 'constant', constant_values=0)

    def flatten(self):
        #when clustering, each shape is represented as a single row of values
        #only flatten AFTER padding
        self.flat = np.ndarray.flatten(self.padded)

    def setLabel(self,label):
        self.label = label
