import math
from scipy.spatial import distance as dist


#============================================
"""RECUPERATE ANGLES"""
#============================================

def collect_angulus(points):
    """We have 2 pairs of coordinates (x1, y1) (x2, y2)
    So we use arctan of rectangle triangle
    for have angulus of orientation formula's:
    angulus = tan ^ -1(opposite side / adjacent) in radians"""

    angulus = []
    for (pts1, pts2) in points:

        x1, y1 = pts1
        x2, y2 = pts2

        #can't divide by 0
        if (x1 - x2) != 0:
            side = (y2 - y1) / (x2 - x1)
            angulus.append(math.atan(side))

        #90 degres only y != 0
        elif (y1 - y2) != 0 and (x1 - x2) == 0 and\
             (y1 - y2) > 0:
            angulus.append(1)

        elif (y1 - y2) != 0 and (x1 - x2) == 0 and\
             (y1 - y2) < 0:
            angulus.append(-1)
    
        elif (y1 - y2) == 0 and (x1 - x2) != 0 and\
             (x1 - x2) > 0:
            angulus.append(1)

        elif (y1 - y2) == 0 and (x1 - x2) != 0 and\
             (x1 - x2) < 0:
            angulus.append(-1)


        #None points as (0, 0) or divide by 0
        else:
            angulus.append(None)

    return angulus

"""FINGER PART"""

def angulus_beetween_points(points1, points2):
    angulus = []

    for pts1, pts2 in zip(points1, points2):
        x1, y1 = pts1
        x2, y2 = pts2

        #can't divide by 0
        if (x1 - x2) != 0:
            side = (y2 - y1) / (x2 - x1)
            angulus.append(math.atan(side))

        #90 degres only y != 0
        elif (y1 - y2) != 0 and (x1 - x2) == 0 and\
             (y1 - y2) > 0:
            angulus.append(1)

        elif (y1 - y2) != 0 and (x1 - x2) == 0 and\
             (y1 - y2) < 0:
            angulus.append(-1)
    
        elif (y1 - y2) == 0 and (x1 - x2) != 0 and\
             (x1 - x2) > 0:
            angulus.append(1)

        elif (y1 - y2) == 0 and (x1 - x2) != 0 and\
             (x1 - x2) < 0:
            angulus.append(-1)


        #None points as (0, 0) or divide by 0
        else:
            angulus.append(None)

    return angulus



#============================================
"""RECUPERATE DISTANCE"""
#============================================

def collect_distances(points):
    """Collect Euclidean distance from each point.
    formula's :
    a = (x2 - x1) ** 2
    b = (y2 - y1) ** 2
    dist = sqrt(a + b)
    """

    distances = []

    for (pts1, pts2) in points:

        eucli = dist.euclidean((pts1), (pts2))

        if eucli == 0:
            distances.append(None)
        else:
            distances.append(eucli)

    return distances


def make_scale(ratio):
    """We need a scale for obtient same distance
    our scale is the area of the contour of the hand
    from: Length*Width in pixel"""
    return ratio[2] * ratio[3]



def normalize(scale1, scale2, dist1):

    if scale1 > scale2:
        dist1 = dist1 / (scale1/scale2)
    else:
        dist1 = dist1 * (scale2/scale1)

    return dist1


""" FINGER PART """

def distance_beetween_points(points1, points2):

    liste = []
    for pts1, pts2 in zip(points1, points2):
        eucli = dist.euclidean((pts1), (pts2))
        liste.append(eucli)

    return liste


#============================================
"""RECUPERATE FEATURE FROM PASSATION"""
#============================================

def passation_informations(points, scale):
    """Recuperate angulus, distance of each pairs
    and the scale of our picture"""

    #Angulus
    angulus = collect_angulus(points)

    #Distance
    distances = collect_distances(points)

    #Scale
    scale = make_scale(scale)

    return angulus, distances, scale


#============================================
"""RECUPERATE FEATURE FROM DATA CSV"""
#============================================
#Recuperate data informations from csv
from csv_treatment import recuperate_data_in_csv

def data_informations():
    """Our csv area compose as:
    label, pairs, points of rectangle."""
    
    scale_list = []
    angulus_list = []
    distance_list = []
    
    data_csv = recuperate_data_in_csv()

    for nb, data in enumerate(data_csv):

        pts_data, scale_data = data[0], data[1]

        #Scale (points of rectangle)
        scale_data = make_scale(scale_data)
        scale_list.append(scale_data)

        #Distance (Make euclidean distance)
        distances_data = collect_distances(pts_data)
        distance_list.append(distances_data)

        #Angulus (Recuperate arctan)
        anglulus_data = collect_angulus(pts_data)
        angulus_list.append(anglulus_data)


    return distance_list, angulus_list, scale_list, data_csv



