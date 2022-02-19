import cv2
import numpy as np


def empty(a):
    pass

cv2.namedWindow("Threshold for Canny")
cv2.resizeWindow("Threshold for Canny",400,240)
cv2.createTrackbar("Threshold1","Threshold for Canny",23,255,empty)
cv2.createTrackbar("Threshold2","Threshold for Canny",22,255,empty)

"""
stack image function :
courtesy @ShyamDev12

"""
def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def getContours(img,imgContour):

    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    cv2.drawContours(imgContour,contours,-1,(255, 0, 0), 2)
    """ for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area>500:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            #print(peri)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            print(len(approx))
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

            if objCor ==3: objectType ="Tri"
            elif objCor == 4:
                aspRatio = w/float(h)
                if aspRatio >0.98 and aspRatio <1.03: objectType= "Square"
                else:objectType="Rectangle"
            elif objCor>4: objectType= "Circles"
            else:objectType="None"



            cv2.rectangle(imgContour,(x,y),(x+w,y+h),(0,255,0),2)
            cv2.putText(imgContour,objectType,
                        (x+(w//2)-10,y+(h//2)-10),cv2.FONT_HERSHEY_COMPLEX,0.7,
                        (0,0,0),2)
 """

if __name__ == "__main__":
    """
    Algorithm to find the contours : that are outlines that bound the shape or form of an object
    output gives the number of corner points along with the area od the shape.

    """
    
    img = cv2.imread(r"C:\Users\manda\Documents\Python Scripts\images\shapes.png") 
    
    #using raw (r) because SyntaxError: (unicode error) ‘unicodeescape’ codec can’t ...
    #decode bytes in position 2-3: truncated \UXXXXXXXX escape
    
    imgContour = img.copy()

    while True:
        imgBlur = cv2.GaussianBlur(img,(3,3),1)

        imgGray = cv2.cvtColor(imgBlur,cv2.COLOR_BGR2GRAY)

        #canny edge detector
        imgCanny = cv2.Canny(imgGray,threshold1=cv2.getTrackbarPos("Threshold1","Threshold for Canny"),threshold2=cv2.getTrackbarPos("Threshold2","Threshold for Canny"))

        kernels = np.ones((5,5))
        imgDil= cv2.dilate(imgCanny,kernels,iterations=1)
        getContours(imgCanny,imgContour)

        imgBlank = np.zeros_like(img)

        imgStack = stackImages(0.5,([img,imgGray,imgCanny],
                                    [imgDil,imgContour,imgBlank]))

        cv2.imshow("Stack", imgStack)
        if cv2.waitKey(1) & 0XFF == ord('q'):
            break

    #cv2.waitKey(0)