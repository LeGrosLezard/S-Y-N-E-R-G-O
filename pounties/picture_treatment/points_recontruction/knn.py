
import cv2
import math
import importlib
import numpy as np
from convert_variable import *
from scipy.spatial import distance as dist


#==============================
"""RECUPERATE CLOSED POINTS"""
#==============================

def a(index_pair, distance_list, angulus_list, finger_name):

    list1 = []
    list2 = []

    for nb, (distance, angulus) in enumerate(zip(distance_list, angulus_list)):

        distance = element_to_dict(distance)
        distance = distance[finger_name]

        angulus = element_to_dict(angulus)
        angulus = angulus[finger_name]

        list_w = [distance[ind] for ind in index_pair]
        list_w1 = [angulus[ind] for ind in index_pair]

        list1.append((list_w, nb))
        list2.append((list_w1, nb))

    return list1, list2


def b(key, index, distances, angulus):

    l = [distances[key][ind] for ind in index]
    m = [angulus[key][ind] for ind in index]

    return l, m


def c(i, j, l, m, k, n, ind):

    list_w = []
    list_w1 = []

    for ii, jj, kk, ll in zip(i[0], j[0], l, m):

        if ii != None and jj != None:

            if k[ind] > n:   ii = ii / (k[ind]/n)
            else:       ll = ll / (n/k[ind])

            list_w.append(((kk - ii) ** 2, ind))
            list_w1.append(((ll - jj) ** 2, ind))

    return list_w, list_w1


def d(list3, list4, list_w, list_w1, ind):
    
    ok1 = sum([i[0] for i in list_w])
    ok2 = sum([i[0] for i in list_w1])
 
    form1 = math.sqrt(ok1)
    list3.append((form1, ind))

    form2 = math.sqrt(ok2)
    list4.append((form2, ind))

    return list3, list4


def z(list3, list4):

    list3 = sorted(list3, key=lambda x: x[0])
    list4 = sorted(list4, key=lambda x: x[0])

    ind1 = list3[0][1]
    ind2 = list4[0][1]

    dist1 = list3[0][0]
    dist2 = list4[0][0]
    print(dist1, dist2)

    return ind1, ind2

    
def dddddddd(distance_list, angulus_list, scale_list, value, angulus, distances, scale, key):

    #Recuperate points of fingers if not (0, 0)
    none = ((0, 0), (0, 0))
    index_pair = [nb for nb, i in enumerate(value) if i != none]


    list1, list2 = a(index_pair, distance_list, angulus_list, key)
    l, m = b(key, index_pair, distances, angulus)

    list3 = []
    list4 = []

    for i, j in zip(list1, list2):

        ind = i[1]

        list_w, list_w1 = c(i, j, l, m, scale_list, scale, ind)

        if len(index_pair) == len(list_w):

            ind = list_w[0][1]

            list3, list4 = d(list3, list4, list_w, list_w1, ind)

    ind1, ind2 = z(list3, list4)

    return ind1, ind2


