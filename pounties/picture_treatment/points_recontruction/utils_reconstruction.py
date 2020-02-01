import os
import ast
import csv
import cv2
import math
import importlib
import numpy as np
import auto_write_thread
from scipy.spatial import distance as dist


#============================================
"""RECUPERATE ANGLES"""
#============================================

def collect_angulus(points):
    
    angulus = []
    for (pts1, pts2) in points:

        x1, y1 = pts1
        x2, y2 = pts2

        if (x1 - x2) != 0:
            side = (y2 - y1) / (x2 - x1)
            angulus.append(math.atan(side))

        else:
            angulus.append(None)

    return angulus




#============================================
"""RECUPERATE DISTANCE"""
#============================================


def collect_distances(points):
    """Collect Euclidean distance from each point.
    Repartite to finger's"""

    distances = []


    for (pts1, pts2) in points:

        eucli = dist.euclidean((pts1), (pts2))

        if eucli == 0:
            distances.append(None)
        else:
            distances.append(eucli)

    return distances



def make_scale(ratio):
    return ratio[2] * ratio[3]


def normalise(scale_data, scale_passation, dist_data, dist_passation):


    if scale_data > scale_passation:
        dist_data = dist_data / (scale_data / scale_passation)

    elif scale_passation > scale_data:
        dist_passation = dist_passation / (scale_passation / scale_data)  

    return (dist_passation, dist_data)



#============================================
"""FORMAT LIST - TUPLE
   FORMAT LIST - DICTIONNARY
"""
#============================================

def tuple_to_list(points):
    return [list(i) for i in points]


def list_to_tuple(points):
    return [tuple(i) for i in points]


def list_to_dict(points):

    points_treat = [list(i) for i in points]

    return {"t" : points_treat[0:4],  "i" : points_treat[5:8],
            "m" : points_treat[9:12], "an" : points_treat[13:16],
            "a" : points_treat[17:20]}


def element_to_dict(points):

    return {"t" : points[0:4],  "i" : points[5:8],
            "m" : points[9:12], "an" : points[13:16],
            "a" : points[17:20]}

def dict_to_list(points):
    liste = []
    for k, v in points.items():
        for i in v:
            try:
                liste.append(tuple(i))
            except:
                pass
    return liste






#==============================
"""CSV TREATMENT"""
#==============================

PATH_FOLDER_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"
PATH = PATH_FOLDER_CSV + "/{}.csv"

def recuperate_data_in_csv():
    """From csv we recuperate points data"""

    global PATH_FOLDER_CSV


    #number csv in folder
    csv_list = os.listdir(PATH_FOLDER_CSV)
    number_csv = len(csv_list)

    data_list = []

    for file in range(1, number_csv):

        with open(PATH.format(file), newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for information in reader:
                points = ast.literal_eval(information["points"])
                ratio =  ast.literal_eval(information["ratio"])
                label =  ast.literal_eval(information["label"])

                data_list.append((points, ratio, label))


    return data_list




def delete_points(points):
    to_delete = []
    for k, v in points.items():
        c = 0
        for i in v:
            if i == ((0, 0), (0, 0)):
                c += 1

        if c == len(v):
            to_delete.append(k)

        elif c == 0:
            to_delete.append(k)
            
    for i in to_delete:
        del points[i]

    return points



#1 phax
def a(distance_list, angulus_list, scale_list, key, index, angulus, distances, scale):
    list1 = []
    list2 = []


    for nb, (i, j) in enumerate(zip(distance_list, angulus_list)):
        i = element_to_dict(i)
        j = element_to_dict(j)
        k = scale_list[nb]

        i = i[key][index]
        j = j[key][index]

        if i != None and j != None:

            list1.append([i, nb])
            list2.append([j, nb])


    l = distances[key][index]
    m = angulus[key][index]
    n = scale

    list3 = []
    for i, j in zip(list1, list2):

        if k > n:   i = [i[0] / (k/n), i[1]]
        else:       l = l / (n/k)

        #print(l, i[0], m, j[0])

        un = (l - i[0]) ** 2
        deux = (m - j[0]) ** 2

        form = math.sqrt(un + deux)
        list3.append((form, i[1]))


    list3 = sorted(list3, key=lambda x: x[0])
    print(list3[0])



 
#better ang, dist
def b(distance_list, angulus_list, scale_list, key, index, angulus, distances, scale):

    list1 = []
    list2 = []


    for nb, (i, j) in enumerate(zip(distance_list, angulus_list)):
        i = element_to_dict(i)
        j = element_to_dict(j)
        k = scale_list[nb]

        i = i[key][index]
        j = j[key][index]

        if i != None and j != None:

            list1.append((i, nb))
            list2.append((j, nb))


    l = distances[key][index]
    m = angulus[key][index]
    n = scale




    for i, j in zip(list1, list2):

        if k > n:   i = [i[0] / (k/n), i[1]]
        else:       l = l / (n/k)













#all other points
def c(distance_list, angulus_list, scale_list, value, angulus, distances, scale):

    index = [nb for nb, i in enumerate(value) if i != ((0, 0), (0, 0))]
    #print(index)


    for nb, (i, j) in enumerate(zip(distance_list, angulus_list)):

        i = element_to_dict(i)
        j = element_to_dict(j)
        k = scale_list[nb]

        
































