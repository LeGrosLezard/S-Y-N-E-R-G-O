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

    nb = 5
    #From the eyes contours, build a box.
    x, y, w, h = cv2.boundingRect(eye)

    #Region interest of the box from gray frame.
    cropGray = gray[y-nb : (y + h) + nb, x - nb : (x + w) + nb]

    #Egalize the region on gray frame.
    cropEgalize = cv2.equalizeHist(cropGray)
    #cv2.imshow("cropMask", cropMask)

    #Recuperate Region on the frame.
    cropImg = frame[y-nb : (y+h)+nb, x-nb : (x+w)+nb]
    #cv2.imshow("cropImg", cropImg)

    return cropEgalize, cropImg


def eye_contour_masking(img, eye, gray):
    """Recuperate contour of eyes points, delimitate that
    recuperate color and gray mask."""

    nb = 5
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
            if mask_eyes_gray[i, j] > 200:
                crop[i, j] = 255

    #cv2.imshow("treat_crop", crop)
 
    return crop



#===================================================== Pupille center part

def find_center_pupille(crop, mask_eyes_img, rayon):
    """Gaussian filter, search the max solo contour on thresh,
    make an erod on 3 neighboors, find center of the contours."""

    out = None, None, None

    #Eliminate noise with gaussian blur.
    gaussian = cv2.GaussianBlur(crop, (9, 9), 0)
    #cv2.imshow("gaussian", gaussian)

    for thresh in range(0, 200, 5):
        _, threshold = cv2.threshold(gaussian, thresh, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 1:
            break

    _, threshold = cv2.threshold(gaussian, thresh - 10, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow("threshold", threshold)

    blackPx = cv2.countNonZero(threshold)

    kernel = np.ones((3,3), np.uint8)

    if blackPx > 10:
        img_erosion = cv2.erode(threshold, kernel, iterations=1)
        #cv2.imshow("img_erosion", img_erosion)
    elif blackPx > 0:
        img_erosion = cv2.dilate(threshold, kernel, iterations=1)
    elif blackPx == 0:
        _, threshold = cv2.threshold(gaussian, thresh + 10, 255, cv2.THRESH_BINARY_INV)
        img_erosion = cv2.dilate(threshold, kernel, iterations=1)

    contours = cv2.findContours(img_erosion, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)[0]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    if len(contours) > 0:

        a = cv2.moments(contours[0])['m00']
        pupille_center = [(int(cv2.moments(contours[0])['m10']/a),
                          int(cv2.moments(contours[0])['m01']/a)) for cnt in contours if a > 0]

        if pupille_center != []:
            x_center, y_center = pupille_center[0][0], pupille_center[0][1]

            mask_eyes_img[y_center, x_center] = 0, 0, 255
            cv2.circle(mask_eyes_img, (x_center, y_center), rayon, (255, 255, 255), 1)

            out = x_center, y_center, mask_eyes_img
            #cv2.imshow("mask_eyes_img", mask_eyes_img)

            #cv2.waitKey(0)

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
    x_center, y_center, crop_eyes = find_center_pupille(gray_crop, mask_eyes_img, rayon)

    return (x_center, y_center), crop_eyes, crop_appli



def pupille_tracker(landmarks, frame, gray, head_box):

    eyes = recuperate_eyes(landmarks, frame)
    right_eye, left_eye = eyes

    glob_right, extremum_right = recuperate_extremums(right_eye, frame)
    glob_left, extremum_left   = recuperate_extremums(left_eye, frame)


    right_eye, crop_eyes_right, crop_appli_right = find_pupil_center(right_eye, frame, gray, glob_right)
    left_eye, crop_eyes_left, crop_appli_left  = find_pupil_center(left_eye, frame, gray, glob_left)

    face_movement(landmarks, frame, eyes, head_box)


    eyes_movements(frame, extremum_right, landmarks, 19, head_box)
    eyes_movements(frame, extremum_left, landmarks, 24, head_box)
    print("")



    return (right_eye, crop_eyes_right, crop_appli_right),\
           (left_eye, crop_eyes_left, crop_appli_left)








def face_movement(landmarks, frame, eyes, head_box):


    joue = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in [2, 41, 31] ])),
            cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in [35, 14, 46] ])))


    #cv2.drawContours(frame, [joue[0]], -1, (0, 255, 0), 1)
    contour_right_joue = cv2.contourArea(joue[0])
    #cv2.drawContours(frame, [joue[1]], -1, (0, 255, 0), 1)
    contour_left_joue = cv2.contourArea(joue[1])

    eyeR_pts = landmarks.part(36).x, landmarks.part(36).y
    eyeL_pts = landmarks.part(45).x, landmarks.part(45).y
    noze_pts = landmarks.part(30).x, landmarks.part(30).y

    head1 = landmarks.part(2).x, landmarks.part(2).y
    head2 = landmarks.part(14).x, landmarks.part(14).y


    turning = turn_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    print(turning)

    head_position = bent_up_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    print("head position : ", head_position)

    #if turning == ""






def eyes_movements(frame, extremum, landmarks, top, head_box):

    x, y, w, h = extremum

    eye = [(j, i) for i in range(y[1], h[1]) for j in range(x[0], w[0])
           if frame[i, j][0] == 0 and frame[i, j][1] == 0 and frame[i, j][2] == 255]

    nose = landmarks.part(27).x, landmarks.part(27).y
    haut = landmarks.part(top).x, landmarks.part(top).y


    if eye != []:

        cv2.line(frame, eye[0], nose, (0, 255, 0), 1)
        cv2.line(frame, eye[0], haut, (0, 255, 0), 1)

        eye_noze = dist.euclidean(eye[0], nose)
        eye_top = dist.euclidean(eye[0], haut)


        w = head_box[2]

        if top == 19:
            if eye_noze >=  w * 0.2825:
                print("yeux droite")
            elif eye_noze <= w * 0.233:
                print("yeux gauche")

        if top == 24:
            if eye_noze <= w * 0.2025:
                print("yeux droite")
            elif eye_noze >= w * 0.262:
                print("yeux gauche")

















