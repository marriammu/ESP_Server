import time
import cv2
from flask import Response
import numpy as np
import requests
import matplotlib.pyplot as plt
import math

def GetImageFromMobile():
    IPAddress='http://172.20.10.2'
    PortNumber=':8080'
    ImagePath='/shot.jpg'
    url=IPAddress+PortNumber+ImagePath
    print(url) 
    i=0
    while i<10:     
        ResponseImage= requests.get(url)
        ImageArray= np.array(bytearray(ResponseImage.content), dtype=np.uint8)
        Image=  cv2.imdecode(ImageArray,-1)     
        Image = cv2.cvtColor(Image, cv2.COLOR_BGR2RGB)
        if cv2.waitKey(1)==27:
            break
        i=i+1
    return Image 

def ShowImage(Image): 
    plt.figure()
    plt.imshow(Image)
    plt.xticks([]), plt.yticks([])
    plt.show()

def rotate_img(image):
    return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)

def Thresholding(Image,Low,High):
    # ShowImage(Image)
    HSVImage = cv2.cvtColor(Image, cv2.COLOR_RGB2HSV)
    # ShowImage(HSVImage)
    ImageMask=cv2.inRange(HSVImage, Low, High)
    # ShowImage(ImageMask)
    return ImageMask

def EdgeDetection(Image):
    Edges = cv2.Canny(Image, 200, 400)
    # ShowImage(Edges)
    return Edges

def CropLines(Edges):
    RowsNumber, ColumnsNumber = Edges.shape
    BlackImage = np.zeros_like(Edges)
    Polygon = np.array([[
        (0, 0.5*RowsNumber),
        (ColumnsNumber,0.5*RowsNumber),
        (ColumnsNumber, RowsNumber),
        (0, RowsNumber),]],
        np.int32)
    cv2.fillPoly(BlackImage, Polygon, 255)
    HalfImage = cv2.bitwise_and(Edges, BlackImage)
    # ShowImage(HalfImage)
    return HalfImage  

##################################################################
def DetectSegments(HalfImage):
    Rho = 1
    Angle = np.pi/180
    print(Angle)
    MinimumThreshold = 5
    LineSegmets = cv2.HoughLinesP(HalfImage, rho= Rho, theta=Angle, threshold=MinimumThreshold, lines=np.array([]), minLineLength=8, maxLineGap=2)
    return LineSegmets

def MakePoints(Image, Line):
    RowsNumber, ColumnsNumber,_ = Image.shape
    Slope, intercept = Line
    BottomOfTheImage = RowsNumber 
    MiddleOfTheImage = int(BottomOfTheImage * 1 / 2)  
    x1 = max(-ColumnsNumber, min(2 * ColumnsNumber, int((BottomOfTheImage - intercept) / Slope)))
    x2 = max(-ColumnsNumber, min(2 * ColumnsNumber, int((MiddleOfTheImage - intercept) / Slope)))
    return [[x1, BottomOfTheImage, x2, MiddleOfTheImage]]


def AverageSlopeIntercept(Image, LineSegmets):
    """
    This function combines Line segments into one or two lane lines
    If all Line slopes are < 0: then we only have detected left lane
    If all Line slopes are > 0: then we only have detected right lane
    """
    laneLines = []
    if LineSegmets is None:
        print('No lineSegment segments detected')
        #MAKE CAR STOP?
        return laneLines

    RowsNumber, ColumnsNumber,_ = Image.shape
    leftFit = []
    rightFit = []

    boundary = 1/2
    leftRegionBoundary = ColumnsNumber * (1 - boundary)
    rightRegionBoundary = ColumnsNumber * boundary

    for lineSegment in LineSegmets:
        for x1, y1, x2, y2 in lineSegment:
            if x1 == x2:
                print('skipping vertical Line segment (slope=inf): ' , lineSegment)
                continue
            fit = np.polyfit((x1, x2), (y1, y2), 1) 
            slope = fit[0]
            intercept = fit[1]
            if slope < 0:
                if x1 < leftRegionBoundary and x2 < leftRegionBoundary:
                    leftFit.append((slope, intercept))
            else:
                if x1 > rightRegionBoundary and x2 > rightRegionBoundary:
                    rightFit.append((slope, intercept))

    leftFitAverage = np.average(leftFit, axis=0)
    if len(leftFit) > 0:
        laneLines.append(MakePoints(Image, leftFitAverage))

    rightFitAverage = np.average(rightFit, axis=0)
    if len(rightFit) > 0:
        laneLines.append(MakePoints(Image, rightFitAverage))

    print('lane lines: ', laneLines) 

    return laneLines

