import cv2
import math
import numpy as np
from scipy.spatial import distance as dist

from utils_reconstruction import csv_files
from utils_reconstruction import recuperate_data_in_csv



liste = recuperate_data_in_csv(1)


ok = []
for i in liste:
    print(i[0])
    for j in i[0]:
        ok.append(j)
print(ok)

        
        
