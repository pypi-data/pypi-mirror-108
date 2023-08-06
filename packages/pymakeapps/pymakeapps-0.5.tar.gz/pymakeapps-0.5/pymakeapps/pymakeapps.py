import cv2
import numpy as np
import time
import autopy
import mediapipe as mp
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import cvzone
import face_recognition as fr
import os
from datetime import datetime
from tkinter import *
import tkinter.messagebox
from tkcalendar import*
import tkinter as tk
from tkinter.ttk import Progressbar
from time import sleep
import webbrowser
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import sqlite3
import parser
import tkcalendar

class Make():
    def Life_Calculator():
        root = Tk()
        space = " "
        root.title(185 * space + "                  Life Calculator                      ")
        #######700
        root.geometry("1285x630+56+0")

        #FRAMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMEEEEEEEEEEESSSSSSSSSSSSSSSSSSS
        MFrame = Frame(root, bd=10, width = 1245, height=680, relief=RIDGE, bg="cyan")
        MFrame.grid()

        TFrame = Frame(MFrame, bd=7, width = 1245, height=100, relief=RIDGE,)
        TFrame.grid(row=0,column=0)

        Top3Frame = Frame(MFrame, bd=5, width = 1245, height=500, relief=RIDGE,)
        Top3Frame.grid(row=1,column=0)

        LFrame = Frame(Top3Frame, bd=5, width = 1245, height=400,padx=2, relief=RIDGE, bg="cyan")
        LFrame.pack(side=LEFT)
        LFrame1 = Frame(LFrame, bd=5, width = 600, height=180,padx=2,pady=4 ,relief=RIDGE,)
        LFrame1.pack(side=TOP, padx=10,pady=12)

        RFrame = Frame(Top3Frame, bd=5, width = 320, height=400,padx=2, relief=RIDGE, bg="cyan")
        RFrame.pack(side=RIGHT,padx=2)
        RFrame1 = Frame(RFrame, bd=5, width = 310, height=300,padx=2,pady=2 ,relief=RIDGE,)
        RFrame1.pack(side=TOP, padx=5,pady=6)

        lblTitle = Label(TFrame, font=('arial',50,'bold'), text="Life Calculator", bd=7)
        lblTitle.grid(row=0,column=0,padx=88)
        #=================================================================================
        DOB= StringVar()
        CDate= StringVar()
        Days= StringVar()
        Ages= StringVar()
        Months= StringVar()
        Weeks= StringVar()
        Hours= StringVar()
        Minutes= StringVar()
        Seconds= StringVar()

        #=================================================================================
        def Reset():
            DOB.set("")
            CDate.set("")
            Days.set("")
            Ages.set("")
            Months.set("")
            Weeks.set("")
            Hours.set("")
            Minutes.set("")
            Seconds.set("")
            entFirstName.delete(0,END)
            entSurName.delete(0,END)

        def iExit():
            iExit = tkinter.messagebox.askyesno("Life Calculator", "Confirm if you want to exit")
            if iExit>0:
                root.destroy()
                return

        def Cal():
            CurrentDate = (DentCD.get_date())
            DOBDate = (DentDOB.get_date())
            Day = (abs ((CurrentDate - DOBDate).days))
            Days.set(str(Day))
            DOB.set("")
            Age = int(Days.get())
            Agess = (Age/365)
            Ages.set(str('%.0f'%Agess))
            Weeks.set(str('%.0f'%(Age/7)))
            Month = int(Weeks.get())
            Months.set(str('%.0f'%(Month/4)))
            Hours.set(str('%.0f'%(Age*24)))
            Minute = int(Hours.get())
            Minutes.set(str('%.0f'%Minute *60))
            Second = int(Minutes.get())
            Seconds.set(str('%.0f'%Second *60))
        ##    CDate.set("")
        ##    Days.set("")
        ##    Ages.set("")
        ##    Months.set("")
        ##    Weeks.set("")
        ##    Hours.set("")
        ##    Minutes.set("")
        ##    Seconds.set("")
        ##    entFirstName.delete(0,END)
        ##    entSurName.delete(0,END)
        #====================================================================================
        cal=Calendar(RFrame1,selectmode="day",year=2021,month=5,day=17, date_pattern='dd/mm/y',
                        font=('arial',16,'bold'))
        cal.grid(row=0,column=0,padx=10)
        #=========================================================================
        lblFirstName = Label(LFrame1, font=('arial',16,'bold'), text="FirstName", bd=7,anchor='w',justify = LEFT)
        lblFirstName.grid(row=0,column=0,sticky = W,padx=5)
        entFirstName = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT)
        entFirstName.grid(row=0,column=1)

        lblSurName = Label(LFrame1, font=('arial',16,'bold'), text="SurName", bd=7,anchor='w',justify = LEFT)
        lblSurName.grid(row=1,column=0,sticky = W,padx=5)
        entSurName = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT)
        entSurName.grid(row=1,column=1)

        lblDOB = Label(LFrame1, font=('arial',16,'bold'), text="Date of Birth", bd=7,anchor='w',justify = LEFT)
        lblDOB.grid(row=2,column=0,sticky = W,padx=5)
        DentDOB = DateEntry(LFrame1, font=('arial',16,'bold'), bd=5,width=46,borderwidth= 2,date_pattern='dd/mm/yyyy')
        DentDOB.grid(row=2,column=1)

        lblCD = Label(LFrame1, font=('arial',16,'bold'), text="Current Date", bd=7,anchor='w',justify = LEFT)
        lblCD.grid(row=3,column=0,sticky = W,padx=5)
        DentCD = DateEntry(LFrame1, font=('arial',16,'bold'), bd=5,width=46,borderwidth= 2,date_pattern='dd/mm/yyyy')
        DentCD.grid(row=3,column=1)

        lblDays = Label(LFrame1, font=('arial',16,'bold'), text="Days", bd=7,anchor='w',justify = LEFT)
        lblDays.grid(row=4,column=0,sticky = W,padx=5)
        entDays = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT,textvariable = Days)
        entDays.grid(row=4,column=1)

        lblAge = Label(LFrame1, font=('arial',16,'bold'), text="Age", bd=7,anchor='w',justify = LEFT)
        lblAge.grid(row=5,column=0,sticky = W,padx=5)
        entAge = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT,textvariable=Ages)
        entAge.grid(row=5,column=1)

        lblMonths = Label(LFrame1, font=('arial',16,'bold'), text="Months", bd=7,anchor='w',justify = LEFT)
        lblMonths.grid(row=6,column=0,sticky = W,padx=5)
        entMonths = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT,textvariable = Months)
        entMonths.grid(row=6,column=1)

        lblWeeks = Label(LFrame1, font=('arial',16,'bold'), text="Weeks", bd=7,anchor='w',justify = LEFT)
        lblWeeks.grid(row=7,column=0,sticky = W,padx=5)
        entWeeks = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT,textvariable = Weeks)
        entWeeks.grid(row=7,column=1)

        lblHours = Label(LFrame1, font=('arial',16,'bold'), text="Hours", bd=7,anchor='w',justify = LEFT)
        lblHours.grid(row=8,column=0,sticky = W,padx=5)
        entHours = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT,textvariable = Hours)
        entHours.grid(row=8,column=1)

        lblMinutes = Label(LFrame1, font=('arial',16,'bold'), text="Minutes", bd=7,anchor='w',justify = LEFT)
        lblMinutes.grid(row=9,column=0,sticky = W,padx=5)
        entMinutes= Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT,textvariable = Minutes)
        entMinutes.grid(row=9,column=1)

        lblSeconds = Label(LFrame1, font=('arial',16,'bold'), text="Seconds", bd=7,anchor='w',justify = LEFT)
        lblSeconds.grid(row=10,column=0,sticky = W,padx=5)
        entSeconds = Entry(LFrame1, font=('arial',16,'bold'), bd=5,width=48,justify = LEFT,textvariable = Seconds)
        entSeconds.grid(row=10,column=1)

        btnCalculate = Button(RFrame1, padx=18,bd=7,font=('Helvetica',18,'bold'), width = 23,text="Calculate",
                                bg='cyan',command = Cal)
        btnCalculate.grid(row=1,column=0,pady=2)

        btnReset = Button(RFrame1, padx=18,bd=7,font=('Helvetica',18,'bold'), width = 23,text="Reset",
                                bg='cyan',command = Reset)
        btnReset.grid(row=2,column=0,pady=2)

        btnExit = Button(RFrame1, padx=18,bd=7,font=('Helvetica',18,'bold'), width = 23,text="Exit",
                                bg='cyan',command = iExit)
        btnExit.grid(row=3,column=0,pady=2)




        root.mainloop()


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
    def bbox():
        cap = cv2.VideoCapture(0)
        detector = cvzone.HandDetector()

        while True:
            # Get image frame
            success, img = cap.read()

            # Find the hand and its landmarks
            img = detector.findHands(img, draw=False)
            lmList, bbox = detector.findPosition(img, draw=False)
            if bbox:
                # Draw  Corner Rectangle
                cvzone.cornerRect(img, bbox)

            # Display
            cv2.imshow("Image", img)
            cv2.waitKey(1)
    def dummysample():
        cap = cv2.VideoCapture(0)
        mpHands = mp.solutions.hands
        hands = mpHands.Hands()
        mpDraw = mp.solutions.drawing_utils

        pTime = 0
        cTime = 0
        while True:
            success, img = cap.read()
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(imgRGB)
            #print(results.multi_hand_landmarks)
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    for id , lm in enumerate(handLms.landmark):
                    # print(id, lm)
                        h, w, c = img.shape
                        cx, cy = int(lm.x*w), int(lm.y*h)
                        #print(id,cx, cy)
                        #if id ==4:
                        cv2.circle(img, (cx, cy), 15, (255,0,255),cv2.FILLED)
                        
                    mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            cTime = time.time()
            fps = 1/(cTime-pTime)
            pTime = cTime

            cv2.putText(img, str(int(fps)),(10,70), cv2.FONT_HERSHEY_PLAIN,3,
            (255,0,255), 3)
                    
            cv2.imshow("WebCam", img)
            cv2.waitKey(1)
    def Virtual_Painter_b_g_r(folder):
        brushThickness = 20
        eraserThickness = 100
        ##importtatione
        folderPath = folder
        myList = os.listdir(folderPath)
        #print(myList)
        overlayList = []
        for imPath in myList:
            image = cv2.imread(f'{folderPath}/{imPath}')
            overlayList.append(image)
        #print(len(overlayList))
        header = overlayList[0]
        drawColor = (255, 0, 255)
        ##webcam##
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        imgCanvas = np.zeros((720, 1280, 3), np.uint8)
        detector = htm.handDetector(detectionCon=0.7)
        xp,yp = 0,0
        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = detector.findHands(img)
            lmList = detector.findPosition(img,draw=False)

            if len(lmList) != 0:
                #print(lmList)

                
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]

                fingers = detector.fingersUp()

                print(fingers)
                if fingers[1] and fingers[2]:
                    cv2.rectangle(img, (x1, y1-25),(x2,y2+25),drawColor,cv2.FILLED)
                    #print("Selection Mode")
                    if y1 < 120:
                        if 250<x1<450:
                            header = overlayList[0]
                            drawColor = (255,0,255)
                        elif 550<x1<750:
                            header = overlayList[1]
                            drawColor = (255,0,0)
                        elif 800<x1<950:
                            header = overlayList[2]
                            drawColor = (0,255,0)
                        elif 1050<x1<1200:
                            header = overlayList[3]
                            drawColor = (0,0,0)

                if fingers[1] and fingers[2]==False:
                    cv2.circle(img, (x1, y1),15,drawColor,cv2.FILLED)
                    #print("Drawing Mode")
                    if xp==0 and yp==0:
                        xp,yp = x1,y1
                    if drawColor == (0,0,0):
                        cv2.line(img, (xp,yp), (x1,y1),drawColor,eraserThickness)
                        cv2.line(imgCanvas, (xp,yp), (x1,y1),drawColor, eraserThickness)

                    else:
                        cv2.line(img, (xp,yp), (x1,y1),drawColor, brushThickness)
                        cv2.line(imgCanvas, (xp,yp), (x1,y1),drawColor, brushThickness)
                    xp, yp = x1,y1

            imgGray = cv2.cvtColor(imgCanvas,cv2.COLOR_BGR2GRAY)
            _, imgInv = cv2.threshold(imgGray,50,255, cv2.THRESH_BINARY_INV)
            imgInv = cv2.cvtColor(imgInv,cv2.COLOR_GRAY2BGR)
            img = cv2.bitwise_and(img,imgInv)
            img = cv2.bitwise_and(img,imgInv)
            img = cv2.bitwise_or(img, imgCanvas)

            #img = cv2.addWeighted(img,0.5,imgCanvas,0.5,0)
                            

            #Setting the header image
            img[0:125, 0:1280] = header
            cv2.waitKey(1)
            cv2.imshow("WebCam",img)
            cv2.imshow("Canvas", imgCanvas)
