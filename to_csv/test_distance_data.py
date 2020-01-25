import numpy as np
import cv2
import math
from scipy.spatial import distance as dist

def drawing_circle(blank_image, points, a, b, color):
    [cv2.circle(blank_image, (j[0] + a, j[1] + b) , 2, color, 2) for i in points for j in i]


def collect_distances(points, ratio):

    distances = []
    for nb in range(len(points)):
  
        distance = dist.euclidean(points[nb][0], points[nb][1])
        distances.append(distance)

    dico = {"t" :distances[0:4], "i" : distances[5:8], "m" : distances[9:12], "an" : distances[13:16],
            "a" : distances[17:20]}

    return dico, ratio[2] * ratio[3]


def collect_points(points):

    abscisse = []
    for nb in range(len(points)):
        ptsX = points[nb][1][0] - points[nb][0][0]
        ptsY = - (points[nb][1][1] - points[nb][0][1])

        abscisse.append((ptsX, ptsY))

    return abscisse



def points_to_angle(abscisse):

    liste_angle = []

    for i in abscisse:

        if i[1] == 0 and i[0] != 0:
            if i[0] > 0:
                liste_angle.append(0)
            elif i[0] < 0:
                liste_angle.append(180)

        elif i[0] == 0 and i[1] != 0:
            if i[1] > 0:
                liste_angle.append(90)
            elif i[1] < 0:
                liste_angle.append(-90)

        elif i != (0, 0):

            tan = math.atan(i[1] / i[0])
            angle = math.degrees(tan)
            if angle < 0: angle += 180
            liste_angle.append(angle)


        elif i == (0, 0):
            liste_angle.append(None)


    dico_angle = {"t" :liste_angle[0:4], "i" : liste_angle[5:8], "m" : liste_angle[9:12], "an" : liste_angle[13:16],
                  "a" : liste_angle[17:20]}

    return dico_angle



def determine_ratio(im1, im2):
    if im1 > im2: norm = im1 / im2
    else: norm = im2 / im1
    return norm







image1 = 1
points1 = [((88, 103), (102, 97)), ((102, 97), (113, 89)), ((113, 89), (123, 79)), ((123, 79), (131, 68)), ((88, 103), (85, 72)), ((85, 72), (81, 57)), ((81, 57), (78, 50)), ((78, 50), (75, 44)), ((88, 103), (74, 79)), ((74, 79), (61, 65)), ((61, 65), (54, 64)), ((54, 64), (47, 62)), ((88, 103), (64, 89)), ((64, 89), (57, 82)), ((57, 82), (50, 75)), ((50, 75), (46, 71)), ((88, 103), (61, 104)), ((61, 104), (50, 100)), ((50, 100), (43, 96)), ((43, 96), (36, 93))]
ratio1 = (31, 31, 114, 98)

image2 = 2
points2 = [((87, 109), (69, 109)), ((69, 109), (54, 98)), ((54, 98), (42, 91)), ((42, 91), (35, 84)), ((87, 109), (102, 109)), ((102, 109), (121, 109)), ((121, 109), (132, 113)), ((132, 113), (143, 116)), ((87, 109), (98, 94)), ((98, 94), (117, 83)), ((117, 83), (128, 79)), ((128, 79), (140, 69)), ((87, 109), (90, 87)), ((90, 87), (106, 69)), ((106, 69), (117, 61)), ((117, 61), (128, 50)), ((87, 109), (79, 79)), ((79, 79), (87, 61)), ((87, 61), (91, 53)), ((91, 53), (98, 46))]
ratio2 = (21, 36, 132, 108)

image3 = 3
points3 = [((105, 94), (106, 77)), ((106, 77), (112, 61)), ((112, 61), (112, 38)), ((112, 38), (116, 25)), ((105, 94), (73, 100)), ((73, 100), (57, 87)), ((57, 87), (47, 81)), ((47, 81), (37, 74)), ((105, 94), (83, 90)), ((83, 90), (60, 74)), ((60, 74), (50, 64)), ((50, 64), (37, 54)), ((105, 94), (86, 77)), ((86, 77), (67, 64)), ((67, 64), (57, 54)), ((57, 54), (47, 48)), ((105, 94), (90, 67)), ((90, 67), (76, 54)), ((76, 54), (67, 47)), ((67, 47), (57, 41))]
ratio3 = (31, 15, 98, 105)

