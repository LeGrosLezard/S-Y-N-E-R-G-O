
import csv
with open('eggs.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
    for i in range(100):
        spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

    
#====================================== Writte in to csv ===============================

def header_csv(name_csv):                                           #Write header
                                                                    #New csv

    with open(name_csv, 'w', newline='') as csvfile:
        fieldnames = ["", "", "", ""]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def writting_data(name_csv, data):                                  #Add into csv

    with open(name_csv, 'a', newline='') as csvfile:
        for k, v in data.items():
            writer.writerow({k: v})





#===================================== Verify length of csv =============================
import os

PATH_OK_CSV = r"C:\Users\jeanbaptiste\Desktop\dougy_petits_pecs\c_csv_files\ok_data"



def last_csv_into_folder():                                         #Recuperate last csv
    global PATH_OK_CSV

    liste_csv = sorted([int(i[:-4]) for i in os.listdir(PATH_OK_CSV)])
    print(liste_csv[-1])
    return liste_csv[-1]



def verify_length_csv(name):                                        #verify_length_csv
    global PATH_OK_CSV

    path = PATH_OK_CSV + "/" + str(name) + ".csv"

    data_number = 0
    with open(path, "rb") as csvfile:
        for i in csvfile:
            data_number += 1

    if data_number == 101:
        print("CSV rempli créez en un nouveau")





if __name__ == "__main__":

    last_csv = last_csv_into_folder()
    verify_length_csv(last_csv)














