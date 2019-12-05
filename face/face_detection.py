from cv2 import rectangle, convexHull, Subdiv2D, line, bitwise_and, boundingRect, bitwise_not, circle, drawContours, polylines, fillPoly, moments, contourArea, imshow, resize, cvtColor, COLOR_BGR2GRAY, threshold, THRESH_BINARY, bilateralFilter, erode, countNonZero, findContours, RETR_TREE, CHAIN_APPROX_NONE, waitKey
from numpy import array, int32, hstack, zeros, uint8, full, ones
from numpy import min as np_min
from math import pow, sqrt, sin, acos, hypot
from threading import Thread
from scipy.spatial import distance as dist


def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""

    face = detector(gray)
    return predictor(gray, face[0]), face


#Interior of face
def intra_face(landmarks, faces, img):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    #points of face
    points = [(landmarks.part(n).x, landmarks.part(n).y)
               for pts in faces for n in range(0, 68)]

    #Convex points (contour of face)
    convexhull = convexHull(array(points))

    head = boundingRect(convexhull)

    #Find triangles into rectangles points (face)
    subdiv = Subdiv2D(head)

    #Put points for extract the list
    subdiv.insert(points)

    #Get triangles list
    triangles = array(subdiv.getTriangleList(), dtype=int32)

    #Recup points
    t_points = [[(t[0], t[1]), (t[2], t[3]), (t[4], t[5])] for t in triangles ]

    return t_points, head, convexhull


#Exterior of face
def exterior_face(face, img):
    """Recuperate area of the forehead and of the exterior of the head"""

    #front + un peu plus
    rectangle(img, (face[0], face[1] - 50), (face[0] + face[2] , face[1] + face[3]), 3)

    #chevelure (effacer la tronche recupérer le pourtour ?)
    rectangle(img, (face[0] - 50, face[1] - 100), (face[0] + face[2] + 50, face[1] + face[3]), 3)



#---------------------------------------------------------------------------------------------------- eye

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
def ana(dico):
    """If a value is >= 3"""
    return list({k for k, v in dico.items() if v >= 3})


def analyse(left_eye, right_eye):
    """Verify if the two eyes are in the same position from
    3 frames"""

    no = []

    #Verify if a movement isn't center from 3 frames ago.
    left_gaze, right_gaze = ana(left_eye), ana(right_eye)
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
    

#---------------------------------------------------------------------------------------------------- yeux
    
#---------------------------------------------------------------------------------------------------- inclinaison

def inclinaison(landmarks, img):
    """Analyse angles of the triangle beetween eyes and nose points"""

    #Recuperate landmarks.
    a = landmarks.part(36).x, landmarks.part(36).y
    b = landmarks.part(45).x, landmarks.part(45).y
    c = landmarks.part(30).x, landmarks.part(30).y

    #Recuperate distances.
    d_eyes = dist.euclidean(a, b) 
    d1 = dist.euclidean(a, c) 
    d2 = dist.euclidean(b, c) 

    coeff = d1 + d2

    #Calculus angle.
    cosb = np_min( (pow(d2, 2) - pow(d1, 2) + pow(d_eyes, 2) ) / (2*d2*d_eyes) )
    a1 = int(250*(d1-d2)/coeff)
    a2 = int(250*(d2*sin(acos(cosb))-coeff/4)/coeff)
    a3 = int(250*(a[1]-b[1])/coeff)
    head = ""

    #Display it
    if a1 < - 20: head += "a droite "
    elif a1 > 20: head += "a gauche "

    if a2 < 15: head += "en haut "
    elif a2 < 0: head += "tres haut "
    elif a2 > 30: head += "en bas "
    elif a2 > 40: head += "tres bas "

    if a3 < - 20: head += "et incline la tete a gauche "
    elif a3 > 20: head += "et incline la tete a droite "

    #print(head)
    return head, a1, a2
#---------------------------------------------------------------------------------------------------- inclinaison
