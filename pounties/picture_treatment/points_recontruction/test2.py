from utils_reconstruction import *


points = [((0, 0), (0, 0)), ((97, 105), (115, 94)), ((115, 94), (122, 79)), ((122, 79), (126, 69)), ((0, 0), (0, 0)), ((86, 76), (83, 55)), ((83, 55), (83, 47)), ((83, 47), (83, 40)), ((0, 0), (0, 0)), ((75, 79), (68, 55)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((0, 0), (0, 0)), ((51, 98), (44, 91)), ((44, 91), (40, 94)), ((40, 94), (41, 90))]
ratio = (31, 31, 113, 109)

data_csv = recuperate_data_in_csv(1)

dico1, echelle = collect_distances(points, ratio)
print(dico1)


print("")

for nb, i in enumerate(data_csv):

    sum_pts = []
    dico, echelle = collect_distances(i[0], i[1])
    a = dico["t"][0]
    b = dico1["t"][1]
    print(abs(a - b), nb)
    print("")


blank_image = np.zeros((500, 500, 3), np.uint8)
for i in data_csv[0][0]:
    for j in i:
        cv2.circle(blank_image, (j[0], j[1]) , 2, (0, 0, 255), 2)
        cv2.line(blank_image, (i[0]), (i[1]), (0, 255, 0), 2)
        cv2.imshow("blanck", blank_image)
        cv2.waitKey(0)


blank_imagea = np.zeros((500, 500, 3), np.uint8)
for i in points:
    for j in i:
        cv2.circle(blank_imagea, (j[0], j[1]) , 2, (0, 0, 255), 2)
        cv2.line(blank_imagea, (i[0]), (i[1]), (0, 255, 0), 2)
        cv2.imshow("blank_imagea", blank_imagea)
        cv2.waitKey(0)














