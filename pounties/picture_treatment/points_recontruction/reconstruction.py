from ok1 import *


def current_points(points, ratio):

    #ratio
    ratio = make_ratio(ratio)

    #distance
    distance = collect_distances(points, "", "", "current")

    #angle
    abscisse = collect_abscisse(points)
    angle = points_to_angle(abscisse)

    informations = (distance, angle, ratio)

    return informations


def points_to_search(distance, points):

    none_points = what_we_need_to_search(distance)

    fingers_points = points_to_fingers_dict(points)

    search_points = so_we_search(none_points, fingers_points)

    for k, v in fingers_points.items():
        print("finger ", k.upper(), v)

    print("")
    print(none_points)
    print(search_points, "\n\n\n\n")


    return search_points, fingers_points
























































if __name__ == "__main__":
    points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
    ratio = (31, 31, 113, 109)


    informations_current_point = current_points(points, ratio)
    distance1, angle1, ratio1 = informations_current_point
    print(distance1, angle1, ratio1)

    points_to_search(distance1, points)




















