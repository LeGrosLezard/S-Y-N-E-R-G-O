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
    #cv2.imshow("cropGray", cropGray)

 
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

    crop = adjust_gamma(crop, 3)
    #cv2.imshow("crop2", crop)

    #Eliminate noise with gaussian blur.
    gaussian = cv2.GaussianBlur(crop, (9, 9), 50)
    cv2.imshow("gaussian", gaussian)


    for thresh in range(0, 200, 5):
        _, threshold = cv2.threshold(gaussian, thresh, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        if len(contours) > 1:
            break

    _, threshold = cv2.threshold(gaussian, thresh - 50, 255, cv2.THRESH_BINARY_INV)
    #cv2.imshow("threshold", threshold)

    blackPx = cv2.countNonZero(threshold)

    kernel = np.ones((1,1), np.uint8)

    if blackPx > 10:
        img_erosion = threshold
        #img_erosion = cv2.erode(threshold, kernel, iterations=1)
    elif blackPx > 0:
        img_erosion = threshold
        #img_erosion = cv2.dilate(threshold, kernel, iterations=1)
    elif blackPx == 0:
        _, threshold = cv2.threshold(gaussian, thresh + 10, 255, cv2.THRESH_BINARY_INV)
        img_erosion = cv2.dilate(threshold, kernel, iterations=1)

    cv2.imshow("img_erosion", img_erosion)

    contours = cv2.findContours(img_erosion, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[0]
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    if len(contours) > 0:
        #cv2.drawContours(mask_eyes_img, [contours[0]], -1, (0, 255, 0), 1)
        cntx = tuple(contours[0][contours[0][:, :, 0].argmin()][0])  #left
        cnty = tuple(contours[0][contours[0][:, :, 1].argmin()][0])  #right
        cntw = tuple(contours[0][contours[0][:, :, 0].argmax()][0])  #top
        cnth = tuple(contours[0][contours[0][:, :, 1].argmax()][0])  #bottom
 
        mask_eyes_img[cntx[1], cntx[0]] = 255, 0, 255
        mask_eyes_img[cntw[1], cntw[0]] = 255, 255, 0

        mask_eyes_img[cnty[1], cnty[0]] = 255, 255, 255
        mask_eyes_img[cnth[1], cnth[0]] = 0, 255, 255



    if len(contours) > 0:
        a = cv2.moments(contours[0])['m00']
        pupille_center = [(int(cv2.moments(contours[0])['m10']/a),
                          int(cv2.moments(contours[0])['m01']/a)) for cnt in contours if a > 0]

        if pupille_center != []:
            x_center, y_center = pupille_center[0][0], pupille_center[0][1]

            mask_eyes_img[y_center, x_center] = 0, 0, 255
            #cv2.circle(mask_eyes_img, (x_center, y_center), rayon, (255, 255, 255), 1)

            out = x_center, y_center, mask_eyes_img, contours[0]
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
    x_center, y_center, crop_eyes, cnts = find_center_pupille(gray_crop, mask_eyes_img, rayon)

    return (x_center, y_center), crop_eyes, crop_appli, cnts



def pupille_tracker(landmarks, frame, gray, head_box):

    eyes = recuperate_eyes(landmarks, frame)
    
    right_eye, left_eye = eyes

    glob_right, extremum_right = recuperate_extremums(right_eye, frame)
    glob_left, extremum_left   = recuperate_extremums(left_eye, frame)


    right_eye, crop_eyes_right, crop_appli_right, cnt1 = find_pupil_center(right_eye, frame, gray, glob_right)
    left_eye, crop_eyes_left, crop_appli_left, cnt2  = find_pupil_center(left_eye, frame, gray, glob_left)

    turning, bot_top = face_movement(landmarks, frame, eyes, head_box)

    #print(turning, bot_top)


    eyes_movements(frame, extremum_right, landmarks, 19, head_box, eyes, glob_right, turning, cnt1)

    eyes_movements(frame, extremum_left, landmarks, 24, head_box, eyes, glob_left, turning, cnt2)
    print("")



    return (right_eye, crop_eyes_right, crop_appli_right, cnt1),\
           (left_eye, crop_eyes_left, crop_appli_left, cnt2)








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

    out = None
    out1 = None
    
    turning = turn_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    #print(turning)

    head_position = bent_up_head(eyeR_pts, eyeL_pts, noze_pts, head_box)
    #print("head position : ", head_position)

    if turning == "legerement a gauche":
        out = "gauche"
    elif turning == "legerement a droite":
        out =  "droite"

    if head_position == "position baissé":
        out1 = "bas"
    elif head_position == "position levé":
        out1 = "haut"

    return out, out1





MEAN = 0
COUNTER = 0

def eyes_movements(frame, extremum, landmarks, top, head_box, eyes, glob, turning, cnt):


    global MEAN
    global COUNTER


    nb = 0.415

    if top == 19:



        
        xe, ye, we, he = extremum

        eye = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
               if frame[i, j][0] == 0 and frame[i, j][1] == 0 and frame[i, j][2] == 255]

        hauteur1 = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
                   if frame[i, j][0] == 255 and frame[i, j][1] == 255 and frame[i, j][2] == 255]

        hauteur2 = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
                   if frame[i, j][0] == 0 and frame[i, j][1] == 255 and frame[i, j][2] == 255]

    

        if eye != []:
            #cv2.circle(frame, eye[0], glob, (0, 0, 255), 1)

