import cv2
import pyautogui as pg
import time
import os
import handtrackingmodule as nh
import numpy as np

#############################
whcam,hhcam = 640,488
frameR= 100
smoothening = 7
pg.FAILSAFE= False
#############################
pTime = 0
plocx,plocy = 0,0
clocx,clocy= 0,0

cap= cv2.VideoCapture(0)
cap.set(3, whcam)
cap.set(4, hhcam)
detector= nh.handDetector(maxHands=1)
wScr, hScr=pg.size()


while True:
    check, img = cap.read()
    img = cv2.flip(img, 1)
    img= detector.findHands(img)
    lmList, bbox = detector.findposition(img)

    if len(lmList)!=0:
        x1, y1 = lmList[8][1:]
        x2,y2 = lmList[12][1:]

        fingres = detector.fingreup()
        cv2.rectangle(img,(frameR, frameR),(whcam- frameR, hhcam-frameR),
        (255,0,255), 2)

        if fingres[1]== 1 and fingres[2]== 0 and fingres[3]==0:
            x2,y2=lmList[12][1:]

            x3 = np.interp(x1, (frameR, whcam- frameR), (0,wScr))
            y3 = np.interp(y1, (frameR, hhcam- frameR), (0,hScr))
            clocx=plocx +(x3 - plocx)/smoothening
            clocy=plocy +(y3 - plocy)/smoothening

            pg.moveTo(x3,y3)

            cv2.circle(img, (x1,y1),15, (255,0,255),cv2.FILLED)

        if  fingres[1]==1 and fingres[2]==1:
            length,img,lineInfo= detector.findDistance(8,12,img)
            print(length)
            if length < 20:
                cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (255,0,255),cv2.FILLED)

                pg.click()
                pg.sleep(0)



        if  fingres[1]==1 and fingres[3]==1:
             length,img,lineInfo=detector.findDistance(8,16,img)
             print(length)
             if length < 40:
                 #cv2.circle(img, (lineInfo[4], lineInfo[5]),15, (255,0,255),cv2.FILLED)
                 pg.click(button="right")
                 pg.sleep(0)


    cTime = time.time()
    fps= 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img,str(int(fps)),(40,50),cv2.FONT_HERSHEY_SIMPLEX,3,(255,0,0),3)
    cv2.imshow("img",img)
    key=cv2.waitKey(1) 
    if key==27:
        break               