
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
