import cv2
import numpy as np


def recup_YCrCb(img):

    b = 0; g = 0; r = 0; counter = 0
    for i in range(img.shape[0]):
         for j in range(img.shape[1]):

             b += img[i ,j][0]
             g += img[i ,j][1]
             r += img[i ,j][2]
             counter += 1

    b = b / counter
    g = g / counter
    r = r / counter

    print(b ,g, r)

    y = 0.299 * r
    cb = -0.1687 * r - 0.3313 * g + 0.5 * b + 128
    cr = 0.5 * r - 0.4187 * g - 0.0813 * b + 128

    print(y, cb, cr)






def skin_detector(crop):
    min_YCrCb = np.array([0,140,85],np.uint8)
    max_YCrCb = np.array([240,180,130],np.uint8)
    imageYCrCb = cv2.cvtColor(crop, cv2.COLOR_BGR2YCR_CB)
    skinRegionYCrCb = cv2.inRange(imageYCrCb,min_YCrCb,max_YCrCb)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    skinMask = cv2.dilate(skinRegionYCrCb, kernel, iterations = 2)

    skinYCrCb = cv2.bitwise_and(crop, crop, mask = skinMask)

    return skinYCrCb



im = cv2.imread("a171.jpg")
ycrb = skin_detector(im)
recup_YCrCb(im)



cv2.imshow("dza", im)
cv2.imshow("ycrb", ycrb)

cv2.waitKey(0)
