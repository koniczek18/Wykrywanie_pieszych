import numpy as np
import cv2
import time


def nothing(value):
    #empty function for callbacks
    pass


# class and parameters for pedestrian detection
maxGap = 5
marginX = 120  # pixels ignored from either side
marginY = 120  # pixels ignored from the top


class Shape:
    def __init__(self):
        self.pixels = []
        self.bounds = []

    def getPixels(self):
        return self.pixels

    def append(self, pxl):
        if len(self.bounds) == 0:
            self.bounds.append(pxl[0])
            self.bounds.append(pxl[1])
        elif len(self.bounds) == 2:
            old_pxl = (self.bounds[0], self.bounds[1])
            self.bounds = [min(old_pxl[0], pxl[0]), min(old_pxl[1], pxl[1]),
                           max(old_pxl[0], pxl[0]), max(old_pxl[1], pxl[1])]
        else:
            self.bounds = [min(self.bounds[0], pxl[0]), min(self.bounds[1], pxl[1]),
                           max(self.bounds[2], pxl[0]), max(self.bounds[3], pxl[1])]
        self.pixels.append(pxl)

    def pixelCount(self):
        return len(self.pixels)

    def getCenter(self):
        if len(self.bounds) < 4:
            return self.bounds[0], self.bounds[1]
        else:
            return (self.bounds[0] + self.bounds[2]) / 2, (self.bounds[1] + self.bounds[3]) / 2


#file paths to video materials
videoPathThermal = ["src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_1.avi",
                    "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_3.avi",
                    "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_4.avi",
                    "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_5.avi",
                    "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_6.avi",
                    "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_7.avi",
                    "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_8.avi",
                    "src/video_in_motion/thermal/Jazda_LudzieNaTorach_Termo_10.avi",
                    "src/video_in_motion/thermal/Jazda_ToryPuste_Termo_1.avi",
                    "src/video_in_motion/thermal/Jazda_ToryPuste_Termo_2.avi",
                    "src/video_in_motion/thermal/Jazda_ToryPuste_Termo_3.avi",
                    "src/video_in_motion/thermal/Jazda_ToryWJezdni_Puste_Termo_1.avi",
                    "src/video_in_motion/thermal/Jazda_ToryWJezdni_Samochod_Termo_1.avi",
                    "src/video_in_motion/thermal/TorowiskoPuste_2_Termo.avi",
                    "src/video_in_motion/thermal/TorowiskoPuste_3_Termo.avi",
                    "src/video_stationary/thermal/Postoj_LudzieNaTorach_termo_1.avi",
                    "src/video_stationary/thermal/Postoj_LudzieNaTorach_termo_3.avi",
                    "src/video_stationary/thermal/Postoj_LudzieNaTorach_termo_7.avi",
                    "src/video_stationary/thermal/Postoj_LudzieNaTorach_termo_10.avi",
                    "src/video_stationary/thermal/Postoj_LudzieNaTorach_termo_12.avi"]
videoPathNormal = ["src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_1.avi",
                    "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_3.avi",
                    "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_4.avi",
                    "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_5.avi",
                    "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_6.avi",
                    "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_7.avi",
                    "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_8.avi",
                    "src/video_in_motion/normal/Jazda_LudzieNaTorach_Zwykla_10.avi",
                    "src/video_in_motion/normal/Jazda_ToryPuste_Zwykla_1.avi",
                    "src/video_in_motion/normal/Jazda_ToryPuste_Zwykla_2.avi",
                    "src/video_in_motion/normal/Jazda_ToryPuste_Zwykla_3.avi",
                    "src/video_in_motion/normal/Jazda_ToryWJezdni_Puste_Zwykla_1.avi",
                    "src/video_in_motion/normal/Jazda_ToryWJezdni_Samochod_Zwykla_1.avi",
                    "src/video_in_motion/normal/TorowiskoPuste_2_Zwykla.avi",
                    "src/video_in_motion/normal/TorowiskoPuste_3_Zwykla.avi",
                    "src/video_stationary/normal/Postoj_LudzieNaTorach_Zwykla_1.avi",
                    "src/video_stationary/normal/Postoj_LudzieNaTorach_Zwykla_3.avi",
                    "src/video_stationary/normal/Postoj_LudzieNaTorach_Zwykla_7.avi",
                    "src/video_stationary/normal/Postoj_LudzieNaTorach_Zwykla_10.avi",
                    "src/video_stationary/normal/Postoj_LudzieNaTorach_Zwykla_12.avi"]
videoPathMerged = ["src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_1.avi",
                    "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_3.avi",
                    "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_4.avi",
                    "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_5.avi",
                    "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_6.avi",
                    "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_7.avi",
                    "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_8.avi",
                    "src/video_in_motion/merged/Jazda_LudzieNaTorach_Merged_10.avi",
                    "src/video_in_motion/merged/Jazda_ToryPuste_Merged_1.avi",
                    "src/video_in_motion/merged/Jazda_ToryPuste_Merged_2.avi",
                    "src/video_in_motion/merged/Jazda_ToryPuste_Merged_3.avi",
                    "src/video_in_motion/merged/Jazda_ToryWJezdni_Puste_Merged_1.avi",
                    "src/video_in_motion/merged/Jazda_ToryWJezdni_Samochod_Merged_1.avi",
                    "src/video_in_motion/merged/TorowiskoPuste_2_Merged.avi",
                    "src/video_in_motion/merged/TorowiskoPuste_3_Merged.avi",
                    "src/video_stationary/merged/Postoj_LudzieNaTorach_Merged_1.avi",
                    "src/video_stationary/merged/Postoj_LudzieNaTorach_Merged_3.avi",
                    "src/video_stationary/merged/Postoj_LudzieNaTorach_Merged_7.avi",
                    "src/video_stationary/merged/Postoj_LudzieNaTorach_Merged_10.avi",
                    "src/video_stationary/merged/Postoj_LudzieNaTorach_Merged_12.avi"]
