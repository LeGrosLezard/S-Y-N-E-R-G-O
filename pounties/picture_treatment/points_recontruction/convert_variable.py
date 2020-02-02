"""Here we switch our variable for example we pass
list to dictionnary annoted by finger name
or dictionnary to list or tuple to list ..."""


#============================================
"""FORMAT LIST - TUPLE
   FORMAT LIST - DICTIONNARY
"""
#============================================

def tuple_to_list(points):
    """We can modified points.
    Like ((0, 0), (0,0) to [[0, 0], [0, 0]]"""
    return [list(i) for i in points]


def list_to_tuple(points):
    """We can return to initial form.
     Like [[0, 0], [0, 0]] to ((0, 0), (0,0))"""
    return [tuple(i) for i in points]

def dictionnary_tuple_to_list(points):

    dico_list = {"t" : [],  "i" : [], "m" : [], "an" : [],
                 "a" : []}

    for k, v in points.items():
        for i in v:
            dico_list[k].append(list(i))

    return dico_list

def list_to_dict(points):
    """Transform tuple to list to dictionnary.
    We can modified points.
    Like ((0, 0), (0,0)) -> t: [[0, 0], [0, 0]]"""

    points_treat = [list(i) for i in points]

    return {"t" : points_treat[0:4],  "i" : points_treat[5:8],
            "m" : points_treat[9:12], "an" : points_treat[13:16],
            "a" : points_treat[17:20]}


def element_to_dict(points):
    """Element already in element list form, so modifiable
    annotated them by finger name.
    Like [[0, 0], [0, 0]] -> t: [[0, 0], [0, 0]]"""

    return {"t" : points[0:4],  "i" : points[5:8],
            "m" : points[9:12], "an" : points[13:16],
            "a" : points[17:20]}



def dict_to_list(points):
    """Transform variable dictionnary to list
    so initial form.
    Like {t: [[0, 0], [0, 0]], i: [[0, 0], [0, 0]]}
    -> [((0, 0), (0,0)), ((0, 0), (0,0))]"""
    liste = []
    for k, v in points.items():
        for i in v:
            try:
                liste.append(tuple(i))
            except:
                pass
    return liste
