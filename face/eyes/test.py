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


def position(landmarks, points_position):

    pointsA = [0, 1, 2]
    pointsB = [16, 15, 14]

    out = False
    for i in range(len(pointsA)):
        a = landmarks.part(pointsA[i]).x
        b = landmarks.part(pointsB[i]).x



        if (b-a) < np.mean(points_position[i]) - 10 and np.mean(points_position[i]) < 110 :
            print("changement de plan recule")
            out = True
        elif (b-a) > np.mean(points_position[i]) + 10 and np.mean(points_position[i]) < 110:
            print("changement de plan, gros plan")
            out = True

        points_position[i].append(b-a)

    return out, b-a

facePoints = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\models\shape_predictor_68_face_landmarks.dat"


video_name = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\a.mp4"

video = cv2.VideoCapture(video_name)

detector = get_frontal_face_detector()
predictor = shape_predictor(facePoints)

xx = []
yy = []

xx1 = []
yy1 = []
points_position = [[], [], []]
while True:


    frame = cv2.resize(video.read()[1], (800, 500))
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)





    
    try:

        landmarks, face = points_landmarks(gray, predictor, detector)
        out, a = position(landmarks, points_position)
        print("iciiiiiiiiiiii", a)
        if out is True:
            xx = []
            yy = []
            points_position = [[], [], []]
            xx1 = []
            yy1 = []


        faces, convexhull = recuperate_intra_face_points(landmarks, face, frame)

        cv2.rectangle(frame, (faces[0], faces[1]), (faces[0] + faces[2], faces[1] + faces[3]), (0, 0, 255), 3)


        eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(36, 42)])),
                cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                        for pts in faces for n in range(42, 48)])))

        cv2.circle(frame, (landmarks.part(36).x, landmarks.part(36).y), 1, (0, 0, 255), 1)
        cv2.circle(frame, (landmarks.part(39).x, landmarks.part(39).y), 1, (0, 0, 255), 1)

        cv2.circle(frame, (landmarks.part(42).x, landmarks.part(42).y), 1, (0, 255, 255), 1)
        cv2.circle(frame, (landmarks.part(45).x, landmarks.part(45).y), 1, (0, 255, 255), 1)


        height, width = gray.shape[:2]
        black_frame = np.zeros((height, width), np.uint8)
        mask = np.full((height, width), 255, np.uint8)
        cv2.fillPoly(mask, [eyes[0]], (0, 0, 0))
        mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)

        x, y, w, h = cv2.boundingRect(eyes[0])
        cropMask = mask[y:y+h, x:x+w]
        cropImg = frame[y:y+h, x:x+w]

        height, width = cropMask.shape[:2]
        cropMask = cv2.resize(cropMask, (width*10, height*8))



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

            if a > 90 and a < 110:
                nb = 8
            elif a > 110:
                nb = 8
            elif a > 65 and a < 90:
                nb = 5
            if len(xx) > 5:

                if x <= np.mean(xx) - nb:
                    print("droite")
                    nan = True
                elif x >= np.mean(xx) + nb:
                    print("gauche")
                    nan = True
            
                print(np.mean(xx), x)
                print(np.mean(yy), y)
                

            if nan is False:
                xx.append(x)
                yy.append(y)

            cv2.circle(tresh, (x, y), 2, (255, 255, 255), 2)

        except (IndexError):
            pass













            



##
##        height, width = gray.shape[:2]
##        black_frame = np.zeros((height, width), np.uint8)
##        mask = np.full((height, width), 255, np.uint8)
##        cv2.fillPoly(mask, [eyes[0]], (0, 0, 0))
##        mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)
##
##        x, y, w, h = cv2.boundingRect(eyes[0])
##        cropMask = mask[y:y+h, x:x+w]
##        cropImg = frame[y:y+h, x:x+w]
##
##        height, width = cropMask.shape[:2]
##        cropMask = cv2.resize(cropMask, (width*10, height*8))
##
##
##
##        minimum_thresh = [10000, 0]
##        for thresh in range(5, 100, 5):
##
##            kernel = np.ones((3, 3), np.uint8)
##            mask = cv2.bilateralFilter(cropMask, 10, 15, 15)
##            mask = cv2.erode(mask, kernel, iterations=3)
##            mask = cv2.threshold(mask, thresh, 255, cv2.THRESH_BINARY)[1]
##
##            height, width = cropMask.shape[:2]
##            nb_pixels = height * width
##            blacks_pixels = nb_pixels - cv2.countNonZero(mask) / nb_pixels
##            if blacks_pixels < minimum_thresh[0]:
##                minimum_thresh[0], minimum_thresh[1] = blacks_pixels, thresh
##
##        tresh = cv2.threshold(mask, minimum_thresh[1], 255, cv2.THRESH_BINARY)[1]
##
##
##
##        contours = cv2.findContours(tresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[0][-2:]
##        contours = sorted(contours, key=cv2.contourArea)
##
##        try:
##            moment = cv2.moments(contours[-1])
##            x = int(moment['m10'] / moment['m00'])
##            y = int(moment['m01'] / moment['m00'])
##
##
##            if len(xx1) > 10:
##
##                if x < np.mean(xx1) - 5:
##                    print("droite")
##
##                elif x > np.mean(xx1) + 5:
##                    print("gauche")
##
##            
##                print(np.mean(xx1), x)
##                print(np.mean(yy1), y)
##
##
##
##            xx1.append(x)
##            yy1.append(y)
##
##            cv2.circle(tresh, (x, y), 2, (255, 255, 255), 2)
##
##
##
##
##
##        except (IndexError):
##            pass
##
##        cv2.imshow('cropMask', cropMask)
##        cv2.imshow('tresh', tresh)










    except (IndexError):
        pass




    cv2.imshow('frame', frame)

    if cv2.waitKey(0) & 0xFF == ord("q"):
        break


