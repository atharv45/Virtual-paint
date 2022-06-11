import cv2
import numpy as np

framewidth = 480
frameheight = 640

cap = cv2.VideoCapture(0)
cap.set(3,framewidth)
cap.set(4,frameheight)
cap.set(10,150)  #todo 3,4,10 for width height brightness

mycolors= [ [0,118,100,17,202,255],   #orange
            [46,42,162,127,255,255],  #blue
            [18,73,54,73,255,255] ]  #yellow

mycolorvalues= [ [0,128,255],   #todo BGR format
                 [204,204,0],
                 [0,255,255]]

mypoints= [ ]  #x , y , countid

def find_colors(img,mycolors,mycolorvalues):
    imghsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    count=0
    newpoints=[]
    for color in mycolors:
        lower = np.array(color[:3])
        upper = np.array(color[3:])
        mask = cv2.inRange(imghsv,lower,upper)
        x,y = get_contours(mask)
        # cv2.imshow(str(color[0]),mask)
        cv2.circle(copyimage,(x,y), 10, mycolorvalues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newpoints.append([x,y,count])
        count+=1
    return newpoints


def get_contours(img):
    contours, hirarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h, =0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>300:
            # cv2.drawContours(copyimage,cnt,-1,(255,0,0),3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x,y,w,h, = cv2.boundingRect(approx)
    return x+w//2,y

def draw_on_canvas(mypoints,myvaluescount):
    for point in mypoints:
        cv2.circle(copyimage,(point[0],point[1]), 20, myvaluescount[point[2]],cv2.FILLED)

while True:
    sucess, img = cap.read()
    copyimage = img.copy()
    newpoints = find_colors(img, mycolors,mycolorvalues)
    if len(newpoints) !=0:
        # print('newpoints',newpoints)
        for newp in newpoints:
            # print('newp',newp)
            mypoints.append(newp)
    if len(mypoints)!=0:
        draw_on_canvas(mypoints,mycolorvalues)
    cv2.imshow("result", copyimage)
    if cv2.waitKey(1) & 0xff == ord('q'):
        break