image4 = 4
points4 = [((86, 105), (100, 101)), ((100, 101), (115, 91)), ((115, 91), (122, 80)), ((122, 80), (126, 69)), ((86, 105), (86, 76)), ((86, 76), (83, 54)), ((83, 54), (83, 47)), ((83, 47), (83, 40)), ((86, 105), (72, 80)), ((72, 80), (65, 65)), ((65, 65), (65, 59)), ((65, 59), (69, 58)), ((86, 105), (65, 94)), ((65, 94), (51, 77)), ((51, 77), (51, 73)), ((51, 73), (51, 66)), ((86, 105), (61, 108)), ((61, 108), (44, 97)), ((44, 97), (40, 94)), ((40, 94), (41, 90))]
ratio4 = (31, 31, 114, 111)

image5 = "a"
points5 = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
ratio5 = (31, 31, 113, 109)


blank_image = np.zeros((500, 500, 3), np.uint8)
drawing_circle(blank_image, points1, 0, 350, (255, 0, 0))
drawing_circle(blank_image, points2, 200, 200, (255, 0, 0))
drawing_circle(blank_image, points3, 0, 200, (255, 0, 0))
drawing_circle(blank_image, points4, 0, 0, (255, 0, 0))
drawing_circle(blank_image, points5, 200, 0, (0, 255, 0))
cv2.imshow("blanck", blank_image)



dico_current, echelle_current = collect_distances(points5, ratio5)
direction_current = collect_points(points5)
dico_angle_current = points_to_angle(direction_current)



for k, v in dico_current.items():
    print(k, v)

print("")

for k, v in dico_angle_current.items():
    print(k, v)

for i in range(6):
    print("")






liste = [(points1, ratio1, "im1"), (points2, ratio2, "im2"),
         (points3, ratio3, "im3"), (points4, ratio4, "im4")]

liste = [(points1, ratio1, "im1")]






def compareason(dico_passation1, dico_passation2, dico_data1, dico_data2, norm):

    fingers = ["t", "i", "m", "an", "a"]

    for fing in fingers:

        print(fing)


        liste_distance = []


        print("distance")

        print("data : ", dico_data1[fing])                  #distance
        print("current :", dico_passation1[fing])

        for i, j in zip(dico_data1[fing], dico_passation1[fing]):

            if i == None:
                liste_angle.append("to search")
            elif j == None:
                liste_angle.append("to search")
            else:
                liste_distance.append(abs(i - j))


        moyenne = [i for i in liste_distance if type(i) != str]
        if moyenne == []: moyenne = ["to search"]
        else: moyenne = sum(moyenne)
        print("result : ", liste_distance, "\nso", moyenne)



        liste_angle = []

        print("\nangle")

        print("data : ", dico_data2[fing])                 #angle
        print("current :", dico_passation2[fing])

        for i, j in zip(dico_data2[fing], dico_passation2[fing]):
            if i == None:
                liste_angle.append("to search")
            elif j == None:
                liste_angle.append("to search")
            else:
                liste_angle.append(abs(i - j))

        moyenne = [i for i in liste_angle if type(i) != str]
        if moyenne == []:  moyenne = ["to search"]
        else: moyenne = sum(moyenne)
        print("result : ", liste_angle, "\nso", moyenne)

        print("")

















for i in liste:
    print(i[2])
    print("")

    dico, echelle = collect_distances(i[0], i[1])
    pts = collect_points(i[0])
    angle = points_to_angle(pts)


    norm = determine_ratio(echelle_current, echelle)

    compareason(dico_current, dico_angle_current, dico, angle, norm)



    print("")
    print("")


















##dico, echelle2 = collect_distances(points1, ratio1)
##for k, v in dico.items():
##    print(k, v)
##print("")
##
##
##dico, echelle3 = collect_distances(points2, ratio2)
##for k, v in dico.items():
##    print(k, v)
##print("")
##
##
##dico, echelle4 = collect_distances(points3, ratio3)
##for k, v in dico.items():
##    print(k, v)
##print("")














