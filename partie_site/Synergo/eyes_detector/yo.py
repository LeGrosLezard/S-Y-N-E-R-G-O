"""
by any chance you fall here?

we resize the frame for speed and recover grayscale for face detection from dlib.
we define the eyes; by the points of dlib we recover

the convex points and transform them into points numpy in matrix for only
have the periphery of the eyes in a rectangle (inside eyes = white, exterior = white)

then we collect the points of the eyes to recover the rectangle
that surrounds the eyes we do a color equalization


we superpose the periphery and the rectangle,
we have an egalized picture Firstly and a focused eye secondly.
We apply all white pixels from the focused eye on the egalized picture.
We now only have pupil.

Now we search contours (only < 80% of the focused picture) and
take their centers !

force with you

"""


import cv2
import numpy as np
from bent_up_head import bent_up_head
from turn_head import turn_head
from scipy.spatial import distance as dist


#===================================================== Recuperate eyes

def recuperate_eyes(landmarks, frame):
    """Recuperate DLIB eyes points"""

    #1) - convexhull = convex points of the contours.
    #2) - to numpy array
    eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for n in range(36, 42)])),
            cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for n in range(42, 48)])))

    return eyes


def recuperate_extremums(eye_contours, frame):
    """Recuperate extremum for eyes movement and glob occular rayon"""

    x = tuple(eye_contours[eye_contours[:, :, 0].argmin()][0])  #left
    y = tuple(eye_contours[eye_contours[:, :, 1].argmin()][0])  #right
    w = tuple(eye_contours[eye_contours[:, :, 0].argmax()][0])  #top
    h = tuple(eye_contours[eye_contours[:, :, 1].argmax()][0])  #bottom
    
    #[cv2.circle(frame, (i), 1, (255, 0, 0), 1) for i in [x, w]]

    occular_glob = abs(int((y[1] - h[1]) / 2))
    return occular_glob, (x, y, w, h)


#===================================================== Get eye
def rectangle_eye_area(frame, eye, gray):
    """Recuperate contour of eyes in a box, make an egalizer,
    make a color and gray mask."""

    nb = 10
    #From the eyes contours, build a box.
    x, y, w, h = cv2.boundingRect(eye)

    #Region interest of the box from gray frame.
    cropGray = gray[y-nb : (y + h) + nb, x - nb : (x + w) + nb]
    #cv2.imshow("cropGray", cropGray)

 
    #Egalize the region on gray frame.
    cropEgalize = cv2.equalizeHist(cropGray)
    #cv2.imshow("cropMask", cropMask)

    #Recuperate Region on the frame.
    cropImg = frame[y-nb : (y+h)+nb, x-nb : (x+w)+nb]
    #cv2.imshow("cropImg", cropImg)

    return cropEgalize, cropImg

def adjust_gamma(image, gamma):
    """We add light to the video, we play with gamma"""

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)
def eye_contour_masking(img, eye, gray):
    """Recuperate contour of eyes points, delimitate that
    recuperate color and gray mask."""

    nb = 10
    height, width = gray.shape[:2]

    black_frame = np.zeros((height, width), np.uint8)   #empty picture
    mask = np.full((height, width), 255, np.uint8)      #Mask
    cv2.fillPoly(mask, [eye], (0, 0, 255))              #

    #recuperate region interest.
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)
    #cv2.imshow("mask", mask)

    (x, y, w, h) = cv2.boundingRect(eye)

    cropMask   = mask[y - nb  : (y+h) + nb, x - nb  : (x+w) + nb]   #
    cropImg    = img[ y  - nb : (y+h) + nb, x - nb  : (x+w) + nb]
    crop_appli = img[ y  - 10 : (y+h) + 10, x - nb  : (x+w) + nb]   #for an extern appli
    cropMask = gray[y-nb:(y+h) + nb, x-nb:(x+w)+nb]
    cropMask = cv2.equalizeHist(cropMask)

    cropMask = adjust_gamma(cropMask, 2)

    return cropMask, cropImg, crop_appli




def superpose_contour_eye_rectangle(mask_eyes_gray, crop):
    """ - mask_eyes_gray's the interior of the eyes.
        - crop's the crop of the frame. (crop treat by an egalizer.)

        Superpose the mask (white part) on the crop for recuperate.
        the iris."""

    #cv2.imshow("mask_eyes_gray", mask_eyes_gray)
    #cv2.imshow("crop", crop)

    for i in range(mask_eyes_gray.shape[0]):
        for j in range(mask_eyes_gray.shape[1]):
            if mask_eyes_gray[i, j] > 120:
                crop[i, j] = 255


    cv2.imshow("treat_crop", crop)
 
    return crop



