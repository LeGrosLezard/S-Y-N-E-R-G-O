import cv2
import numpy as np




def make_contour(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    cv2.drawContours(frame, [area], 0, color, 1)

    return area.tolist()

def make_contour_by_range(area, color, frame, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    cv2.drawContours(frame, [area], 0, color, 1)

    return area.tolist()



def make_contour_NONE(points, color, frame):
    area = np.array([points])
    #cv2.drawContours(frame, [area], 0, color, 1)



def make_contour_by_range_NONE(points, color, frame):

    area = np.array([points])
    cv2.drawContours(frame, [area], 0, color, 1)


def make_mask_area(area, gray, frame):


    height, width = gray.shape[:2]
    nb = 0
    copy = frame.copy()
    black_frame = np.zeros((height, width), np.uint8)
    mask = np.full((height, width), 255, np.uint8)
    cv2.fillPoly(mask, [area], (0, 0, 255))
    mask = cv2.bitwise_not(black_frame, gray.copy(), mask=mask)

    x, y, w, h = cv2.boundingRect(area)
    cropMask = mask[y-nb : (y+h)+nb, x-nb : (x+w)+nb]

    return cropMask


def recup_pixels(cropMask):

    pixels = [(cropMask[i, j]) for i in range(cropMask.shape[0]) for j in range(cropMask.shape[1])]
    return pixels

def compare_pixels(PIXELS, pixels):

    diff = 0

    print(len(PIXELS), len(pixels))
    for i, j in zip(PIXELS, pixels):
        if i == j:
            diff += 1
    return diff



def head_tracker(head_box):
    pass
    #Ici on va suivre la tete
    #du genre droite 2px droite 2px plus rien donc droit 2px ? 1px ?
    #moindre jcrois


def head_size():
    pass
    #ICI on récuepre les dimensions des zones des fois trop petit
    #ou le truk deviens trop grand
    #si oui on récupere une autre d




AREA1 = []
AREA2 = []

CHEEK5 = []

a = 0
bb = []
cc = []
def face_area(frame, landmarks, subtractor, head_box):

    global AREA1
    global AREA2
    global CHEEK5
    global a
    global bb
    global cc


    areas =  { "cheek2":[54, 13, 16, 28], "chin":[58, 56, 9, 7],
               "beet_eyes" :[21, 22, 28], "chin1":[58, 7, 3, 48],
               "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
               "noze_area":[28, 48, 54], "mouse":(48, 50, 52, 54, 56, 58),
               "leftEye":(0, 17, 21, 28), "rightEye":(22, 26, 16, 28)}

    areas2 = {"onEye1":[17, 22], "onEye2":[22, 27]}

    gray = cv2.cvtColor(frame,cv2.COLOR_RGB2GRAY)

    if landmarks is not None:

        AREA1 = [make_contour(areas[k], (255,0,0), frame, landmarks)
                           for nb, k in enumerate(areas)]

        cropMask = make_mask_area(np.array(AREA1[5]), gray, frame)

        if a == 0:
            bb = cropMask
            a += 1
        else:
            w, h = bb.shape[:2]

            cc = cropMask
            cc = cv2.resize(cc, (h,w))

            a = 0



            h, w = bb.shape[:2]
            print(h, w)
            h, w = cc.shape[:2]
            print(h, w)

            diff = cv2.subtract(bb, cc)

            cv2.imshow("diff", np.array(diff))





        cheek5 = recup_pixels(cropMask)
        diff = compare_pixels(CHEEK5, cheek5)
        CHEEK5 = cheek5
        print(diff)



        AREA2 = [make_contour_by_range(areas2[k], (255,0,0), frame, landmarks)
                 for nb, k in enumerate(areas2)]



    else:

        for i in AREA1:
            make_contour_NONE(i, (0, 255, 0), frame)

        a, b, c = make_mask_area(np.array(AREA1[5]), gray, frame)


        for i in AREA2:
            make_contour_by_range_NONE(i, (0, 255, 0), frame)

    print("")



##






