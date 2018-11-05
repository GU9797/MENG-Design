import numpy as np
import cv2

def write(img,location):
    cv2.imwrite(location,img)

class Image(object):

    def __init__(self, location):
        self.location = location
        self.readImage()
        self.process()
        self.getShapes()
        self.drawShapes()

    def readImage(self):
        self.image = cv2.imread(self.location)

    def process(self):
        #smooth the image with a bilateral filter
        blur = cv2.bilateralFilter(self.image,9,150,150)
        #turn everything below (limit) to black
        ret,proc = cv2.threshold(blur,100,255,cv2.THRESH_TOZERO)
        #turn everything above (limit) to white
        ret,proc = cv2.threshold(proc,180,255,cv2.THRESH_TRUNC)
        #highlight the edges with Canny edge detection
        self.processed_image = cv2.Canny(proc,100,200)
        
    def getShapes(self):
        _, contours, _ = cv2.findContours(self.processed_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        self.shapes = [Shape(contour,self) for contour in contours]
        big_shapes = []
        for shape in self.shapes:
            if shape.area>100:
                big_shapes.append(shape)
        self.big_shapes = big_shapes

    def drawShapes(self):
        big_contours = [shape.contour for shape in self.big_shapes]
        shapes_image = np.copy(self.image)
        self.shapes_image = cv2.drawContours(shapes_image, big_contours,  -1, (0,0,255), 1 )

    def splitShapes(self,shapedir):
        shapes_split = [self.shapes_image[Shape.boundary[0]:Shape.boundary[1],Shape.boundary[2]:Shape.boundary[3]]
                        for Shape in self.big_shapes]        
        idx = 0
        for shape in shapes_split:
            idx+=1
            write(shape,shapedir+str(idx)+".jpg")
        #why do we output two copies of every image??

class Shape(object):

    def __init__(self, contour, parent):
        self.contour = contour
        self.parent = parent
        self.getArea()
        self.getApprox()
        self.getBoundary()
    
    def getArea(self):
        self.area = cv2.contourArea(self.contour)

    def getApprox(self):
        self.approx = cv2.approxPolyDP(self.contour,0.01*cv2.arcLength(self.contour,True),True)

    def getBoundary(self): 
        x,y,w,h = cv2.boundingRect(self.contour)
        self.boundary = [y,y+h,x,x+w]
