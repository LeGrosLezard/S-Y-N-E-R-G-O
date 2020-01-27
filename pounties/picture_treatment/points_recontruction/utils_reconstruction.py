import os
import csv
import cv2
import importlib
import auto_write_thread

PATH_FOLDER_CSV = r"C:\Users\jeanbaptiste\Desktop\pounties\data\csv"


def csv_files():

    global PATH_FOLDER_CSV
    liste_csv = os.listdir(PATH_FOLDER_CSV)
    number_csv = len(liste_csv)

    return number_csv

def recuperate_data_in_csv(csv_name):

    path = PATH_FOLDER_CSV + "/" + str(csv_name) + ".csv"

    liste_data = []

    with open(path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for i in reader:
            liste_data.append((i["points"], i["ratio"], i["label"]))

    return liste_data


def to_thread(number):

    with open('auto_write_thread.py', 'w') as file:
        file.write('import os\nimport threading')
        file.write("path = " + str(PATH_FOLDER_CSV))
    importlib.reload(auto_write_thread)




def drawing_circle(blank_image, points, a, b, color):
    [cv2.circle(blank_image, (j[0] + a, j[1] + b) , 2, color, 2)
     for i in points for j in i]



if __name__ == "__main__":
    liste_video = os.listdir(r"C:\Users\jeanbaptiste\Desktop\pounties\videos")
    for i in liste_video:
        print(i)
    recuperate_data_in_csv(1)
    #to_thread(5)





