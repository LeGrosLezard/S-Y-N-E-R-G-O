#==============================
"""SEARCHING POINTS"""
#==============================
def searching_points(points):

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

    new = {"t" : [],  "i" : [],  "m" :[], "an" : [], "a" : []}

    for k, v in points.items():
        nan = False

        for i in to_delete:
            if k == i:
                nan = True

        if nan is False:
            new[k] = v

    return new
