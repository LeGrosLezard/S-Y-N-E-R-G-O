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



facePoints = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\models\shape_predictor_68_face_landmarks.dat"


video_name = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\a.mp4"
xml = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\frontalEyes35x16.xml"




video = cv2.VideoCapture(video_name)

detector = get_frontal_face_detector()
predictor = shape_predictor(facePoints)



last = []

while True:


    frame = cv2.resize(video.read()[1], (800, 500))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    try:

        landmarks, face = points_landmarks(gray, predictor, detector)


        faces, convexhull = recuperate_intra_face_points(landmarks, face, frame)

        cv2.rectangle(frame, (faces[0], faces[1]), (faces[0] + faces[2], faces[1] + faces[3]), (0, 0, 255), 3)


        a = (landmarks.part(36).x, landmarks.part(36).y)
        b = (landmarks.part(37).x - 2, landmarks.part(37).y - 2)
        c = (landmarks.part(38).x + 2, landmarks.part(38).y - 2)
        d = (landmarks.part(39).x, landmarks.part(39).y)
        e = (landmarks.part(40).x, landmarks.part(40).y)
        f = (landmarks.part(41).x, landmarks.part(41).y)

        cv2.circle(frame, (landmarks.part(36).x, landmarks.part(36).y), 1, (0, 0, 255), 1)
        cv2.circle(frame, (landmarks.part(39).x, landmarks.part(39).y), 1, (0, 0, 255), 1)
        


        eyes = np.array([a, b, c, d, e, f])


        height, width = gray.shape[:2]
        black_frame = np.zeros((height, width), np.uint8)
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [eyes], (0, 0, 0))
        mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)

        x, y, w, h = cv2.boundingRect(eyes)

        cropMask = mask[y:y+h, x:x+w]
        height, width = cropMask.shape[:2]
        cropMask = cv2.resize(cropMask, (width*10, height*8))

        aa = frame[y:y+h, x:x+w]
        aa = cv2.resize(aa, (width*10, height*8))


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

        contours = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0][-2:]
        contours = sorted(contours, key=cv2.contourArea)
        nan = False
        try:
            moment = cv2.moments(contours[-1])
            x = int(moment['m10'] / moment['m00'])
            y = int(moment['m01'] / moment['m00'])
        except:
            pass

        cv2.circle(frame, (x, y), 1, (0, 0, 255), 1)


        print((0,0), x, y, (tresh.shape[1], tresh.shape[0]))

        if x > (0.65) * tresh.shape[1]:
            print("droite")

        elif x < 0.45 * tresh.shape[1]:
            print("gauche")

        if y < 0.40 * tresh.shape[0]:
            print("haut")

        elif y > 0.70 * tresh.shape[0]:
            print("bas")


   
        droite = ""
        gauche = ""
        droit_bas = ""
        droit_haut = ""
        gauche_bas = ""
        gauche_haut = ""


        cv2.imshow('cropMask', cropMask)
        cv2.imshow('tresh', tresh)
        cv2.imshow('aa', aa)








    except (IndexError):
        pass











    cv2.imshow('frame', frame)

    if cv2.waitKey(0) & 0xFF == ord("q"):
        break


