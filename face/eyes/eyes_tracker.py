from dlib import get_frontal_face_detector, shape_predictor
import numpy as np
import cv2
import time
import matplotlib.pyplot as plt



#===================================================== Video part
def resize_frame(frame):

    height, width = frame.shape[:2]
    frame = cv2.resize(frame, (int(width / 1.1), int(height / 1.1)))
    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    return frame, gray

    





def croping(img, eye, gray):
    """Recuperate contour of eyes, make a mask, recuperate the area."""

    """Recuperate the eye area"""
    x, y, w, h = cv2.boundingRect(eye)
    cropMask = gray[y-5:y+h+5, x-5:x+w+5]
    cropMask = cv2.equalizeHist(cropMask)

    cropImg = img[y-5:y+h+5, x-5:x+w+5]

    return cropMask, cropImg


def make_mask(img, eye, gray):
    """Recuperate contour of eyes, make a mask, recuperate the area."""

    height, width = gray.shape[:2]
    black_frame = np.zeros((height, width), np.uint8)
    mask = np.full((height, width), 255, np.uint8)
    cv2.fillPoly(mask, [eye], (0, 0, 255))
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)

    x, y, w, h = cv2.boundingRect(eye)
    cropMask = mask[y-5:y+h+5, x-5:x+w+5]
    cropImg = img[y-5:y+h+5, x-5:x+w+5]

    return cropMask, cropImg


def make_masking(mask_eyes_gray, crop):
    for i in range(mask_eyes_gray.shape[0]):
        for j in range(mask_eyes_gray.shape[1]):
            if mask_eyes_gray[i, j] == 255:
                crop[i, j] = 255
    return crop



def find_center_pupille(crop, mask_eyes_img):

    contours, hierarchy = cv2.findContours(crop, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    for cnt in contours:

        if cv2.contourArea(cnt) < (0.80 * (mask_eyes_img.shape[0] * mask_eyes_img.shape[1])):

            area = cv2.contourArea(cnt)
            center = cv2.moments(cnt)
            try:
                cx,cy = int(center['m10']/center['m00']), int(center['m01']/center['m00'])
                cv2.circle(mask_eyes_img, (cx,cy), 6, (0, 0, 255),2)
            except:pass

video = cv2.VideoCapture("a.mp4")
detector = get_frontal_face_detector()
predictor = shape_predictor("shape_predictor_68_face_landmarks.dat")


while True:

    _, frame = video.read()
    frame, gray = resize_frame(frame)

    faces = detector(gray)
    landmarks = predictor(gray, faces[0])


    eyes = (cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(36, 42)])),
            cv2.convexHull(np.array([(landmarks.part(n).x, landmarks.part(n).y)
                    for pts in faces for n in range(42, 48)])))


    right_eyes = cv2.convexHull(np.array(eyes[0]))

    right_crop, right_maskimg = croping(frame, right_eyes, gray)
    right_mask_eyes_gray, right_mask_eyes_img = make_mask(frame, right_eyes, gray)

    right_crop = make_masking(right_mask_eyes_gray, right_crop)

    find_center_pupille(right_crop, right_mask_eyes_img)



    left_eyes = cv2.convexHull(np.array(eyes[1]))

    left_crop, left_maskimg = croping(frame, left_eyes, gray)
    left_mask_eyes_gray, left_mask_eyes_img = make_mask(frame, left_eyes, gray)

    left_crop = make_masking(left_mask_eyes_gray, left_crop)

    find_center_pupille(left_crop, left_mask_eyes_img)



    cv2.imshow('frame', frame)
    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    
video.release()
cv2.destroyAllWindows()


