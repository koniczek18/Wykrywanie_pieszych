
import numpy as np
import cv2

def nothing(x):
    pass

video = cv2.VideoCapture("xD.mp4")
cv2.namedWindow("ddd")
cv2.createTrackbar("LH", "ddd", 179, 179, nothing)
cv2.createTrackbar("LS", "ddd", 255, 255, nothing)
cv2.createTrackbar("LV", "ddd", 255, 255, nothing)
cv2.createTrackbar("UH", "ddd", 179, 179, nothing)
cv2.createTrackbar("US", "ddd", 255, 255, nothing)
cv2.createTrackbar("UV", "ddd", 255, 255, nothing)

while True:
    ret, frame = video.read()

    if not ret:
        video = cv2.VideoCapture("xD.mp4")
        continue

    LH = cv2.getTrackbarPos("LH", "ddd")
    LS = cv2.getTrackbarPos("LS", "ddd")
    LV = cv2.getTrackbarPos("LV", "ddd")
    UH = cv2.getTrackbarPos("UH", "ddd")
    US = cv2.getTrackbarPos("US", "ddd")
    UV = cv2.getTrackbarPos("UV", "ddd")
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    low = np.array([LH, LS, LV])
    high = np.array([UH, US, UV])
    mask = cv2.inRange(hsv, low, high)
    edges = cv2.Canny(mask,75,150)
    cv2.imshow("edges", edges)
    lines = cv2.HoughLinesP(edges,1,np.pi/180,50,maxLineGap=100,minLineLength=70)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
    cv2.imshow("frame", frame)
    cv2.imshow("mask", mask)
    key = cv2.waitKey(1)
    if key == 27:
        break

video.release()
cv2.destroyAllWindows()