def LaneDetection(Image, Low, High):
    # im=rotate_img(Image)
    im=Thresholding(Image, Low, High)
    edges = EdgeDetection(im)
    croppedEdges = CropLines(edges)
    croppedEdges = edges
    LineSegmets = DetectSegments(croppedEdges)
    laneLines = AverageSlopeIntercept(Image, LineSegmets)
  
    return laneLines
    # return LineSegmets

def LinesDisplaying(Image, lines, lineColor = (0,255,0), lineWidth = 20):
    lineImage = np.zeros_like(Image)
    if lines is not None:
        for Line in lines:
            for x1, y1, x2, y2 in Line:
                cv2.line(lineImage, (x1, y1), (x2, y2), lineColor, lineWidth)
    lineImage = cv2.addWeighted(Image, 0.8, lineImage, 1, 1)
    return lineImage

def SteeringAngle(Image, laneLines):
    """ Find the steering Angle based on lane Line coordinate
        We assume that camera is calibrated to point to dead center
    """
    if len(laneLines) == 0:
        print('No lane lines detected, do nothing')
        #MAKE CAR STOP?
        return -90
    RowsNumber, ColumnsNumber,_ = Image.shape
    if len(laneLines) == 1:
        print('Only detected one lane Line, just follow it. ', laneLines[0])
        x1, _, x2, _ = laneLines[0][0]
        x_offset = x2 - x1
    else: 
        print(laneLines[1][0]) 
        left_x2 = laneLines[0][0][2]
        right_x2= laneLines[1][0][2]
        print(left_x2)
        print(right_x2)
        print(ColumnsNumber)
        x_offset =int(left_x2 + right_x2- ColumnsNumber ) / 2 

    y_offset = int(RowsNumber / 2)

    angleToMidRadian = math.atan(x_offset / y_offset) 
    angleToMidDeg = int(angleToMidRadian * 180.0 / math.pi)
    steeringAngle = angleToMidDeg+90

    print('new steering Angle: ', steeringAngle)
    return steeringAngle


def displayHeadingLine(Image, steeringAngle, lineColor=(0, 0, 255), lineWidth=15):
    headingImage = np.zeros_like(Image)
    RowsNumber, ColumnsNumber,_ = Image.shape
    steeringAngleRadian = (steeringAngle / 180.0 * math.pi)
    x1 = int(ColumnsNumber / 2)
    y1 = RowsNumber
    x2 = int(x1 - RowsNumber / 2 / math.tan(steeringAngleRadian))
    y2 = int(RowsNumber / 2)

    cv2.line(headingImage, (x1, y1), (x2, y2), lineColor, lineWidth)
    headingImage = cv2.addWeighted(Image, 0.8, headingImage, 1, 1)
    # ShowImage(headingImage)
    return headingImage

# low=np.array([60,40,40])
# high=np.array([150,255,255])
# # low=np.array([36,25,25]) 
# # high=np.array([86, 255,255])
# # image=GetImageFromMobile()
# image=plt.imread('3.png')
# image=np.multiply(image,255)
# image = image.astype('uint8')
# # image=plt.imread('lane 2.jpg')
# laneLines =LaneDetection(image, low, high)
# laneLinesImage = LinesDisplaying(image, laneLines)
# steeringAngle= SteeringAngle(image, laneLines)
# currentAngle = steeringAngle
# finalImage = displayHeadingLine(laneLinesImage, currentAngle)
