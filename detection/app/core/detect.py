from .yolo_nas_onnx.models import load_net
from .yolo_nas_onnx.processing import Preprocessing, Postprocessing
from .yolo_nas_onnx.draw import draw_box
from .yolo_nas_onnx.utils import Labels
import cv2
import numpy as np


def detect(net, source, pre_process, post_process, labels, img3):
    net_input = source.copy()  # copy source array
    input_, prep_meta = pre_process(net_input)  # run preprocess
    outputs = net.forward(input_)  # forward

    boxes, scores, classes = post_process(outputs, prep_meta)  # postprocess output
    selected = cv2.dnn.NMSBoxes(
        boxes, scores, post_process.score_thres, post_process.iou_thres
    )  # run nms to filter boxes
    b_box = []
    for i in selected:  # loop through selected idx
        box = boxes[i, :].astype(np.int32).flatten() # get box
        b_box.append(box)
        score = float(scores[i]) * 100  # percentage score
        label, color = labels(classes[i], use_bgr=True)  # get label and color class_id

        draw_box(source, box, label, score, color)  # draw boxes

    return source, b_box, prep_meta, scores  # Image array after draw process


use_gpu = True
use_opencv_dnn_runtime = False
model_path = "average_model.onnx"

net = load_net(model_path, use_gpu, use_opencv_dnn_runtime)
net.assert_input_shape([1, 3, 640, 640])
net.warmup()


def detection(img, ):
    img3 = img.copy()
    prep_steps = [
        {"DetLongMaxRescale": None},
        {"BotRightPad": {"pad_value": 114}}
    ]

    iou_thres = 0.65
    score_thres = 0.5
    labels = ["0"]

    _, _, input_height, input_width = net.input_shape  # get input height and width [b, c, h, w]

    pre_process = Preprocessing(
        prep_steps, (input_height, input_width)
    )

    post_process = Postprocessing(
        prep_steps,
        iou_thres,
        score_thres,
    )

    labels = Labels(labels)

    img1, b_boxes, prep_meta, scores = detect(net, img, pre_process, post_process, labels, img3)
    return img1, b_boxes, scores