class Posture():
    def Posture():
        cap = cv2.VideoCapture(0)
        detector = cvzone.PoseDetector()
        while True:
            success, img = cap.read()
            img = detector.findPose(img)
            lmList = detector.findPosition(img, draw=False)
            if lmList:
                print(lmList[14])
                cv2.circle(img, (lmList[14][1], lmList[14][2]), 15, (0, 0, 255), cv2.FILLED)

            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
    def Trainer(Hand="Left",minangle=210,maxangle=310,halfval=False,count=0):
        Hand = "Left"

        bar = True

        minangle = 210

        maxangle = 310
        cap = cv2.VideoCapture(0)

        detector = cvzone.PoseDetector()

        count = 1

        dir = 0

        halfval = False

        pTime = 0

        val = 10

        while True:
            success, img = cap.read()
            img = cv2.resize(img,(1280,720))
            #img = cv2.imread("AiTrainer/test.jpg")
            img = detector.findPose(img,False)
            lmList = detector.findPosition(img,False)
            #print(lmList[32])
            if len(lmList) != 0:
                #Right Arm
                if Hand == "Left":
                    angle = detector.findAngle(img,11,13,15)
                    per = np.interp(angle,(minangle,maxangle),(0,100))
                    bar = np.interp(angle,(minangle,maxangle),(650, 100))
                    #print(angle,per)
                elif Hand == "Right":
                    angle = detector.findAngle(img,12,14,16)
                    per = np.interp(angle,(minangle,maxangle),(0,100))
                    bar = np.interp(angle,(minangle,maxangle),(650, 100))
                    #print(angle,per)
                color = (255,0,255)
                if per == 100:
                    color = (0,255,0)
                    if dir == 0:
                        count +=0.5
                        dir = 1
                if per == 0:
                    color = (0,255,0)
                    if dir==1:
                        count+=0.5
                        dir = 0
                #print(count)

                cv2.rectangle(img,(1100,100),(1175,650),color,3)
                cv2.rectangle(img,(1100,int(bar)),(1175,650),color, cv2.FILLED)
                cv2.putText(img,f'{int(per)} %', (1100,75), cv2.FONT_HERSHEY_PLAIN,4,
                                color,4)
                
                if count >= 1 and count < 10:
                    cv2.rectangle(img,(0,450),(250,720),(0,255,0), cv2.FILLED)
                if count >= 10 and count < 100:
                    cv2.rectangle(img,(0,450),(400,720),(0,255,0), cv2.FILLED)
                if  count >= 100 and count < 1000:
                    cv2.rectangle(img,(0,450),(600,720),(0,255,0), cv2.FILLED)
                if  count >= 1000 and count < 10000:
                    cv2.rectangle(img,(0,450),(700,720),(0,255,0), cv2.FILLED)
                    
                if halfval == False:
                    cv2.putText(img, str(int(count)), (45,670), cv2.FONT_HERSHEY_PLAIN,15,
                                (255,0,0),25)
                if halfval == True:
                    cv2.putText(img, str(count), (45,670), cv2.FONT_HERSHEY_PLAIN,15,
                                (255,0,0),25)
                cTime = time.time()
                fps = 1/(cTime-pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (50,100), cv2.FONT_HERSHEY_PLAIN,5,
                                (255,0,0),5)
                
            cv2.imshow("Image",img)
            cv2.waitKey(1)


