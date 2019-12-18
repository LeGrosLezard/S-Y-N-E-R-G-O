from dlib import get_frontal_face_detector, shape_predictor
import cv2
import numpy as np


def points_landmarks(gray, predictor, detector):
    """ Return the 68 points of the face and the face"""
    face = detector(gray)
    return predictor(gray, face[0]), face

def recuperate_intra_face_points(landmarks, faces, img):
    """Recuperate all coordiantes of landmarks (faces points).
    Recuperate convex points (exterior of face) and triangle
    points (area of the interior of the face)."""

    points = [(landmarks.part(n).x, landmarks.part(n).y) for pts in faces for n in range(0, 68)]
    convexhull = cv2.convexHull(np.array(points))
    head = cv2.boundingRect(convexhull)
    return head, convexhull


def masking_for_eyes(eyes):
    height, width = gray.shape[:2]
    black_frame = np.zeros((height, width), np.uint8)
    mask = np.full((height, width), 255, np.uint8)
    cv2.fillPoly(mask, [eyes], (0, 0, 0))
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)

    x, y, w, h = cv2.boundingRect(eyes)

    cropMask = mask[y:y+h, x:x+w]
    return cropMask


def rezsizing(crop):

    height, width = crop.shape[:2]
    crop = cv2.resize(crop, (width*2, height*2))
    return crop


def position(landmarks, points_position):

    pointsA = [0, 1, 2]
    pointsB = [16, 15, 14]

    out = False
    for i in range(len(pointsA)):
        a = landmarks.part(pointsA[i]).x
        b = landmarks.part(pointsB[i]).x

        if (b-a) < mean(points_position[i]) - 10:
            print("changement de plan recule")
            out = True
        elif (b-a) > mean(points_position[i]) + 10:
            print("changement de plan, gros plan")
            out = True

        points_position[i].append(b-a)

    return out


def define_threshold(cropMask):

    minimum_thresh = [10000, 0]
    for thresh in range(5, 100, 5):

        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.bilateralFilter(cropMask, 10, 15, 15)
        mask = cv2.erode(mask, kernel, iterations=3)
        mask = cv2.threshold(mask, thresh, 255, cv2.THRESH_BINARY)[1]

        height, width = cropMask.shape[:2]
        nb_pixels = height * width
        blacks_pixels = nb_pixels - cv2.countNonZero(mask) / nb_pixels
        if blacks_pixels < minimum_thresh[0]:
            minimum_thresh[0], minimum_thresh[1] = blacks_pixels, thresh

    tresh = cv2.threshold(mask, minimum_thresh[1], 255, cv2.THRESH_BINARY)[1]

    return tresh

def find_center(tresh):
    out = "", ""
    contours = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0][-2:]
    contours = sorted(contours, key=cv2.contourArea)
    nan = False
    try:
        moment = cv2.moments(contours[-1])
        x = int(moment['m10'] / moment['m00'])
        y = int(moment['m01'] / moment['m00'])
        out = x, y
    except:
        pass

    return out


facePoints = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\models\shape_predictor_68_face_landmarks.dat"
video_name = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\a.mp4"





video = cv2.VideoCapture(video_name)

detector = get_frontal_face_detector()
predictor = shape_predictor(facePoints)



points_position = [[], [], []]

while True:

    try:
        frame = cv2.resize(video.read()[1], (500, 400))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        landmarks, face = points_landmarks(gray, predictor, detector)
        position(landmarks, points_position)

        faces, convexhull = recuperate_intra_face_points(landmarks, face, frame)

        crop_face = frame[faces[1]:faces[1] + faces[3], faces[0]:faces[0] + faces[2]]

        eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(36, 42)])),
                cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(42, 48)])))

        for i in eyes[0]:
            cv2.circle(frame, (i[0][0], i[0][1]), 1, (0, 0, 255), 1)

        for i in eyes[1]:
            cv2.circle(frame, (i[0][0], i[0][1]), 1, (255, 0, 0), 1)


        cv2.imshow('crop_face', crop_face)



        cropMask1 = masking_for_eyes(eyes[0])
        cropMask1 = rezsizing(cropMask1)

        cropMask2 = masking_for_eyes(eyes[1])
        cropMask2 = rezsizing(cropMask2)

        cv2.imshow('cropMask1', cropMask1)
        cv2.imshow('cropMask2', cropMask2)


        tresh = define_threshold(cropMask1)
        tresh2 = define_threshold(cropMask2)


        x, y = find_center(tresh1)
        #x1, y1 = find_center(tresh2)


        print((0,0), x, y, (tresh.shape[1], tresh.shape[0]))


        if x > (0.65) * tresh.shape[1]:
            print("droite")

        elif x < 0.45 * tresh.shape[1]:
            print("gauche")

        if x > 0.65 * tresh.shape[1] and y > 0.48 * tresh.shape[0]:
            print("droite bas")

        if x > 0.65 * tresh.shape[1] and y < 0.45 * tresh.shape[0]:
            print("droite haut")

        if x < 0.45 * tresh.shape[1] and y < 0.45 * tresh.shape[0]:
            print("gauche haut")

        if x < 0.45 * tresh.shape[1] and y > 0.48 * tresh.shape[0]:
            print("gauche bas")


    except:
        pass



    if cv2.waitKey(0) & 0xFF == ord("q"):
        break


