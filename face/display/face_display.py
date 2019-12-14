from cv2 import bitwise_and, polylines, fillConvexPoly, imshow, imread, resize, cvtColor, COLOR_BGR2GRAY, line, boundingRect, copyMakeBorder, BORDER_CONSTANT
from numpy import zeros_like, hstack, empty, uint8, vstack
from PIL import Image
import cv2
import numpy as np


def mask_head(gray, img, copy, convexhull):
    mask = zeros_like(gray)
    polylines(copy, [convexhull], True, (0, 0, 255), 1)
    fillConvexPoly(mask, convexhull, 255)
    face = bitwise_and(copy, copy, mask=mask)

    return face


def make_rectangle(area, color, img, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    x, y, w, h = boundingRect(area)
    cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)

def make_contour(area, color, img, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    cv2.drawContours(img, [area], 0, color, 1)

def crop_rectangle(area, color, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(area[0], area[1])])
    x, y, w, h = boundingRect(area)
    return x - 5, y - 5, w + 5, h + 10

def crop_contour(area, color, landmarks):
    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in area])
    return boundingRect(area)

def concatenate_areas(area):

    numpy_horizontal_concat = np.concatenate( (area[0], area[1]), axis=1 )
    numpy_horizontal_concat2 = np.concatenate( (area[7], area[9]), axis=1 )

    for i in range(2, 6): numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, area[i]), axis=1 )
    for i in range(8, 12): numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2,  area[i]), axis=1 )

    return np.vstack( (numpy_horizontal_concat, numpy_horizontal_concat2) )


def make_border(img, areas):
    return copyMakeBorder(areas, top=0,bottom=0, left=0,right=540, borderType=BORDER_CONSTANT, value=[0, 0, 0])

def intra_face_displaying(img, gray, landmarks, face, fgbg, displaying):


    areas =  { "beet_eyes" :[21, 22, 27], "chin":[58, 56, 9, 7], "chin1":[58, 7, 3, 48],  "chin2": [56, 54, 13, 9],
               "cheek1": [48, 3, 0, 28], "cheek2":[54, 13, 16, 28], "noze_area":[27, 48, 54], "mouse":(48, 61),
               "onEye1":(17, 22), "onEye2":(22, 27), "leftEye":(36, 42), "rightEye":(42, 48) }

    area_by_contour = [crop_contour(areas[k], (0,255,0), landmarks) for nb, k in enumerate(areas) if nb <= 6]
    area_by_rectangle = [crop_rectangle(areas[k], (0,255,0), landmarks) for nb, k in enumerate(areas) if nb > 6]
    area = [cv2.resize(img[i[1]:i[1] + i[3], i[0]:i[0] + i[2]], (100, 50)) for i in area_by_contour + area_by_rectangle]

    areas = concatenate_areas(area)
    areas = make_border(img, areas)

    return areas


def face_displaying(gray, img, convexhull, head_points, landmarks, fgbg):

    copy = img.copy()
    areas =  { "beet_eyes" :[21, 22, 27], "chin":[58, 56, 9, 7], "chin1":[58, 7, 3, 48],
               "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
               "cheek2":[54, 13, 16, 28], "noze_area":[27, 48, 54], "mouse":(48, 61),
               "onEye1":(17, 22), "onEye2":(22, 27), "leftEye":(36, 42), "rightEye":(42, 48)}

    [make_contour(areas[k], (0,0,255), copy, landmarks) for nb, k in enumerate(areas) if nb <= 6]
    [make_rectangle(areas[k], (0,255,0), copy, landmarks) for nb, k in enumerate(areas) if nb > 6]

    face = mask_head(gray, img, copy, convexhull)
    image = imread(r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\display\face_pictures\head_model.jpg")
    head_model = resize(image, (int(gray.shape[1]/2), gray.shape[0]))


    displaying = hstack((head_model, img))
    displaying = hstack((displaying, face))

    areas = intra_face_displaying(img, gray, landmarks, face, fgbg, displaying)
    areas = cv2.resize(areas, (int(displaying.shape[1]), int(areas.shape[0])) )

    horizontal_concat = vstack( (areas, displaying) )



    cv2.imshow("horizontal_concat", horizontal_concat)











 














##def emotion_points(img, landmarks):
##
##    import cv2
##
##    anatomy_y =  {"open_mouse_points_top" :[61, 62, 63], "open_mouse_points_bot":[67, 66, 65],
##                  "top_eyes_left": [37, 38], "bot_eyes_left":[41, 40],
##                  "top_eyes_right":[43, 44], "bot_eyes_right":[47, 46],
##                  "on_eye_right":[17, 18, 19, 20, 21], "on_eye_left":[22, 23, 24, 25, 26]}
##
##    anatomy_x = {"right_side_mouse": [48], "left_side_mouse": [54], "nose":[31, 35]}
##
##
##    def coordinates(coordinate, axis):
##
##        if axis == "x": out = [(landmarks.part(i).x, landmarks.part(i).y) for i in coordinate]
##        else: out = [(landmarks.part(i).x, landmarks.part(i).y) for i in coordinate]
##        return out
##
##    dico_points = {}
##
##    for k1, v1 in anatomy_y.items():
##        a = coordinates(v1, "y")
##        dico_points[k1] = a
##
##    for k1, v1 in anatomy_x.items():
##        b = coordinates(v1, "x")
##        dico_points[k1] = b
##
##
##    for k, v in dico_points.items():
##        for i in v:
##            cv2.circle(img, (i[0], i[1]), 1, (0, 255, 0), 1)














##    numpy_horizontal_concat3 = np.concatenate( (e[0], e[1]), axis=1 )
##    numpy_horizontal_concat3 = np.concatenate( (numpy_horizontal_concat3, e[2]), axis=1 )
##    numpy_horizontal_concat3 = np.concatenate( (numpy_horizontal_concat3, e[3]), axis=1 )
##    numpy_horizontal_concat3 = np.concatenate( (numpy_horizontal_concat3, e[4]), axis=1 )
##    numpy_horizontal_concat3 = np.concatenate( (numpy_horizontal_concat3, e[5]), axis=1 )
##
##    numpy_horizontal_concat4 = np.concatenate( (e[7], e[9]), axis=1 )
##    numpy_horizontal_concat4 = np.concatenate( (numpy_horizontal_concat4,  e[8]), axis=1 )
##    numpy_horizontal_concat4 = np.concatenate( (numpy_horizontal_concat4, e[10]), axis=1 )
##    numpy_horizontal_concat4 = np.concatenate( (numpy_horizontal_concat4, e[6]), axis=1 )
##    numpy_horizontal_concat4 = np.concatenate( (numpy_horizontal_concat4, e[11]), axis=1 )
##
##    numpy_vertical11 = np.vstack( (numpy_horizontal_concat3, numpy_horizontal_concat4) )
##
