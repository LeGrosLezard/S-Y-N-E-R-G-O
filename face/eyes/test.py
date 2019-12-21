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

    cv2.fillPoly(mask, [eye], (0, 0, 255))

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
    #frame = cv2.resize(frame, (500, 400))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    faces = detector(gray)
    landmarks = predictor(gray, faces[0])


    eyes = [(landmarks.part(36).x + 2, landmarks.part(36).y),
            (landmarks.part(37).x , landmarks.part(37).y - 2),
            (landmarks.part(38).x + 5, landmarks.part(38).y - 2),
            (landmarks.part(39).x, landmarks.part(39).y),
            (landmarks.part(40).x, landmarks.part(40).y),
            (landmarks.part(41).x, landmarks.part(41).y)]

 
    eyes = cv2.convexHull(np.array(eyes))


    crop, maskimg = croping(frame, eyes, gray)
    crop = cv2.equalizeHist(crop)
    #cv2.imshow('crop', crop)

    #height, width = crop.shape[:2]
    #cropcrop = cv2.resize(crop, (width*4, height*4))
    #cv2.imshow('cropcrop', cropcrop)


    mask_eyes, aaaaaaaa = make_mask(frame, eyes, gray)
    #cv2.imshow('mask_eyes', mask_eyes)



    for i in range(mask_eyes.shape[0]):
        for j in range(mask_eyes.shape[1]):
            if mask_eyes[i, j] == 255:
                crop[i, j] = 255


    #height, width = crop.shape[:2]
    #crop = cv2.resize(crop, (width*4, height*4))
    #aaaaaaaa = cv2.resize(aaaaaaaa, (width*4, height*4))
    #cv2.imshow('after', crop)


    windowClose = np.ones((5,5),np.uint8)
    windowOpen = np.ones((5,5),np.uint8)
    windowErode = np.ones((2,2),np.uint8)


    ret, pupilFrame = cv2.threshold(crop,240,255,cv2.THRESH_BINARY)
    pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_CLOSE, windowClose)
    pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_ERODE, windowErode)
    pupilFrame = cv2.morphologyEx(pupilFrame, cv2.MORPH_OPEN, windowOpen)

    cv2.imshow('pupilFrame',pupilFrame)

    threshold = cv2.inRange(pupilFrame,250,255)
    contours, hierarchy = cv2.findContours(threshold,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)



    for cnt in contours:
        area = cv2.contourArea(cnt)
        center = cv2.moments(cnt)
        try:
            cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
            cv2.circle(aaaaaaaa,(cx,cy), 8, (0, 0, 255),1)
        except:pass

    cv2.imshow('aaaaaaaa',aaaaaaaa)




    









    cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


