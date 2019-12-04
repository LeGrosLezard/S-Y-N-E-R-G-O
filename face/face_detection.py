from cv2 import rectangle, convexHull, Subdiv2D, bitwise_and, boundingRect, bitwise_not, circle, drawContours, polylines, fillPoly, moments, contourArea, imshow, resize, cvtColor, COLOR_BGR2GRAY, threshold, THRESH_BINARY, bilateralFilter, erode, countNonZero, findContours, RETR_TREE, CHAIN_APPROX_NONE, waitKey
from numpy import array, int32, hstack, zeros, uint8, min, max, full, ones
from math import pow, sqrt, sin, acos, hypot
from threading import Thread
from scipy.spatial import distance as dist


def points_landmarks(gray, predictor, detector):
    """ 68 points"""

    face = detector(gray)
    landmarks = predictor(gray, face[0])

    return landmarks, face


def intra_face(landmarks, faces, img):
    """Intra face"""

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


def exterior_face(face, img):

    #front + un peu plus
    rectangle(img, (face[0], face[1] - 50), (face[0] + face[2] , face[1] + face[3]), 3)

    #chevelure (effacer la tronche recupérer le pourtour ?)
    rectangle(img, (face[0] - 50, face[1] - 100), (face[0] + face[2] + 50, face[1] + face[3]), 3)



#-------------------------------------- yeux

def closing_eyes(eye):
    return (dist.euclidean(eye[1], eye[5]) + dist.euclidean(eye[2], eye[4])) / (2.0 * dist.euclidean(eye[0], eye[3]))

def make_mask(img, eye, gray):
    """Recuperate eye mask"""

    height, width = gray.shape[:2]
    black_frame = zeros((height, width), uint8)
    mask = full((height, width), 255, uint8)
    fillPoly(mask, [eye], (0, 0, 0))
    mask = bitwise_not(black_frame, gray.copy(), mask=mask)

    """Recuperate the eye area"""
    x, y, w, h = boundingRect(eye)
    cropMask = mask[y-5:y+h+5, x-5:x+w+5]
    cropImg = img[y-5:y+h+5, x-5:x+w+5]
    
    return cropMask, cropImg


def define_threshold(crop):
    """Recuperate the minimum contour by an automatic threshold"""

    minimum = 0
    for thresh in range(5, 100, 5):

        kernel = ones((3, 3), uint8)
        mask = bilateralFilter(crop, 10, 15, 15)
        mask = erode(mask, kernel, iterations=3)
        mask = threshold(mask, thresh, 255, THRESH_BINARY)[1]

        height, width = crop.shape[:2]
        nb_pixels = height * width
        blacks_pixels = nb_pixels - countNonZero(mask) / nb_pixels
        if blacks_pixels < minimum:
            minimum = blacks_pixels

    return threshold(mask, minimum, 255, THRESH_BINARY)[1]


def get_eyes(crop, thresh, cropPicture):
    """Recuperate center of contour"""

    out = "", ""

    contours = findContours(thresh, RETR_TREE, CHAIN_APPROX_NONE)[0][-2:]
    contours = sorted(contours, key=contourArea)

    try:
        moment = moments(contours[-2])
        x = int(moment['m10'] / moment['m00'])
        y = int(moment['m01'] / moment['m00'])

        circle(cropPicture, (x, y), 3, (0, 0, 255), 1)

        out = x, y

    except (IndexError, ZeroDivisionError):
        pass

    return out


#close
def tracking_eyes(landmarks, faces, img, gray):

    state = ""; min_ear = 0.3; max_ear = 0.5; left_ear = 0.4; right_ear = 0.4
    eyes = (convexHull(array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(36, 42)])),
            convexHull(array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(42, 48)])))

    try:
        left_ear = closing_eyes(eyes[0])
        right_ear = closing_eyes(eyes[1])
    except (IndexError):
        pass

    if left_ear <= min_ear and right_ear <= min_ear: state = "closed"
    elif left_ear <= min_ear: state = "gauche"
    elif right_ear <= min_ear: state = "droite"
    elif left_ear >= max_ear and right_ear >= max_ear: state= "very open eyes"
    else:

        #Recuperate a mask with only the contour of eye
        cropMaskLeft, cropImgLeft = make_mask(img, eyes[0], gray)
        cropMaskRight, cropImgRight = make_mask(img, eyes[1], gray)

        #Make an automatic threshold
        threshold_left = define_threshold(cropMaskLeft)
        threshold_right = define_threshold(cropMaskRight)
 
        #Recuperate center of the contour (pupil).
        x_left, y_left = get_eyes(cropMaskLeft, threshold_left, cropImgLeft)
        x_right, y_right = get_eyes(cropMaskRight, threshold_right, cropImgRight)


        def position(mask, x, y):


            imshow("mask", mask)
            waitKey(0)

            height, width = mask.shape
            blank_image = zeros((height, width, 3), uint8)
            blank_image[:, :] = 255, 255, 255
            a = int(width/3); b = int(height/3)
            rectangle(blank_image, (0, 0), (a, b), (58, 128, 58), 1)
            rectangle(blank_image, (0, b*2), (a, b), (100, 238, 229), 1)
            rectangle(blank_image, (0, b*3), (a, b*2), (44, 44, 210), 1)

            rectangle(blank_image, (a*2, 0), (a*3, b), (58, 128, 58), 1)
            rectangle(blank_image, (a*2, b*2), (a*3, b), (100, 238, 229), 1)
            rectangle(blank_image, (a*2, b*3), (a*3, b*2), (44, 44, 210), 1)

            circle(blank_image, (x, y), 3, (0, 0, 0), 1)

            imshow("dazdsq", blank_image)
            waitKey(0)

        if x_left != "" or y_left != "": 
            position(cropMaskLeft, x_left, y_left)




        print(x_left, y_left, x_right, y_right)
        




    if state != "": print(state)





    


#-------------------------------------- inclinaison

def inclinaison(landmarks, img):

    a = landmarks.part(36).x, landmarks.part(36).y
    b = landmarks.part(45).x, landmarks.part(45).y
    c = landmarks.part(30).x, landmarks.part(30).y

    d_eyes = sqrt(pow(a[0] - b[0], 2) + pow(a[1] - b[1], 2))
    d1 = sqrt(pow(a[0] - c[0], 2) + pow(a[1] - c[1], 2))
    d2 = sqrt(pow(b[0] - c[0], 2) + pow(b[1] - c[1], 2))
    coeff = d1 + d2

    cosb = min( (pow(d2, 2) - pow(d1, 2) + pow(d_eyes, 2) ) / (2*d2*d_eyes) )
    a1 = int(250*(d1-d2)/coeff)
    a2 = int(250*(d2*sin(acos(cosb))-coeff/4)/coeff)
    a3 = int(250*(a[1]-b[1])/coeff)
    head = ""

    if a1 < - 20: head += "a droite "
    elif a1 > 20: head += "a gauche "

    if a2 < 15: head += "en haut "
    elif a2 < 0: head += "tres haut "
    elif a2 > 30: head += "en bas "
    elif a2 > 40: head += "tres bas "

    if a3 < - 20: head += "et incline la tete a gauche "
    elif a3 > 20: head += "et incline la tete a droite "

    print(head)
    return head

