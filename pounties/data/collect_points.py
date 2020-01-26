import csv


data = [((82, 103), (99, 97)), ((99, 97), (113, 89)), ((113, 89), (123, 79)), ((123, 79), (130, 68)), ((82, 103), (85, 72)), ((85, 72), (78, 57)), ((78, 57), (78, 50)), ((78, 50), (75, 44)), ((82, 103), (74, 79)), ((74, 79), (61, 68)), ((61, 68), (53, 65)), ((53, 65), (46, 62)), ((82, 103), (64, 90)), ((64, 90), (57, 82)), ((57, 82), (50, 75)), ((50, 75), (46, 72)), ((82, 103), (61, 104)), ((61, 104), (50, 100)), ((50, 100), (43, 96)), ((43, 96), (36, 93))]


LISTE_HEADER = ["image", "points", "ratio"]


def header_csv(name_csv):                                           #Write header
                                                                    #New csv
    global LISTE_HEADER
    with open(name_csv, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LISTE_HEADER)
        writer.writeheader()



def writting_data(name_csv, image, points, ratio):                  #Add into csv

    global LISTE_HEADER
    
    dico_data = {"image":image, "points":points, "ratio":ratio}
  
    with open(name_csv, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=LISTE_HEADER)
        writer.writerow(dico_data)






if __name__ == "__main__":

    image = "1"
    points = data
    ratio = (5, 10 ,15)

    header_csv("yo.csv")
    writting_data("yo.csv", image, points, ratio)
