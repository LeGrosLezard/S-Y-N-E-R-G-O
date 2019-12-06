import cv2
import tensorflow as tf
import numpy as np

print(tf.version.VERSION)


# Load a frozen infrerence graph into memory
def load_inference_graph(path_to_ckpt):

    # load frozen tensorflow model into memory
    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.compat.v1.GraphDef()
        with tf.io.gfile.GFile(path_to_ckpt, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
        sess = tf.compat.v1.Session(graph=detection_graph)
    return detection_graph, sess



def detect_objects(image_np, detection_graph, sess):
    # Definite input and output Tensors for detection_graph
    image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
    # Each box represents a part of the image where a particular object was detected.
    detection_boxes = detection_graph.get_tensor_by_name(
        'detection_boxes:0')
    # Each score represent how level of confidence for each of the objects.
    # Score is shown on the result image, together with the class label.
    detection_scores = detection_graph.get_tensor_by_name(
        'detection_scores:0')
    detection_classes = detection_graph.get_tensor_by_name(
        'detection_classes:0')
    num_detections = detection_graph.get_tensor_by_name(
        'num_detections:0')

    image_np_expanded = np.expand_dims(image_np, axis=0)

    (boxes, scores, classes, num) = sess.run(
        [detection_boxes, detection_scores,
            detection_classes, num_detections],
        feed_dict={image_tensor: image_np_expanded})
    return np.squeeze(boxes), np.squeeze(scores)



def draw_box_on_image(num_hands_detect, score_thresh, scores, boxes, im_width, im_height, image_np):
    for i in range(num_hands_detect):
        if (scores[i] > score_thresh):
            (left, right, top, bottom) = (boxes[i][1] * im_width, boxes[i][3] * im_width,
                                          boxes[i][0] * im_height, boxes[i][2] * im_height)
            p1 = (int(left), int(top))
            p2 = (int(right), int(bottom))
            cv2.rectangle(image_np, p1, p2, (77, 255, 9), 3, 1)


def video_capture(video_name, hand_model):

    detection_graph, sess = load_inference_graph(hand_model)

    video = cv2.VideoCapture(video_name)
    while True:
        frame = cv2.resize(video.read()[1], (500, 400))

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        boxes, scores = detect_objects(frame, detection_graph, sess)
        draw_box_on_image(2, 0.20, scores, boxes, 500, 400, frame)


        cv2.imshow('frame', frame)


        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    video.release()
    destroyAllWindows()


video_capture("a.mp4", path_to_ckpt)





















