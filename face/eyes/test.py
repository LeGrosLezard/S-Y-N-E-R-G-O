from dlib import get_frontal_face_detector, shape_predictor
import numpy as np
import cv2
import time


def croping(img, eye, gray):
    """Recuperate contour of eyes, make a mask, recuperate the area."""

    """Recuperate the eye area"""
    x, y, w, h = cv2.boundingRect(eye)
    cropMask = gray[y-5:y+h+5, x-5:x+w+5]
    cropImg = img[y-5:y+h+5, x-5:x+w+5]

    return cropMask, cropImg


def make_mask(img, eye, gray):
    """Recuperate contour of eyes, make a mask, recuperate the area."""

    height, width = gray.shape[:2]
    black_frame = np.zeros((height, width), np.uint8)

    mask = np.full((height, width), 255, np.uint8)



    cv2.fillPoly(mask, [eye], (0, 0, 0))


    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)



    """Recuperate the eye area"""
    x, y, w, h = cv2.boundingRect(eye)
    cropMask = mask[y-5:y+h+5, x-5:x+w+5]
    cropImg = img[y-5:y+h+5, x-5:x+w+5]

    return cropMask, cropImg



video = cv2.VideoCapture("a.mp4")
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:

    _, frame = video.read()
    frame = cv2.resize(frame, (500, 400))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    faces = detector(gray)
    landmarks = predictor(gray, faces[0])



    eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(36, 42)])),
            cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(42, 48)])))


    crop, maskimg = croping(frame, eyes[0], gray)
    crop = cv2.equalizeHist(crop)


    crop = cv2.resize(crop, (crop.shape[1] * 8, crop.shape[0] * 6))
    cv2.imshow('crop', crop)











    cropMask, cropImg = make_mask(frame, eyes[0], gray)
    th3 = cv2.equalizeHist(cropMask)
    cv2.imshow('th3', th3)



    contours, _ = cv2.findContours(th3, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    contours = sorted(contours, key=cv2.contourArea)


    cv2.drawContours(cropMask, [contours[0]], -1, (255, 255, 255), 1)





##    height, width = cropMask.shape[:2]
##    black_frame = np.zeros((height, width), np.uint8)
##    mask = np.full((height, width), 255, np.uint8)
##
##    cv2.fillPoly(mask, contours, (0, 0, 0))
##
##    maskmask = cv2.bitwise_not(black_frame, crop, mask=mask)
##
##    cv2.imshow('maskmask', maskmask)



    mask = cv2.resize(cropMask, (cropMask.shape[1] * 8, cropMask.shape[0] * 6))

    cv2.imshow('mask', mask)



    cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


