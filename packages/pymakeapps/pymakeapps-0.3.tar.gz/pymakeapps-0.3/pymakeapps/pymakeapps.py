import cv2
import numpy as np
import time
import autopy
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class htm():
    class handDetector():
        def __init__(self, mode=False,maxHands=2,detectionCon=0.5,trackCon=0.5):
            self.mode = mode
            self.maxHands = maxHands
            self.detectionCon = detectionCon
            self.trackCon = trackCon
            
            self.mpHands = mp.solutions.hands
            self.hands = self.mpHands.Hands(self.mode,self.maxHands,
                                            self.detectionCon,self.trackCon)
            self.mpDraw = mp.solutions.drawing_utils

            self.tipIds = [4, 8, 12, 16, 20]
        def findHands(self, img,draw = True):
            
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(imgRGB)
            #print(results.multi_hand_landmarks)
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:
                    if draw:
                        self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
            return img           
                        
        def findPosition(self, img, handNo=0, draw = True):
            xList = []
            yList = []
            bbox = []
            self.lmList = []
            if self.results.multi_hand_landmarks:
                myHand = self.results.multi_hand_landmarks[handNo]
                for id , lm in enumerate(myHand.landmark):
                    # print(id, lm)
                    h, w, c = img.shape
                    cx, cy = int(lm.x*w), int(lm.y*h)
                    xList.append(cx)
                    yList.append(cy)
                    #print(id,cx, cy)
                    self.lmList.append([id, cx, cy])
                    if draw:
                        cv2.circle(img, (cx, cy), 5, (0,0,255),cv2.FILLED)
                xmin, xmax = min(xList), max(xList)
                ymin, ymax = min(yList), max(yList)
                bbox = xmin, ymin, xmax, ymax
                if draw:
                    cv2.rectangle(img, (bbox[0]-20,bbox[1]-20),
                            (bbox[2]+20,bbox[3]+20),(0,255,0),2)
                
            return self.lmList, bbox
        def findDistance(self,p1,p2,img,draw=True):
            x1,y1 = self.lmList[p1][1],self.lmList[p1][2]
            x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
            cx, cy = (x1+x2) //2, (y1 +y2) //2

            if draw:
                cv2.circle(img,(x1,y1), 10, (0,255,0), cv2.FILLED)
                cv2.circle(img,(x2,y2), 10, (0,255,0), cv2.FILLED)
                cv2.line(img, (x1,y1), (x2,y2), (255,0,255),3)
                cv2.circle(img,(cx,cy), 10, (255,0,255), cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            return length,img,[x1,y1,x2,y2,cx,cy]
            
        def FINGUP(self):
            fingers = []

            if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
                
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            return fingers
        def fingersUp(self):
            if self.results.multi_hand_landmarks:
                myHandType = self.handType()
                fingers = []
                # Thumb
                if myHandType == "Right":
                    if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if self.lmList[self.tipIds[0]][1] < self.lmList[self.tipIds[0] - 1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                # 4 Fingers
                for id in range(1, 5):
                    if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
            return fingers
        def handType(self):
            if self.results.multi_hand_landmarks:
                if self.lmList[17][1] < self.lmList[5][1]:
                    return "Right"
                else:
                    return "Left"

            

    def main():
        pTime = 0
        cTime = 0
        cap = cv2.VideoCapture(0)
        detector = htm.handDetector()
        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img)
            #if len(lmList) !=0 :
                #print(lmList[4])
                
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,
                        (255,0,255), 3)
                    
            cv2.imshow("WebCam", img)
            cv2.waitKey(1)

        if __name__ == "__main__":
            main()

