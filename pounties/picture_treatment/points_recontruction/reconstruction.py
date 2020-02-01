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





#all other points better ang, better dist
def d(distance_list, angulus_list, scale_list, value, angulus, distances, scale, key):


    index = [nb for nb, i in enumerate(value) if i != ((0, 0), (0, 0))]
    print(index, key)

    list1 = []
    list2 = []

    for nb, (i, j) in enumerate(zip(distance_list, angulus_list)):

        i = element_to_dict(i)
        j = element_to_dict(j)

        i = i[key]
        j = j[key]

 
        list_w = [i[ind] for ind in index]
        list_w1 = [j[ind] for ind in index]

        list1.append((list_w, nb))
        list2.append((list_w1, nb))


    
    l = [distances[key][ind] for ind in index]
    m = [angulus[key][ind] for ind in index]
    n = scale

    list3 = []
    list4 = []
    k = scale_list
    for i, j in zip(list1, list2):

        ind = i[1]

        list_w = []
        list_w1 = []
        for ii, jj, kk, ll in zip(i[0], j[0], l, m):

            if ii != None and jj != None:

                if k[ind] > n:   ii = ii / (k[ind]/n)
                else:       ll = ll / (n/k[ind])

                list_w.append(((kk - ii) ** 2, ind))
                list_w1.append(((ll - jj) ** 2, ind))

        if len(index) == len(list_w):

            ind = list_w[0][1]

            ok1 = sum([i[0] for i in list_w])
            ok2 = sum([i[0] for i in list_w1])
 

            form1 = math.sqrt(ok1)
            list3.append((form1, ind))

            form2 = math.sqrt(ok2)
            list4.append((form2, ind))



    list3 = sorted(list3, key=lambda x: x[0])


    list4 = sorted(list4, key=lambda x: x[0])




    ind1 = list3[0][1]
    ind2 = list4[0][1]

    print(ind1)
    print(ind2)

    print(list1[ind1][0])
    print(list2[ind2][0])



