from video_capture import video_lecture

#Video
videoA = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\a.mp4"
videoB = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\b.mp4"


#Models
facePoints = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\face\models\shape_predictor_68_face_landmarks.dat"




if __name__ == "__main__":

    video_lecture(videoA, facePoints)
