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
            liste_angle.append(int(angle))


        elif i == (0, 0):
            liste_angle.append(0)


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
#cv2.imshow("blanck", blank_image)



dico_distance_current, echelle_current = collect_distances(points5, ratio5)
direction_current = collect_points(points5)
dico_angle_current = points_to_angle(direction_current)









liste = [(points1, ratio1, "im1"), (points2, ratio2, "im2"),
         (points3, ratio3, "im3"), (points4, ratio4, "im4")]

liste = [(points1, ratio1, "im1")]




def to_search(dico_passation_distance):

    dico = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for k, v in dico.items():
        phax = []

        for nb, i in enumerate(dico_passation_distance[k]):
            if i == 0.0: phax.append(nb)

        if len(phax) == 3:       dico[k].append("finger")
        elif 3 > len(phax) > 0:  dico[k] += [i for i in phax]
        elif len(phax) == 0:     dico[k].append("None")


    return dico



def prox(dico_passation_distance, data_distance, norm):

    dico = {"t" :[], "i" : [], "m" : [], "an" : [], "a" : []}

    for k, v in dico.items():
        liste_working = []
        for i, j in zip(dico_passation_distance[k], data_distance[k]):
            liste_working.append(abs(i - j))

        dico[k] += [i for i in liste_working]

    return dico







#[number] = phax miss
#None = all fingers
#finger = search finger miss
searching_points = to_search(dico_distance_current)
print(searching_points, "\n")

liste_informations_angle = []
liste_informations_distance = []

for i in liste:

    #data treatment
    dico_distance, echelle = collect_distances(i[0], i[1])#---- distance echelle

    pts = collect_points(i[0])#-------------------------------- pts for angle
    angle = points_to_angle(pts)#------------------------------ angle

    norm = determine_ratio(echelle_current, echelle)#---------- norm beetween data and current passation


    #Recup data
    distance = prox(dico_distance_current, dico_distance, norm)
    angle = prox(dico_angle_current, angle, 1)

    liste_informations_distance.append(distance)
    liste_informations_angle.append(angle)



def search_points(to_search_pts, value):                    #pts phax et angle phax

    for i in  to_search_pts:#I = indexage
        if i != None:

            print(value)

            if i == len(value):                             #derniere phax
                print(i - 1)

            elif i not in (0, "None", "finger"):            #phax avec un avant apres
                print(i)
                print(i + 1)
                print(i - 1)

            elif i == 0:                                    #premiere phax
                print(i + 1)

        print("")




def finger_to_search(to_search_pts, value, dico, k):

    for i in  to_search_pts:
        if i != None:

            if i == "finger":
                fings = ["t", "i", "m", "an", "a"]

                avant_doigt = fings.index(k) - 1
                apres_doigt = fings.index(k) + 1

                print(fings[avant_doigt], fings[apres_doigt])
                print(dico[fings[avant_doigt]])
                print(dico[fings[apres_doigt]])




"""
en gros on a fait les diff entre chauqe pts
"""






for i in liste_informations_distance:           #phax la plus proche
    for k, v in i.items():
        search_points(searching_points[k], v)

    print("")



for i in liste_informations_distance:           #doigt qui ressemble le pluss
    for k, v in i.items():
        finger_to_search(searching_points[k], v, i, k)

    print("")

    

for i in liste_informations_angle:              #angle le plus proche
    for k, v in i.items():
        search_points(searching_points[k], v)

    print("")














