

import math
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
