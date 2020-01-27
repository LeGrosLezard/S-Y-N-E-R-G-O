import cv2
import ast
import math
import numpy as np
from scipy.spatial import distance as dist

from utils_reconstruction import csv_files
from utils_reconstruction import recuperate_data_in_csv



liste = recuperate_data_in_csv(1)


ok = []
for i in liste:
    for j in i:
        x = ast.literal_eval(j)
    
        print(type(x))
        
        