#===================================================== Pupille center part
def adjust_gamma(image, gamma):
    """We add light to the video, we play with gamma"""

    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
            for i in np.arange(0, 256)]).astype("uint8")

    return cv2.LUT(image, table)


def find_center_pupille(crop, mask_eyes_img, rayon):
    """Gaussian filter, search the max solo contour on thresh,
    make an erod on 3 neighboors, find center of the contours."""

    out = None, None, None, None

    #cv2.imshow("crop", crop)
    crop = adjust_gamma(crop, 1.5)

    #Eliminate noise with gaussian blur.
    gaussian = cv2.GaussianBlur(crop, (9, 9), 20)

    for i in range(gaussian.shape[1]):
        for j in range(gaussian.shape[0]):
            if gaussian[j, i] < 60:
                gaussian[j, i] = 0
    
    cv2.imshow("gaussian", gaussian)


    for thresh in range(0, 200, 1):
        _, threshold = cv2.threshold(gaussian, thresh, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 1:
            break


    _, threshold = cv2.threshold(gaussian, thresh, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("threshold", threshold)

    blackPx = cv2.countNonZero(threshold)

    kernel = np.ones((1,1), np.uint8)

    if blackPx > 10:

        img_erosion = cv2.dilate(threshold, kernel, iterations=1)
    elif blackPx > 0:

        img_erosion = cv2.dilate(threshold, kernel, iterations=1)
    elif blackPx == 0:
        _, threshold = cv2.threshold(gaussian, thresh + 10, 255, cv2.THRESH_BINARY_INV)
        img_erosion = cv2.dilate(threshold, kernel, iterations=1)

    cv2.imshow("img_erosion", img_erosion)

    contours = cv2.findContours(img_erosion, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

##    if len(contours) > 0:
##        cv2.drawContours(mask_eyes_img, [contours[0]], -1, (0, 255, 0), 1)




    if len(contours) > 0:
        a = cv2.moments(contours[0])['m00']
        pupille_center = [(int(cv2.moments(contours[0])['m10']/a),
                          int(cv2.moments(contours[0])['m01']/a)) for cnt in contours if a > 0]

        if pupille_center != []:
            x_center, y_center = pupille_center[0][0], pupille_center[0][1]

            mask_eyes_img[y_center, x_center] = 0, 0, 255
            cv2.circle(mask_eyes_img, (x_center, y_center), rayon, (0, 0, 255), 1)

            out = x_center, y_center, mask_eyes_img, contours[0]
            #cv2.imshow("mask_eyes_img", mask_eyes_img)



    return out


#===================================================== Main

def find_pupil_center(eye, frame, gray, rayon):
    """Recuperate egalized rectangle area or box area,
       recuperate contour eyes,
       Superpose egalized rectangle with contour eyes,
       find centers"""

    #Box egalized eyes areas
    gray_crop, color_crop = rectangle_eye_area(frame, eye, gray)

    #Contours of the broder of the eyes
    mask_eyes_gray, mask_eyes_img, crop_appli = eye_contour_masking(frame, eye, gray)

    #Superpose box and contours
    gray_crop = superpose_contour_eye_rectangle(mask_eyes_gray, gray_crop)

    #Define centers of pupils
    x_center, y_center, crop_eyes, cnts = find_center_pupille(gray_crop, mask_eyes_img, rayon)

    return (x_center, y_center), crop_eyes, crop_appli, cnts



def pupille_tracker(landmarks, frame, gray, head_box):

    eyes = recuperate_eyes(landmarks, frame)
    
    right_eye, left_eye = eyes

    glob_right, extremum_right = recuperate_extremums(right_eye, frame)
    glob_left, extremum_left   = recuperate_extremums(left_eye, frame)


    right_eye, crop_eyes_right, crop_appli_right, cnt1 = find_pupil_center(right_eye, frame, gray, glob_right)
    left_eye, crop_eyes_left, crop_appli_left, cnt2  = find_pupil_center(left_eye, frame, gray, glob_left)


    return (right_eye, crop_eyes_right, crop_appli_right, cnt1),\
           (left_eye, crop_eyes_left, crop_appli_left, cnt2)









