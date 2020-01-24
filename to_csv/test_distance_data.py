import numpy as np
import cv2
import math
from scipy.spatial import distance as dist


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

for i in points1:
    for j in i:
        cv2.circle(blank_image, (j[0], j[1] + 350) , 2, (0, 0, 255), 2)

for i in points2:
    for j in i:
        cv2.circle(blank_image, (j[0] + 200, j[1] + 200) , 2, (0, 0, 255), 2)

for i in points3:
    for j in i:
        cv2.circle(blank_image, (j[0], j[1] + 200) , 2, (0, 0, 255), 2)

for i in points4:
    for j in i:
        cv2.circle(blank_image, j, 2, (0, 0, 255), 2)

for i in points5:
    for j in i:
        cv2.circle(blank_image, (j[0] + 200, j[1]) , 2, (0, 0, 255), 2)



#cv2.imshow("blanck", blank_image)


print("")



def pts(points):

    x = []
    y = []
    distance_liste = []


    for i in points:
        for nb in range(len(i)):
            if nb < len(i) - 1:

                #cv2.line(blank_image, (i[nb]), (i[nb + 1]), (255, 255, 255), 2)

                distance = dist.euclidean(i[nb], i[nb + 1])

                distance_liste.append(distance)
                x.append(i[nb][0] - i[nb + 1][0])
                y.append(i[nb][1] - i[nb + 1][1])


    px = x[0:4]
    ix = x[5:8]
    mx = x[9:12]
    anx = x[13:16]
    ax = x[17:20]
    a = [px, ix, mx, anx, ax]




    py = y[0:4]
    iy = y[5:8]
    my = y[9:12]
    any = y[13:16]
    ay = y[17:20]


    distance_listep = distance_liste[0:4]
    distance_listei = distance_liste[5:8]
    distance_listem = distance_liste[9:12]
    distance_listean = distance_liste[13:16]
    distance_listea = distance_liste[17:20]


    return a


#
liste = [points1, points2, points3, points4]
yox = []
for nb, i in enumerate(liste):
    x = pts(i)
    yox.append(x)
#














x1 = []
y1 = []
distance_liste1 = []

for i in points5:
    for nb in range(len(i)):
        if nb < len(i) - 1:

            distance = dist.euclidean(i[nb], i[nb + 1])

            distance_liste1.append(distance)
            x1.append(i[nb][0] - i[nb + 1][0])
            y1.append(i[nb][1] - i[nb + 1][1])


for i in range(5):
    print("")


px1 = x1[0:4]
ix1 = x1[5:8]
mx1 = x1[9:12]
anx1 = x1[13:16]
ax1 = x1[17:20]

a1 = [px1, ix1, mx1, anx1, ax1]

py1 = y1[0:4]
iy1 = y1[5:8]
my1 = y1[9:12]
any1 = y1[13:16]
ay1 = y1[17:20]


distance_listep1 = distance_liste1[0:4]
distance_listei1 = distance_liste1[5:8]
distance_listem1 = distance_liste1[9:12]
distance_listean1 = distance_liste1[13:16]
distance_listea1 = distance_liste1[17:20]




print("")



for i in yox:
    retouchingX = []
    for nb, j in enumerate(i):

        print(j, "............", a1[nb])




        E = 0
        xxx = []
        for k, l in zip(j, a1[nb]):
            print(k, l, "******", abs(k-l))
            E += abs(k-l)


        retouchingX.append(E)
        print("somme", E)
        



    print(retouchingX)
    print("si points manquant peut etre faire le : ", retouchingX.index(min(retouchingX)))
    print("")
    print("")
    print("")
    print("")






















