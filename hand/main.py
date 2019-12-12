from video_capture import video_capture

#Video
videoA = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\a.mp4"
videoB = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\b.mp4"
videoC = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\c.mp4"
videoD = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\d.mp4"
videoE = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\e.mp4"
videoF = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\f.mp4"
videoH = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\h.mp4"
videoI = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\i.mp4"
videoJ = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\j.mp4"
videoK = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\video\k.mp4"


#Models
path_model = r"C:\Users\jeanbaptiste\Desktop\jgfdposgj\handa\models"
hand_detetion_model =  path_model + "/" + 'frozen_inference_graph.pb'
hand_skelettor_PROTXT = path_model + "/" + 'pose_deploy.prototxt'
hand_skelettor_CAFFE = path_model + "/" + 'pose_iter_102000.caffemodel'


if __name__ == "__main__":

    video_capture(videoA, hand_detetion_model, hand_skelettor_PROTXT, hand_skelettor_CAFFE)
