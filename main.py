
import numpy as np
import cv2

def nothing(value):
    pass

videoPathThermal = "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_1.avi"
videoPathNormal = "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_1.avi"
videoPathMerged = "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_1.avi"

videoT = cv2.VideoCapture(videoPathThermal)
videoN = cv2.VideoCapture(videoPathNormal)
videoM = cv2.VideoCapture(videoPathMerged)

cv2.namedWindow("Trackbars")
cv2.createTrackbar("LH", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("LS", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("LV", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("US", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)

dim = (640, 360)

fpsT = videoT.get(cv2.CAP_PROP_FPS)
fpsN = videoT.get(cv2.CAP_PROP_FPS)
fpsM = videoT.get(cv2.CAP_PROP_FPS)
print(fpsT)
print(fpsN)
print(fpsM)

while True:
    retT, frameT = videoT.read()
    retN, frameN = videoN.read()
    retM, frameM = videoM.read()

    if (not retT) and (not retN):
        videoT = cv2.VideoCapture(videoPathThermal)
        retT, frameT = videoT.read()
        videoN = cv2.VideoCapture(videoPathNormal)
        retN, frameN = videoN.read()
        videoM = cv2.VideoCapture(videoPathMerged)
        retM, frameM = videoM.read()
        continue

    LH = cv2.getTrackbarPos("LH", "Trackbars")
    LS = cv2.getTrackbarPos("LS", "Trackbars")
    LV = cv2.getTrackbarPos("LV", "Trackbars")
    UH = cv2.getTrackbarPos("UH", "Trackbars")
    US = cv2.getTrackbarPos("US", "Trackbars")
    UV = cv2.getTrackbarPos("UV", "Trackbars")

    frameT = cv2.resize(frameT, dim, interpolation=cv2.INTER_AREA)
    frameN = cv2.resize(frameN, dim, interpolation=cv2.INTER_AREA)
    frameM = cv2.resize(frameM, dim, interpolation=cv2.INTER_AREA)

    hsv = cv2.cvtColor(frameT, cv2.COLOR_BGR2HSV)
    low = np.array([LH, LS, LV])
    high = np.array([UH, US, UV])
    mask = cv2.inRange(hsv, low, high)
    edges = cv2.Canny(mask,75,150)
    cv2.imshow("edges", edges)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,50,maxLineGap=100,minLineLength=70)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frameT, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.imshow("Thermal", frameT)
    cv2.imshow("Normal", frameN)
    cv2.imshow("Merged", frameM)
    cv2.imshow("Mask Thermal", mask)
    key = cv2.waitKey(1)
    if key == 27:
        break

videoT.release()
cv2.destroyAllWindows()