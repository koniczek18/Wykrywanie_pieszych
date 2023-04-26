import numpy as np
import cv2
import time

def nothing(value):
    #empty function for callbacks
    pass

#file paths to video materials
videoPathThermal = "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_1.avi"
videoPathNormal = "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_1.avi"
videoPathMerged = "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_1.avi"

#initialise video capture based on file paths
videoT = cv2.VideoCapture(videoPathThermal)
videoN = cv2.VideoCapture(videoPathNormal)
videoM = cv2.VideoCapture(videoPathMerged)

#create windows
cv2.namedWindow('Thermal')
cv2.namedWindow('Normal')
cv2.namedWindow('Merged')
cv2.namedWindow('Mask Thermal')
cv2.namedWindow("Edges")
cv2.namedWindow("Trackbars")

#move windows for convenience
cv2.moveWindow('Thermal',0,0)
cv2.moveWindow('Normal',640,0)
cv2.moveWindow('Merged',1280,0)
cv2.moveWindow('Edges',640,390)
cv2.moveWindow('Mask Thermal',0,390)
cv2.moveWindow('Trackbars',1280,390)

#initialise trackbars !!! THE FIRST VALUE IN TRACKBAR IS INITIAL, SECOND IS MAX!!!
cv2.createTrackbar("LH", "Trackbars", 7, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 50, 255, nothing)
cv2.createTrackbar("UH", "Trackbars", 173, 179, nothing)
cv2.createTrackbar("US", "Trackbars", 7, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 115, 255, nothing)

#aditonal variables for resizing and fps limitation
dim = (640, 360)
fpsT = videoT.get(cv2.CAP_PROP_FPS)

while True:
    #fps limiation
    start = time.time()

    #begin video read
    retT, frameT = videoT.read()
    retN, frameN = videoN.read()
    retM, frameM = videoM.read()

    #if video playback has ended, start it again
    if (not retT) and (not retN):
        videoT = cv2.VideoCapture(videoPathThermal)
        retT, frameT = videoT.read()
        videoN = cv2.VideoCapture(videoPathNormal)
        retN, frameN = videoN.read()
        videoM = cv2.VideoCapture(videoPathMerged)
        retM, frameM = videoM.read()
        continue

    #get trackbar positions to create mask
    LH = cv2.getTrackbarPos("LH", "Trackbars")
    LS = cv2.getTrackbarPos("LS", "Trackbars")
    LV = cv2.getTrackbarPos("LV", "Trackbars")
    UH = cv2.getTrackbarPos("UH", "Trackbars")
    US = cv2.getTrackbarPos("US", "Trackbars")
    UV = cv2.getTrackbarPos("UV", "Trackbars")

    #resize windows
    frameT = cv2.resize(frameT, dim, interpolation=cv2.INTER_AREA)
    frameN = cv2.resize(frameN, dim, interpolation=cv2.INTER_AREA)
    frameM = cv2.resize(frameM, dim, interpolation=cv2.INTER_AREA)

    #find lines algorithm
    hsv = cv2.cvtColor(frameT, cv2.COLOR_BGR2HSV)
    low = np.array([LH, LS, LV])
    high = np.array([UH, US, UV])
    mask = cv2.inRange(hsv, low, high)
    edges = cv2.Canny(mask,75,150)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,50,maxLineGap=100,minLineLength=70)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frameT, (x1, y1), (x2, y2), (0, 255, 0), 3)
    #show results
    cv2.imshow("Thermal", frameT)
    cv2.imshow("Normal", frameN)
    cv2.imshow("Merged", frameM)
    cv2.imshow("Edges", edges)
    cv2.imshow("Mask Thermal", mask)

    #if 'esc' key has been pressed, close all
    key = cv2.waitKey(1)
    if key == 27:
        break

    #fps limitation
    end =time.time()
    elapsed=end-start
    if 1/25>elapsed:
        time.sleep(1/25 - elapsed)

#close all
videoT.release()
cv2.destroyAllWindows()