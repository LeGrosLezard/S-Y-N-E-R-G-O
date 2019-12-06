from video_capture import video_capture

#Video
videoA = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\a.mp4"
videoB = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\b.mp4"
videoC = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\c.mp4"
videoD = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\d.mp4"
videoE = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\e.mp4"
videoF = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\f.mp4"



#Models
hand_model =  r'C:\Users\jeanbaptiste\Desktop\jgfdposgj\handtracking-master\hand_inference_graph\frozen_inference_graph.pb'



if __name__ == "__main__":

    video_lecture(videoA, hand_model)