class VideoExamples():
    def Stack():
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)

        while True:
            success, img = cap.read()
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            imgList = [img, img, imgGray, img, imgGray, img,imgGray, img, img]
            stackedImg = cvzone.stackImages(imgList, 3, 0.4)

            cv2.imshow("stackedImg", stackedImg)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
class Face():
    def Face_Recognition(pathname,csvname):
        path = pathname
        images = []
        classNames = []
        myList = os.listdir(path)
        print(myList)
        for cl in myList:
            curImg = cv2.imread(f'{path}/{cl}')
            images.append(curImg)
            classNames.append(os.path.splitext(cl)[0])
        print(classNames)

        def findEncodings(images):
            encodeList = []
            for img in images:
                img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                encode = fr.face_encodings(img)[0]
                encodeList.append(encode)
            return encodeList

        def markAttendance(name):
            with open(csvname,'r+')as f:
                myDataList = f.readlines()
                nameList = []
                for line in myDataList:
                    entry = line.split(',')
                    nameList.append(entry[0])
        ##        if name not in nameList: #####U can use this and indent the next 3 lines once if you want a name to be there only once
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')
                    
            

        encodeListKnown = findEncodings(images)
        print('Encoding Complete')

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            imgS = cv2.resize(img,(0,0),None,0.25,0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
            
            facesCurFrame = fr.face_locations(imgS)           
            encodesCurFrame = fr.face_encodings(imgS,facesCurFrame)

            for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
                matches = fr.compare_faces(encodeListKnown,encodeFace)
                faceDis = fr.face_distance(encodeListKnown,encodeFace)
                #print(faceDis)
                matchIndex = np.argmin(faceDis)

                if matches[matchIndex]:
                    name = classNames[matchIndex].upper()
                    #print(name)
                    y1,x2,y2,x1 = faceLoc
                    y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                    cv2.rectangle(img,(x1,y1),(x2,y2),(0,0,255),2)
                    cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                    cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                    markAttendance(name)

                cv2.imshow('Webcam',img)
                cv2.waitKey(1)

                
                
            

        ##faceLoc = fr.face_locations(imgElon)[0]
        ##encodeElon = fr.face_encodings(imgElon)[0]
        ###print(faceLoc)
        ##cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
        ##
        ##faceLocTest = fr.face_locations(imgTest)[0]
        ##encodeTest = fr.face_encodings(imgTest)[0]
        ###print(faceLoc)
        ##cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
        ##
        ##results = fr.compare_faces([encodeElon],encodeTest)
        ##faceDis = fr.face_distance([encodeElon],encodeTest)
                

        ##imgElon = fr.load_image_file("ImagesBasic/elon musk.jpg")
        ##imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
        ##imgTest = fr.load_image_file("ImagesBasic/bill gates.jpg")
        ##imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
    def face_percent_detection():
        cap = cv2.VideoCapture(0)
        detector = cvzone.FaceDetector()

        while True:
            success, img = cap.read()
            img, bboxs = detector.findFaces(img)
            #print(bboxs)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
    def face_mesh_detection():
        cap = cv2.VideoCapture(0)
        detector = cvzone.FaceMeshDetector(maxFaces=2)
        while True:
            success, img = cap.read()
            img, faces = detector.findFaceMesh(img)
            if faces:
                print(faces[0])
            cv2.imshow("Image", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()