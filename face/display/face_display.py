from cv2 import bitwise_and, polylines, fillConvexPoly, imshow, imread, resize, cvtColor, COLOR_BGR2GRAY, line
from numpy import zeros_like, hstack, empty, uint8


#si touché -> c pas dans display

#mettre la zone en bleu
#définir un nom de zone (ex: joue par droite + nombre de frame a la fin)
#l'afficher


def displaying(gray, img, copy, convexhull):

    head_model = imread("display/head_model.jpg")
    head_model = resize(head_model, (int(gray.shape[1]/2), gray.shape[0]))

    mask = zeros_like(gray)

    polylines(copy, [convexhull], True, (0, 0, 255), 1)
    fillConvexPoly(mask, convexhull, 255)

    face = bitwise_and(copy, copy, mask=mask)

    displaying = hstack((head_model, img))
    displaying = hstack((displaying, face))

    imshow('Display', displaying)


def recuperate_face(convexhull, gray, img, points):
    """We displaying the frame, the face
    from the frame"""

    copy = img.copy()

    for pts in points:
        pts1 = pts[0]; pts2 = pts[1]; pts3 = pts[2]

        line(copy, pts1, pts2, (0, 0, 255), 1)
        line(copy, pts2, pts3, (0, 0, 255), 1)
        line(copy, pts1, pts3, (0, 0, 255), 1)

    displaying(gray, img, copy, convexhull)






##def make_rectangle(area, color):
##    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in range(area[0], area[1])])
##    x, y, w, h = boundingRect(area)
##    cv2.rectangle(img, (x, y), (x + w, y + h), color, 1) 
##    return x, y, w, h
##
##def make_contour(area, color):
##    area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in area])
##    cv2.drawContours(img, [area], 0, color, 1)
##
##
##areas =  { "beet_eyes" :[21, 22, 27], "chin":[58, 56, 9, 7], "chin1":[58, 7, 3, 48],
##           "chin2": [56, 54, 13, 9], "cheek1": [48, 3, 0, 28],
##           "cheek2":[54, 13, 16, 28], "noze_area":[27, 48, 54], "mouse":(48, 61),
##           "onEye1":(17, 22), "onEye2":(22, 27), "leftEye":(36, 42), "rightEye":(42, 48)}
##
##[make_contour(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb <= 6]
##[make_rectangle(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb > 6]
##





##def intra_face(img, gray, landmarks, face, fgbg):
##
##    #A CONTINUER
##    import cv2
##    import numpy as np
##
##    subastrac = fgbg.apply(img)
##
##    def crop_rectangle(area, color):
##        area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in range(area[0], area[1])])
##        x, y, w, h = boundingRect(area)
##        #cv2.rectangle(img, (x, y), (x + w, y + h), color, 1)
##        return x - 5, y - 5, w + 5, h + 10
##
##    def crop_contour(area, color):
##        area = np.array([(landmarks.part(n).x, landmarks.part(n).y) for pts in face for n in area])
##        x, y, w, h = boundingRect(area)
##        #cv2.drawContours(img, [area], 0, color, 1)
##        return x , y , w, h
##
##
##    def counter(area):
##        a = cv2.countNonZero(area)
##        #print(a)
##
##
##    areas =  { "beet_eyes" :[21, 22, 27], "chin":[58, 56, 9, 7],
##               "chin1":[58, 7, 3, 48],  "chin2": [56, 54, 13, 9],
##               "cheek1": [48, 3, 0, 28], "cheek2":[54, 13, 16, 28],
##               "noze_area":[27, 48, 54], "mouse":(48, 61),
##               "onEye1":(17, 22), "onEye2":(22, 27),
##               "leftEye":(36, 42), "rightEye":(42, 48) }
##
##
##    b = [crop_contour(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb <= 6]
##    a = [crop_rectangle(areas[k], (0,255,0)) for nb, k in enumerate(areas) if nb > 6]
##    d = [cv2.resize(img[i[1]:i[1] + i[3], i[0]:i[0] + i[2]], (100, 50)) for i in a + b]
##
##    e = [cv2.resize(subastrac[i[1]:i[1] + i[3], i[0]:i[0] + i[2]], (100, 50)) for i in a + b]
##
##
##
##    numpy_horizontal_concat = np.concatenate( (d[0], d[1]), axis=1 )
##    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[2]), axis=1 )
##    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[3]), axis=1 )
##    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[4]), axis=1 )
##    numpy_horizontal_concat = np.concatenate( (numpy_horizontal_concat, d[5]), axis=1 )
##
##    numpy_horizontal_concat2 = np.concatenate( (d[7], d[9]), axis=1 )
##    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2,  d[8]), axis=1 )
##    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2, d[10]), axis=1 )
##    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2, d[6]), axis=1 )
##    numpy_horizontal_concat2 = np.concatenate( (numpy_horizontal_concat2, d[11]), axis=1 )
##
##    numpy_vertical = np.vstack( (numpy_horizontal_concat, numpy_horizontal_concat2) )
##
##
##    counter(e[0])
##
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


##    cv2.imshow("numpy_vertical", numpy_vertical)
##    cv2.imshow("numpy_vertical11", numpy_vertical11)
##    cv2.waitKey(0)


##    images = [Image.fromarray(name) for name in d]
##    somme=[]
##    for img in images:
##        somme+=list((np.asarray(img)))
##
##    cv2.imshow("img", np.array(somme))
##    cv2.waitKey(0)




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

