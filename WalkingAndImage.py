#!/usr/bin/env python
#-*- cording: utf-8 -*-
import time
import cv2
import sys

g_width = 320;
g_height = 240;

#カメラのサイズを適宜変更して処理速度を調整
g_width2 = 100;
g_height2 = 100;

out_img = cv2.imread("white.jpg");
out_img = cv2.resize(out_img, (g_width2, g_height2))


timeStart = 0
timeEnd = 0
spanTime = 0

args = sys.argv

print(len(sys.argv))

if len(args) < 5:
 exit()

#diffFolder = args[1];
#動きに合わせて表示する画像リストのファイルパス
ImageFilePath = args[1];
file1 = open(ImageFilePath, 'r')
#差分判定率
DiffJudgePercent = float(args[2])
TimeSpan = float(args[3])
walkCountThrethold = int(args[4])
walkCount = walkCountThrethold;

# VideoCapture オブジェクトを取得します
g_capture = cv2.VideoCapture(0)

print(g_capture.set(cv2.CAP_PROP_FRAME_WIDTH, g_width2))
print(g_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, g_height2)) 

out_img = cv2.imread("white.jpg")

global firstPoseFlg
firstPoseFlg = True;

MoviePlayFlg = True

def Play():

    global g_capture
    global g_width
    global g_height

    global diffFolder
    global diffEdgeFolder
    global poseFlowFilePath
    global MusicFilePath
    global out_img
    global MoviePlayFlg
    global DiffJudgePercent
    
    global walkCount
    
    timeStart = 0.0
    timeEnd = 0.0
    spanTime = 0.0

    Lines1 = file1.readlines()
    
    idx1 = 0
    while(1):
        ret, frame = g_capture.read()
        img1 = frame;        
        
        str1 = cv2.waitKey(1)
        if str1 == ord("q"):
            break
        
        cv2.imshow('frame', frame)
        
        if idx1 < len(Lines1):
            line1 = Lines1[idx1]
        elif idx1 == len(Lines1):
            line1 = line1
        else:
            break
            
        line1 = line1.replace( '\n' , '' )
        if line1 == '':
            break
        

            
        currentTime = time.time()
        if timeStart == 0:
            img2 = img1
            timeStart = time.time()
            timeEnd = time.time()

            #print(line1)
            frame = cv2.imread(line1)    
            cv2.imshow('frame3', frame)
            
        else:
            timeEnd = time.time()
            
        timeDiff = timeEnd - timeStart
        
        if(timeDiff >= TimeSpan):
            img3 = Diff(img1, img2)
            WRate = calcWhiteRate(img3)
            timeStart = currentTime
            
            print(WRate)
            if WRate >= DiffJudgePercent:
                walkCount = walkCount + 1
                str1 = "walkCount:"
                str1 += str(walkCount)
                print(str1)
                
            
            if WRate >= DiffJudgePercent and walkCount >= walkCountThrethold:
                walkCount = 0
                idx1 = idx1 + 1
                
                print(line1)
                frame = cv2.imread(line1)    
                cv2.imshow('frame3', frame)
                

            
            img2 = img1
       

    g_capture.release()

    cv2.destroyAllWindows()

def calcWhiteRate(img1):

    global g_width2
    global g_height2
    
    WCount = 0
    
    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
             
             if ( img1[y, x, 0] == 255 and
                  img1[y, x, 1] == 255 and
                  img1[y, x, 2] == 255 ) :
                    WCount = WCount+1
    
    WRate = WCount / (g_width2 * g_height2)
    WRate = WRate * 100.0
    
    return WRate
    

def Diff(img1, img2):
    
    global g_width
    global g_height
    global out_img

    for x in range(0, g_width2) :
         for y in range(0, g_height2) :
            if img1[y, x, 0] >= img2[y, x, 0]:
                out_img[y, x, 0] = abs(img1[y, x, 0] - img2[y, x, 0]);
            else:
                out_img[y, x, 0] = abs(img2[y, x, 0] - img1[y, x, 0]);

            if img1[y, x, 1] >= img2[y, x, 1]:
                out_img[y, x, 1] = abs(img1[y, x, 1] - img2[y, x, 1]);
            else:
                out_img[y, x, 1] = abs(img2[y, x, 1] - img1[y, x, 1]);

            if img1[y, x, 2] >= img2[y, x, 2]:
                out_img[y, x, 2] = abs(img1[y, x, 2] - img2[y, x, 2]);
            else:
                out_img[y, x, 2] = abs(img2[y, x, 2] - img1[y, x, 2]);

            absSum = int(out_img[y, x, 0]) + int(out_img[y, x, 1]) + int(out_img[y, x, 2])
            if absSum >= 120:
                    out_img[y, x, 0] = 255
                    out_img[y, x, 1] = 255
                    out_img[y, x, 2] = 255
            else:
                    out_img[y, x, 0] = 0
                    out_img[y, x, 1] = 0
                    out_img[y, x, 2] = 0
                    
    return out_img


def main(): 

    Play()


    return 0
   

    
        
main()
