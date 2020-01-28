from utils_reconstruction import *
from test21 import *

points_current = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
ratio_current = (31, 31, 113, 109)

ratio_current = make_ratio(ratio_current)
distance = collect_distances(points_current, "", "", "current")
to_search = what_we_need_to_search(distance)
print(to_search)






data_csv = recuperate_data_in_csv(1)

for data in data_csv:

    points_data, ratio_data = data[0], data[1]

    #collect normalize distances
    ratio_data = make_ratio(ratio_data)
    norm, which = normalisation(ratio_data, ratio_current)
    distance_data = collect_distances(points_data, which, norm, "data")

    #collect angles
    abscisse = collect_abscisse(points_data)
    angle_data = points_to_angle(abscisse)

