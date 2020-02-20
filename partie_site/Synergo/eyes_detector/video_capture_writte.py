import time

start_time_import = time.time()

import cv2
import numpy as np

#Recuperate face points.
from .recuperate_points.face_points import recuperate_landmarks
from .recuperate_points.face_points import head_points
from .recuperate_points.face_points import get_face_in_box
from .recuperate_points.face_points import eyes_points_for_head_analysis

#Path to model, to media folder.
from .paths import media_path, dlib_model

#Load dlib model
from .recuperate_points.face_points import load_model_dlib

#Resize video.
from .pre_treatment.pre_test import search_video_size

print("Import time : ", time.time() - start_time_import)


from .pre_treatment.pre_test import search_video_size
from .pre_treatment.writter import video_writter
from .pre_treatment.writter import run_data_wrote

def video_capture_treament(video, dlib_model):

    start_treatment = time.time()

    #Load model.
    predictor, detector = load_model_dlib(dlib_model)

    #Search size of resize.
    number_divise = search_video_size(video, predictor, detector, dlib_model)

    #Divise video to file of 20 sec.
    video_writter(video, number_divise)

    #data = run_data_wrote()

    print("End treatment : ", time.time() - start_treatment)

    return data


##video = r"C:\Users\jeanbaptiste\Desktop\videos\e.mp4"
##video_capture_treament(video, dlib_model)
