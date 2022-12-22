import cv2 as cv
import numpy as np
from scipy import stats

for index in range(1, 21):
    # 檔名
    name = ''
    if index < 10:
        name = "00" + str(index)
    else:
        name = "0" + str(index)
    nameall = "IMG" + name + ".jpg"
    img = cv.imread(nameall)
    zero_channel = np.zeros(img.shape[0:2], dtype="uint8")

    # BGR通道
    B, G, R = cv.split(img)
    imgR = cv.merge([R, R, R])
    imgG = cv.merge([G, G, G])

    # Threshold
    mat, imgThreshold = cv.threshold(imgR, 70, 255, cv.THRESH_BINARY_INV)
    heightThreshold, widthThreshold = imgThreshold.shape[:2]

    # 找ROI
    imgROI = imgThreshold[0:heightThreshold, 300:400]

    height, width = imgROI.shape[:2]

    # 找最長的
    length = []
    greatest = 0
    greatest_index = 0
    for i in range(0, height):
        con = True
        count = 0
        for j in range(0, width):
            if imgROI[i][j][0] == 255:
                count += 1
            elif count != 0:
                break
        # print(count)
        length.append(count)
        if count > greatest:
            greatest = count
            greatest_index = i

    # 長度設為眾數
    mode = stats.mode(length)
    greatest = mode[0]
    text = "L1: " + str(greatest)

    # 最長的上色
    for j in range(0, width):
        if imgROI[greatest_index][j][0] == 255:
            imgROI[greatest_index][j] = [0, 0, 255]

    # 疊回去
    imgThreshold[0:heightThreshold, 300:400] = imgROI

    mat, imgThresholdG = cv.threshold(imgG, 120, 255, cv.THRESH_BINARY_INV)
    imgROIG = imgThresholdG[0:heightThreshold, 0:300]
    imgThreshold[0:heightThreshold, 0:300] = imgROIG

    imgGray = cv.cvtColor(imgROIG, cv.COLOR_BGR2GRAY)
    pixels = cv.countNonZero(imgGray)

    text2 = "N: " + str(pixels)
    text3 = ""
    if greatest < 30 or pixels > 100:
        text3 = "NG"
    else:
        text3 = "OK"

    #cv.putText(img, text, org, fontFace, fontScale, fontcolor, thickness, lineType)
    cv.putText(imgThreshold, text, (400, 40),
               cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, 4)
    cv.putText(imgThreshold, text2, (400, 80),
               cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, 4)
    cv.putText(imgThreshold, text3, (400, 120),
               cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 1, 4)
    cv.imshow(nameall, imgThreshold)
    cv.imwrite("IMG"+name+"Result.jpg", imgThreshold)
    cv.waitKey(0)
