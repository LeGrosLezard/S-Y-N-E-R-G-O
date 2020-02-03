#==============================
"""INDENTIFY POINTS OF PHAXS"""
#==============================
def identify_phaxs_points(points):
    """We need to identify points presents or not
    if one point's is egal to ((0, 0), (0, 0))
    don't recuperate index into the list.

    form is like a dictionnary:
    t : {((1, 1),(1, 1)), ((2, 2), (2, 2)), ((0, 0), (0, 0))}
    we recupera index 0 and 1, index 2 is none point.
    In case there are no points into the finger or all points
    into the finger don't
    search it in this part.
    """

    to_delete = []  #Phax to delete from points.
    finger = []
    for k, v in points.items():

        c = 0 #None points

        for i in v: #None points += 1
            if i == ((0, 0), (0, 0)):
                c += 1

        if c == len(v): #All points is None so we have no points
            finger.append(k)
            to_delete.append(k)

        elif c == 0: #One points is None
            to_delete.append(k)

    """This dictionnary is phax missing to search"""
    phax = {"t" : [],  "i" : [],  "m" :[], "an" : [], "a" : []}

    for k, v in points.items():
        nan = False

        for i in to_delete: #No points into the finger
            if k == i:
                nan = True

        if nan is False: #There are max one none
            phax[k] = v

    return phax, finger






#==============================
"""SEARCHING POINTS OF PHAXS"""
#==============================



def indentify_finger_points(finger):

    liste_index = ["t", "i", "m", "an", "a"]

    to_search = []

    for name in finger:

        if name is "t":
            searching = liste_index[1]
            to_search.append(searching)

        elif name is "a":
            searching = liste_index[-2]
            to_search.append(searching)

        elif name not in ("t", "a"):
            searching = liste_index.index(name)
            searching = [liste_index[searching - 1], liste_index[searching + 1]]
            to_search.append(searching)


    return to_search










