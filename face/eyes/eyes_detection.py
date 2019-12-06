from cv2 import convexHull, boundingRect, bitwise_not, circle, fillPoly, moments, contourArea, threshold, THRESH_BINARY, bilateralFilter, erode, countNonZero, findContours, RETR_TREE, CHAIN_APPROX_NONE
from numpy import array, zeros, uint8, full, ones
from scipy.spatial import distance as dist

#Blinking function
def closing_eyes(eye):
    """ Recuperate eye report dist euclidien(widths) / 2 (length)"""
    return (dist.euclidean(eye[1], eye[5]) + dist.euclidean(eye[2], eye[4])) / (2.0 * dist.euclidean(eye[0], eye[3]))



#Recuperate eyes masks
def make_mask(img, eye, gray):
    """Recuperate contour of eyes, make a mask, recuperate the area."""

    height, width = gray.shape[:2]
    black_frame = zeros((height, width), uint8)
    mask = full((height, width), 255, uint8)
    fillPoly(mask, [eye], (0, 0, 0))
    mask = bitwise_not(black_frame, gray.copy(), mask=mask)

    """Recuperate the eye area"""
    x, y, w, h = boundingRect(eye)
    cropMask = mask[y-5:y+h+5, x-5:x+w+5]
    cropImg = img[y-5:y+h+5, x-5:x+w+5]

    return cropMask, cropImg, x-5, y-5, x + w+5, y + h+5


def define_threshold(crop):
    """Recuperate the minimum contour by an automatic threshold"""

    minimum_thresh = [10000, 0]

    for thresh in range(5, 100, 5):

        #Make a mask
        kernel = ones((3, 3), uint8)
        mask = bilateralFilter(crop, 10, 15, 15)
        mask = erode(mask, kernel, iterations=3)
        mask = threshold(mask, thresh, 255, THRESH_BINARY)[1]

        #Recuperate the min number's blacks pixels and his associate value of threshold filter
        height, width = crop.shape[:2]
        nb_pixels = height * width
        blacks_pixels = nb_pixels - countNonZero(mask) / nb_pixels
        if blacks_pixels < minimum_thresh[0]:
            minimum_thresh[0], minimum_thresh[1] = blacks_pixels, thresh

    return threshold(mask, minimum_thresh[1], 255, THRESH_BINARY)[1]



#Recuperate eyes movements
def get_eyes(crop, thresh, cropPicture, landmarks, num):
    """Recuperate center of contour"""

    out = None, None

    contours = findContours(thresh, RETR_TREE, CHAIN_APPROX_NONE)[0][-2:]
    contours = sorted(contours, key=contourArea)

    try:
        moment = moments(contours[-2])
        x = int(moment['m10'] / moment['m00'])
        y = int(moment['m01'] / moment['m00'])

        #circle(cropPicture, (x, y), 2, (0, 0, 255), 2)

        out = x, y

    except (IndexError, ZeroDivisionError):
        pass

    return out


def add_movement(movement, pos_eye, axis_eye):
    """Add + 1 if the movement isn't center"""

    if movement != "centre": pos_eye[movement] += 1
    elif movement == "centre":
        for k,v in axis_eye.items():
            pos_eye[k] = 0


def position_eye(crop, x, y, pos_eye):
    """Define 3 points, right center left in function of the
    dimensions of the crop, recuperate the min value of the center
    of the pupil.
    ex: crop = 40: right = 0, mid = 20 left = 40"""
    try:
        #Define center, left and right from the crop.
        horrizontal = {"centre": abs(crop.shape[0] / 2 - x), "droite":abs(x),
                       "gauche":abs(crop.shape[0] - x)}
        vertical = {"centre":abs(crop.shape[1] / 2 - y), "haut":abs(y),
                    "bas":abs(crop.shape[1] - y)}

        #Verify if the pupil tends to a side.
        verti = min(horrizontal, key=horrizontal.get)
        horri = min(vertical, key=vertical.get)

        #Add + 1 if movement isn't center.
        add_movement(verti, pos_eye, horrizontal)
        add_movement(horri, pos_eye, vertical)

    except TypeError:pass




#Analyse eyes positions
def recup_info(dico):
    """If a value is >= 3"""
    return list({k for k, v in dico.items() if v >= 3})


def analyse(left_eye, right_eye):
    """Verify if the two eyes are in the same position from
    3 frames"""

    no = []

    #Verify if a movement isn't center from 3 frames ago.
    left_gaze, right_gaze = recup_info(left_eye), recup_info(right_eye)
    #If yes display the last 3 movements.
    if left_gaze != no and right_gaze != no:
        gaze = [i for i in left_gaze for j in right_gaze if i == j]
        if gaze != []: print("regarde vers", gaze)



#Global function
def tracking_eyes(landmarks, faces, img, gray, left_eye, right_eye):
    """Define rapport eye min and max for blink eyes. Define the movement
    of them."""

    #Define min and max EAR. Recuperate exterior/convex points of the face.
    state = ""; min_ear = 0.3; max_ear = 0.5; left_ear = 0.4; right_ear = 0.4
    eyes = (convexHull(array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(36, 42)])),
            convexHull(array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(42, 48)])))

    try: #Calculus rapport of eye (EAR) 
        left_ear, right_ear = closing_eyes(eyes[0]), closing_eyes(eyes[1])
    except (IndexError): pass

    #Verify rapport eye ratio.
    if left_ear <= min_ear and right_ear <= min_ear: state = "closed"
    elif left_ear <= min_ear: state = "blinking gauche"
    elif right_ear <= min_ear: state = "blinking droite"
    elif left_ear >= max_ear and right_ear >= max_ear: state= "very open eyes"
    else:

        #Recuperate a mask with only the contour of eye
        cropMaskLeft, cropImgLeft, x, y, w, h = make_mask(img, eyes[0], gray)
        cropMaskRight, cropImgRight, x1, y1, w1, h1 = make_mask(img, eyes[1], gray)

        #Make an automatic threshold
        threshold_left = define_threshold(cropMaskLeft)
        threshold_right = define_threshold(cropMaskRight)

        #Recuperate center of the contour (pupil).
        x_left, y_left = get_eyes(cropMaskLeft, threshold_left, cropImgLeft, landmarks, 0)
        x_right, y_right = get_eyes(cropMaskRight, threshold_right, cropImgRight, landmarks, 1)

        #Analyse position of the eyes.
        position_eye(cropMaskLeft, x_left, y_left, left_eye)
        position_eye(cropMaskRight, x_right, y_right, right_eye)

        #Display it
        analyse(left_eye, right_eye)

    if state != "": print(state)
    