##            total = int(dist.euclidean( (eyes[0][3][0][0], 0), (eyes[0][0][0][0], 0) ))
##            print("total", total, int(total * nb))
##
##            gauche = dist.euclidean( (eyes[0][3][0][0], 0), (eye[0][0], 0) )
##            print("dist gauche", gauche)
##
##            droite = dist.euclidean( (eyes[0][0][0][0], 0), (eye[0][0], 0) )
##            print("dist droite", droite)
##
##
##            if gauche <= int(total * nb):
##                print("oeil gauche")
##            elif droite <= int(total * nb):
##                print("oeil droite")


            eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                            for n in range(36, 42)])),
                    cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                            for n in range(42, 48)])))
            cv2.drawContours(frame, [eyes[0]], -1, (0, 0, 255), 1)

            
            aa = landmarks.part(36).x, landmarks.part(36).y
            bb = landmarks.part(39).x, landmarks.part(39).y
            cc = int((aa[1] + bb[1])/2)


            mid_top = dist.euclidean((0, cc), (0, eye[0][1]))
            print("milieu pupille", mid_top)



            a = landmarks.part(41).x, landmarks.part(41).y
            b = landmarks.part(40).x, landmarks.part(40).y
            c = int((a[1] + b[1])/2)

            d = landmarks.part(37).x, landmarks.part(37).y
            e = landmarks.part(38).x, landmarks.part(38).y
            f = int((d[1] + e[1])/2)


            hauteur = dist.euclidean( (0, c), (0, f) )

            print("head", head_box[3], "total", hauteur)

            if mid_top >= int(hauteur * 0.34) and hauteur >= int(head_box[3] * 0.065):
                print("ENFIN")





##    if top == 24:
##
##
##
##
##
##        xe, ye, we, he = extremum
##
##        eye = [(j, i) for i in range(ye[1], he[1]) for j in range(xe[0], we[0])
##               if frame[i, j][0] == 0 and frame[i, j][1] == 0 and frame[i, j][2] == 255]
##
##
##
##        if eye != []:
##
##            cv2.circle(frame, eye[0], glob, (0, 0, 255), 1)
##
####            total = int(dist.euclidean( (eyes[1][3][0][0], 0), (eyes[1][0][0][0], 0) ))
####            print(total, total * nb)
####
####            gauche = dist.euclidean( (eyes[1][3][0][0], 0), (eye[0][0], 0) )
####            print("dist gauche", gauche)
####
####            droite = dist.euclidean( (eyes[1][0][0][0], 0), (eye[0][0], 0) )
####            print("dist droite", droite)
####
####            if gauche <= int(total * nb):
####                print("oeil gauche")
####            elif droite <= int(total * nb):
####                print("oeil droite")
##
##
##            eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
##                            for n in [43, 44, 46, 47] ])))
##
##
##
##
##            top = landmarks.part(43).x, landmarks.part(43).y
##            bot = landmarks.part(47).x, landmarks.part(47).y
##
##            total = int(dist.euclidean((0, top[1]), (0, bot[1])))
##
##            eye_top = int(dist.euclidean((0, top[1]), (0, eye[0][1])))
##            eye_bot = int(dist.euclidean((0, bot[1]), (0, eye[0][1])))
##
##            print(total, int(total * 0.455), eye_top, eye_bot)
##            print(int(total * 0.42), abs(eye_top-eye_bot))
##
##            if eye_top <= int(total * 0.42) and abs(eye_top-eye_bot) >= int(total * 0.35):
##                print("haut")
##
##
##
##


    print("")