vid_num = 0   # from 0 to 19, problems with 4 and 15

#initialise video capture based on file paths
videoT = cv2.VideoCapture(videoPathThermal[vid_num])
videoN = cv2.VideoCapture(videoPathNormal[vid_num])
videoM = cv2.VideoCapture(videoPathMerged[vid_num])

#create windows
cv2.namedWindow('Thermal')
cv2.namedWindow('Normal')
cv2.namedWindow('Merged')
cv2.namedWindow('Mask Thermal')
cv2.namedWindow("Edges")
cv2.namedWindow("Trackbars")

#aditonal variables for resizing and fps limitation
dim = (640, 360)
fpsT = videoT.get(cv2.CAP_PROP_FPS)

#move windows for convenience
cv2.moveWindow('Thermal',0,0)
cv2.moveWindow('Normal',dim[0],0)
cv2.moveWindow('Merged',2*dim[0],0)
cv2.moveWindow('Mask Thermal',0,30+dim[1])
cv2.moveWindow('Edges',dim[0],30+dim[1])
cv2.moveWindow('Trackbars',2*dim[0],30+dim[1])

#initialise trackbars !!! THE FIRST VALUE IN TRACKBAR IS INITIAL, SECOND IS MAX!!!
cv2.createTrackbar("LH", "Trackbars", 0, 179, nothing)  # 7
cv2.createTrackbar("LS", "Trackbars", 0, 255, nothing)  # 0
cv2.createTrackbar("LV", "Trackbars", 125, 255, nothing)  # 50
cv2.createTrackbar("UH", "Trackbars", 179, 179, nothing)  # 173
cv2.createTrackbar("US", "Trackbars", 71, 255, nothing)  # 7
cv2.createTrackbar("UV", "Trackbars", 255, 255, nothing)  # 115
cv2.createTrackbar("PS", "Trackbars", 5, 25, nothing)  # 115
cv2.createTrackbar("PG", "Trackbars", 15, 25, nothing)  # 115

while True:
    #fps limiation
    start = time.time()

    #begin video read
    retT, frameT = videoT.read()
    retN, frameN = videoN.read()
    retM, frameM = videoM.read()

    #if video playback has ended, start it again
    if (not retT) and (not retN):
        videoT = cv2.VideoCapture(videoPathThermal[vid_num])
        retT, frameT = videoT.read()
        videoN = cv2.VideoCapture(videoPathNormal[vid_num])
        retN, frameN = videoN.read()
        videoM = cv2.VideoCapture(videoPathMerged[vid_num])
        retM, frameM = videoM.read()
        continue

    #get trackbar positions to create mask
    LH = cv2.getTrackbarPos("LH", "Trackbars")
    LS = cv2.getTrackbarPos("LS", "Trackbars")
    LV = cv2.getTrackbarPos("LV", "Trackbars")
    UH = cv2.getTrackbarPos("UH", "Trackbars")
    US = cv2.getTrackbarPos("US", "Trackbars")
    UV = cv2.getTrackbarPos("UV", "Trackbars")
    PS = cv2.getTrackbarPos("PS", "Trackbars")
    PG = cv2.getTrackbarPos("PG", "Trackbars")

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
            if abs(x1 - x2)/dim[0] < abs(y1 - y2)/dim[1]:
                cv2.line(frameT, (x1, y1), (x2, y2), (0, 255, 0), 3)

    # find pedestrians, hopefully
    shapes = []
    for x in range(dim[0] - 2 * marginX):
        for y in range(dim[1] - marginY):
            # for every pixel we check its value
            if edges[y + marginY][x + marginX] > 0:
                foundShape = False
                # we check for existing shapes
                for s in shapes:
                    pixel = None
                    for p in s.getPixels():
                        # we check all pixels in a shape, to see if any are close enough
                        if (x + marginX - maxGap < p[0] < x + marginX + maxGap)\
                                and (y + marginY - maxGap < p[1] < y + marginY + maxGap):
                            pixel = (x + marginX, y + marginY)
                            break
                    # if shape contains a pixel close by, current pixel is added to it
                    if pixel is not None:
                        foundShape = True
                        s.append(pixel)
                        break

                # if pixel stands alone, create a new Shape
                if not foundShape:
                    shape = Shape()
                    shape.append((x + marginX, y + marginY))
                    shapes.append(shape)

    # change color of found shapes, for some reason
    for s in shapes:
        if s.pixelCount() > PS + PG * int(s.getCenter()[1]/60):
            for p in s.getPixels():
                edges[p[1]][p[0]] = 80

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