class HandProjects():
    def Mouse(smoothening=20):

        wCam, hCam = 640,480

        frameR = 100 #CV2.REC

        smoothening = 7

        ####ScreenSize = 1536.0,864.0
        pTime = 0

        plocX,plocY = 0,0
        clocX, clocY = 0, 0

        cap = cv2.VideoCapture(0)
        cap.set(3, wCam)
        cap.set(4, hCam)


        detector = htm.handDetector(maxHands = 1,detectionCon = 0.85)
        wScr, hScr = autopy.screen.size()
        #print(wScr,hScr)
        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img,draw = True)

            if len(lmList) != 0:
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]

                #print(x1,y1,x2,y2)
                fingers = detector.fingersUp()

                cv2.rectangle(img,(frameR,frameR),(wCam-frameR, hCam-frameR),
                                (0,0,255), 2)
                    
                #print(fingers)
                if fingers[1]==1 and fingers[2]==0:
                    x3 = np.interp(x1, (frameR,wCam-frameR),(0,wScr))
                    y3 = np.interp(y1, (frameR,hCam-frameR),(0,hScr))
                    clocX = plocX + (x3-plocX) /smoothening
                    clocY = plocY + (y3-plocY) /smoothening
                    
                    autopy.mouse.move(wScr-clocX,clocY)
                    cv2.circle(img,(x1,y1),15,(0,255,0),cv2.FILLED)
                    plocX,plocY = clocX, clocY


                if fingers[1]==1 and fingers[2] == 1:
                    length, img, lineInfo, = detector.findDistance(8,12, img)

                    #print(length)
                    if length <30:
                        cv2.circle(img, (lineInfo[4],lineInfo[5]),
                                15, (0, 0,255), cv2.FILLED)
                        autopy.mouse.click()

                    
                    


                
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,
                        (255,0,0),3)
            cv2.imshow("Image",img)
            cv2.waitKey(1)
    def HandVolumeControl(SkipVal=10):
        wCam, hCam = 640,480


        cap = cv2.VideoCapture(0)

        cap.set(3, wCam)
        cap.set(4, hCam)
        pTime = 0
        detector = htm.handDetector(detectionCon=0.85,maxHands = 1)

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        #volume.GetMute()
        #volume.GetMasterVolumeLevel()
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        vol = 0
        volBar = 400
        volPer = 0
        area = 0
        colorVolume = (255,0,0)
        while True:
            success, img = cap.read()
            img = detector.findHands(img)
            lmList, bbox = detector.findPosition(img,draw = True)
            if len(lmList) != 0:
                
                #print(lmList[4][8])
                area = (bbox[2]-bbox[0] * bbox[3]-bbox[1])//100
                #print(area)
        ##        if -700<area<-1300:
        ##        print("yes")

                length, img, lineinfo = detector.findDistance(4, 8, img)
                #print(length)

                volBar = np.interp(length,[15,130],[400, 150])
                volPer = np.interp(length,[15,130],[0, 100])
                
                fingers = detector.fingersUp()
                #print(fingers)
                smoothness = SkipVal
                volPer = smoothness * round(volPer/smoothness)
                if not fingers[4]:
                    volume.SetMasterVolumeLevelScalar(volPer/100, None)
                    cv2.circle(img,(lineinfo[4],lineinfo[5]), 10, (0,255,0), cv2.FILLED)
                    colorVol = (0,255, 0)
                    time.sleep(0.25)
                else:
                    colorVol = (255,0,0)
                #print(length)

                
        ##        if length<40:
        ##            cv2.circle(img,(lineinfo[4],lineinfo[5]), 10, (0,255,0), cv2.FILLED)
            cv2.rectangle(img, (50,150), (85,400), (255, 0,0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (255, 0,0), cv2.FILLED)
            cv2.putText(img,f'{int(volPer)} %', (40,450), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0,0), 3)
            cVol = int(volume.GetMasterVolumeLevelScalar()*100)
            cv2.putText(img,f'Vol Set: {int(cVol)}', (400,50), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0,0), 3)
                    
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime
            
            cv2.putText(img,f'FPS: {int(fps)}', (40,50), cv2.FONT_HERSHEY_COMPLEX,
                        1, (255, 0,0), 3)
            cv2.imshow("WebCam",img)
            cv2.waitKey(1)





