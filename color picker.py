import cv2
import numpy as np

cap = cv2.VideoCapture(0)
cap.set(3,200)
cap.set(4,200)
cap.set(10,150)

def empty(a):
    pass
def stackImages(imgArray,scale,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver


cv2.namedWindow('taskbar')
cv2.resizeWindow('taskbar',640,380)
cv2.createTrackbar('hmin','taskbar',0,179,empty)
cv2.createTrackbar('smin','taskbar',0,255,empty)
cv2.createTrackbar('vmin','taskbar',0,255,empty)
cv2.createTrackbar('hmax','taskbar',179,179,empty)
cv2.createTrackbar('smax','taskbar',255,255,empty)
cv2.createTrackbar('vmax','taskbar',255,255,empty)

while True:
    _,img = cap.read()
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    hmin = cv2.getTrackbarPos("hmin",'taskbar')
    smin = cv2.getTrackbarPos("smin",'taskbar')
    vmin = cv2.getTrackbarPos("vmin",'taskbar')
    hmax = cv2.getTrackbarPos("hmax",'taskbar')
    smax = cv2.getTrackbarPos("smax",'taskbar')
    vmax = cv2.getTrackbarPos("vmax",'taskbar')

    lower = np.array([hmin,smin,vmin])
    upper = np.array([hmax,smax,vmax])
    mask = cv2.inRange(imghsv,lower,upper)
    result = cv2.bitwise_and(img,img,mask=mask)
    # cv2.imshow('1',img)
    # cv2.imshow('2',mask)
    # cv2.imshow('3',result)
    stack = stackImages([[img,imghsv],
                         [mask,result] ],0.6)
    cv2.imshow('stack',stack)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
