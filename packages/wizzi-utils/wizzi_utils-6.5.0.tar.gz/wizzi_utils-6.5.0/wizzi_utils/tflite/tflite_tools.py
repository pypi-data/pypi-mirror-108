from wizzi_utils import misc_tools as mt  # misc tools
from wizzi_utils.socket import socket_tools as st
from wizzi_utils.pyplot import pyplot_tools as pyplt
from wizzi_utils.open_cv import open_cv_tools as cvt
import numpy as np
import os
# noinspection PyPackageRequirements
import cv2
# noinspection PyPackageRequirements
import tflite_runtime
# noinspection PyPackageRequirements
from tflite_runtime.interpreter import Interpreter


def get_tflite_version(ack: bool = False, tabs: int = 1) -> str:
    """
    :param ack:
    :param tabs:
    :return:
    see get_tflite_version_test()
    """
    string = mt.add_color('{}* TFLite Version {}'.format(tabs * '\t', tflite_runtime.__version__), ops=mt.SUCCESS_C)
    # string += mt.add_color(' - GPU detected ? ', op1=mt.SUCCESS_C)
    # if gpu_detected():
    #     string += mt.add_color('True', op1=mt.SUCCESS_C2[0], extra_ops=mt.SUCCESS_C2[1])
    # else:
    #     string += mt.add_color('False', op1=mt.FAIL_C2[0], extra_ops=mt.FAIL_C2[1])
    if ack:
        print(string)
    return string


def gpu_detected() -> bool:
    """
    :return:
    TODO FUTURE - maybe check if threads available
    """
    return False


class ssd_mobilenet_coco:
    # TODO check rpi guide
    # https://www.tensorflow.org/lite/guide/python
    # to move to mvs virtual env:
    # cp -r /usr/lib/python3/dist-packages/tflite_runtime* ~/.virtualenvs/mvs/lib/python3.7/site-packages/
    # TODO op1:
    # $ wget "https://raw.githubusercontent.com/PINTO0309/TensorflowLite-bin/main/2.5.0/
    #           download_tflite_runtime-2.5.0-cp37-none-linux_armv7l.whl.sh"
    # $ ./download_tflite_runtime-2.5.0-cp37-none-linux_armv7l.whl.sh
    # $ sudo pip3 install --upgrade tflite_runtime-2.5.0-cp37-none-linux_armv7l.whl
    # from tflite_runtime.interpreter import Interpreter
    # interpreter = Interpreter(model_path="foo.tflite", num_threads=4)

    # https://github.com/EdjeElectronics/TensorFlow-Lite-Object-Detection-on-Android-and-Raspberry-Pi/blob/master/Raspberry_Pi_Guide.md
    # https://blog.paperspace.com/tensorflow-lite-raspberry-pi/
    """
    ssd_mobilenet_coco -
    quick access to tflite models that were designed for devices such as raspberry pi, android and so on
    as far as i know all are ssd_mobilenet models that were trained on coco data set
    """
    MODEL_CONF = {
        'ssd_mobilenet_v3_small_coco_2020_01_14': {  # m1
            'input_dim': (320, 320),
            'input_type': np.uint8,
            'normalize_RGB': False,
            'download_format': 'tar',
            'url': 'http://download.tensorflow.org/models/object_detection/' +
                   'ssd_mobilenet_v3_small_coco_2020_01_14.tar.gz',
            'info': 'https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/'
                    + 'tf1_detection_zoo.md#mobile-models'
        },
        'ssd_mobilenet_v2_mnasfpn_shared_box_predictor_320x320_coco_sync_2020_05_18': {  # m2
            'input_dim': (320, 320),
            'input_type': np.float32,
            'normalize_RGB': True,
            'download_format': 'tar',
            'url': 'http://download.tensorflow.org/models/object_detection/' +
                   'ssd_mobilenet_v2_mnasfpn_shared_box_predictor_320x320_coco_sync_2020_05_18.tar.gz',
            'info': 'https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/'
                    + 'tf1_detection_zoo.md#mobile-models'
        },
        'ssd_mobilenet_v3_large_coco_2020_01_14': {  # m3
            'input_dim': (320, 320),
            'input_type': np.uint8,
            'normalize_RGB': False,
            'download_format': 'tar',
            'url': 'http://download.tensorflow.org/models/object_detection/' +
                   'ssd_mobilenet_v3_large_coco_2020_01_14.tar.gz',
            'info': 'https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/'
                    + 'tf1_detection_zoo.md#mobile-models'
        },
        'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19': {  # m4
            'input_dim': (320, 320),
            'input_type': np.float32,
            'normalize_RGB': True,
            'download_format': 'tar',
            'url': 'http://download.tensorflow.org/models/object_detection/' +
                   'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19.tar.gz',
            'info': 'https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/'
                    + 'tf1_detection_zoo.md#mobile-models'
        },
        'ssd_mobilenet_v1_1_metadata_1': {  # m5
            'input_dim': (300, 300),
            'input_type': np.uint8,
            'normalize_RGB': False,
            'download_format': 'tflite',
            'url': 'https://tfhub.dev/tensorflow/lite-model/ssd_mobilenet_v1/1/metadata/1?lite-format=tflite',
            'info': 'https://www.tensorflow.org/lite/examples/object_detection/overview'
        },
        'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess': {  # m6
            'input_dim': (300, 300),
            'input_type': np.float32,
            'normalize_RGB': True,
            'download_format': 'tflite',
            'url': 'https://drive.google.com/uc?export=download&confirm=${CODE}&id=1LjTqn5nChAVKhXgwBUp00XIKXoZrs9sB',
            'info': 'https://github.com/PINTO0309/PINTO_model_zoo/tree/main/006_mobilenetv2-ssdlite/01_coco/'
                    + '03_integer_quantization'
        },
        'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29': {  # m7
            'input_dim': (300, 300),
            'input_type': np.uint8,
            'normalize_RGB': False,
            'download_format': 'zip',
            'url': 'http://storage.googleapis.com/download.tensorflow.org/models/tflite/' +
                   'coco_ssd_mobilenet_v1_1.0_quant_2018_06_29.zip',
            'info': 'https://gist.github.com/iwatake2222/e4c48567b1013cf31de1cea36c4c061c'
        },
    }

    # TODO more models:
    # TODO: https://www.tensorflow.org/lite/guide/hosted_models
    # TODO: https://github.com/tensorflow/models/blob/master/research/
    #           object_detection/g3doc/tf1_detection_zoo.md#mobile-models  # m1-m4
    # TODO: https://www.tensorflow.org/lite/guide/https://github.com/PINTO0309/PINTO_model_zoo

    COCO_LABELS = LABELS = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                            'traffic light', 'fire hydrant', '???', 'stop sign', 'parking meter', 'bench', 'bird',
                            'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', '???',
                            'backpack', 'umbrella', '???', '???', 'handbag', 'tie', 'suitcase', 'frisbee', 'skis',
                            'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 'skateboard',
                            'surfboard', 'tennis racket', 'bottle', '???', 'wine glass', 'cup', 'fork', 'knife',
                            'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
                            'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', '???', 'dining table',
                            '???', '???', 'toilet', '???', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 'cell phone',
                            'microwave', 'oven', 'toaster', 'sink', 'refrigerator', '???', 'book', 'clock', 'vase',
                            'scissors', 'teddy bear', 'hair drier', 'toothbrush']

    DEFAULT_COLOR_D = {
        'bbox': pyplt.get_BGR_color('r'),
        'label_bbox': pyplt.get_BGR_color('black'),
        'text': pyplt.get_BGR_color('white'),
        'sub_image': pyplt.get_BGR_color('blue'),
    }

    def __init__(self,
                 save_load_dir: str,
                 model_name: str,
                 threshold: float = 0.5,
                 tabs: int = 1
                 ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
            TODO add FPS
            FPS reports are relative. testing was made on relative strong pc - no threads or GPU usage
        :param threshold: only detection above this threshold will be returned
        :param tabs:
        see tests in test_tflite.py
        e.g. test_tflite.py : test_all()
        """
        if model_name not in self.MODEL_CONF:
            mt.exception_error('model name must be one of {}'.format(list(self.MODEL_CONF.keys())), tabs=tabs)
            exit(-1)
        else:  # supported model
            self.model_conf = self.MODEL_CONF[model_name]

        self.name = model_name
        self.model_path = '{}/{}.tflite'.format(save_load_dir, model_name)
        if not os.path.exists(self.model_path):
            mt.create_dir(save_load_dir)
            if self.model_conf['download_format'] in ['tar', 'zip']:
                # download tar.gz\zip file
                if self.model_conf['download_format'] == 'tar':
                    model_comp = '{}/{}.tar.gz'.format(save_load_dir, model_name)
                else:
                    model_comp = '{}/{}.zip'.format(save_load_dir, model_name)

                st.download_file(url=self.model_conf['url'], dst_path=model_comp)
                # extract tar.gz\zip file
                extracted_folder = '{}/extracted'.format(save_load_dir)
                mt.extract_file(src=model_comp, dst_folder=extracted_folder,
                                file_type=self.model_conf['download_format'])
                mt.delete_file(model_comp)

                # move .tflite model to save_load_dir
                tflite_files = mt.find_files_in_folder(
                    dir_path=extracted_folder,
                    file_suffix='.tflite'
                )

                if len(tflite_files) != 1:
                    err_msg = 'not found or found more than 1 tflite files in downloaded folder: {}'.format(
                        tflite_files)
                    mt.exception_error(err_msg, tabs=tabs)
                    exit(-1)

                mt.move_file(
                    file_src=tflite_files[0],
                    file_dst='{}/{}.tflite'.format(save_load_dir, model_name))
                mt.delete_dir_with_files(dir_path=extracted_folder)
            elif self.model_conf['download_format'] == 'tflite':
                # strait download
                st.download_file(url=self.model_conf['url'], dst_path='{}/{}.tflite'.format(save_load_dir, model_name))

        # load model
        self.interpreter = Interpreter(model_path=self.model_path, num_threads=4)
        # try:  # should work on RPi
        #     # self.interpreter.set_num_threads(4)
        #     # self.interpreter.SetNumThreads(4)
        #     print('4 working threads')
        # except AttributeError as e:
        #     mt.exception_error('threads allocation failed: {}'.format(e), tabs=tabs)

        # allocate input output placeholders
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()

        self.tabs = tabs
        self.threshold = threshold  # detection threshold
        return

    def __str__(self):
        string = '{}{}'.format(self.tabs * '\t', mt.add_color(string='ssd_mobilenet_coco:', ops='underlined'))
        string += '\n\t{}name={}'.format(self.tabs * '\t', self.name)
        string += '\n\t{}model_path={}'.format(self.tabs * '\t', self.model_path)
        string += '\n\t{}threshold={}'.format(self.tabs * '\t', self.threshold)
        string += '\n\t{}model_conf={}'.format(self.tabs * '\t', self.model_conf)
        string += '\n\t{}{}'.format(self.tabs * '\t', mt.to_str(self.COCO_LABELS, 'COCO_LABELS', wm=False, chars=200))
        string += '\n\t{}tabs={}'.format(self.tabs * '\t', self.tabs)
        return string

    def prepare_input(self, cv_img: np.array) -> np.array:
        """
        :param cv_img:
        resize and change dtype to predefined params
        :return:
        """
        img_RGB = cvt.BGR_img_to_RGB(cv_img)
        if self.model_conf['normalize_RGB']:
            # normalization is done via the authors of the MobileNet SSD implementation
            img_RGB = (img_RGB - 127.5) * 0.007843  # normalize image
        img = cv2.resize(img_RGB, self.model_conf['input_dim'])  # size of this model input
        img_processed = np.expand_dims(img, axis=0).astype(self.model_conf['input_type'])  # a,b,c -> 1,a,b,c

        # print(mt.to_str(img_processed, 'img_processed'))
        # img_processed_cv = img_processed[0]
        # img_processed_cv = cvt.RGB_img_to_BGR(img_processed_cv)
        # print(mt.to_str(img_processed_cv, 'img_processed_cv'))
        # cv2.imshow("img_processed_cv", img_processed_cv)
        # cv2.waitKey(0)
        # exit(22)

        return img_processed

    def run_network(self, img_preprocessed: np.array) -> None:
        self.interpreter.set_tensor(self.input_details[0]['index'], img_preprocessed)  # set input tensor
        self.interpreter.invoke()  # run
        return

    def extract_results(
            self,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            title: str = None
    ) -> list:
        # get results
        boxes_np = self.interpreter.get_tensor(self.output_details[0]['index'])[0]  # bboxes
        labels_np = self.interpreter.get_tensor(self.output_details[1]['index'])[0]  # labels as list of floats
        confidences_np = self.interpreter.get_tensor(self.output_details[2]['index'])[0]  # confidence
        # count_np = interpreter.get_tensor(output_details[3]['index'])[0]  # number of detections
        labels_ids = [int(label_id) for label_id in labels_np]  # get labels as int
        if ack:
            msg = '{}{} - detections:'
            print(msg.format(tabs * '\t', title if title is not None else '{} on image'.format(self.name)))

        cv_width, cv_height = cv_img.shape[1], cv_img.shape[0]
        detections = []
        for bbox, label_id, confidence in zip(boxes_np, labels_ids, confidences_np):
            if confidence > self.threshold:
                x0 = max(int(bbox[1] * cv_width), 0)
                y0 = max(int(bbox[0] * cv_height), 0)
                x1 = min(int(bbox[3] * cv_width), cv_width)
                y1 = min(int(bbox[2] * cv_height), cv_height)
                label = self.COCO_LABELS[label_id]
                score = round(confidence * 100, fp)

                detection_d = {
                    'label': label,
                    'score': score,
                    'bbox': {
                        #  pt1 = (x0, y0)  # obj frame top left corner
                        #  pt2 = (x1, y1)  # obj frame bottom right corner
                        'x0': x0,
                        'y0': y0,
                        'x1': x1,
                        'y1': y1,
                    },
                }
                detections.append(detection_d)
                if ack:
                    d_msg = '{}\tDetected {}({}%) in top left=({}), bottom right=({})'
                    print(d_msg.format(tabs * '\t', label, score, (x0, y0), (x1, y1)))
        return detections

    def classify_cv_img(self, cv_img: np.array, fp: int = 2, ack: bool = False, tabs: int = 1,
                        title: str = None) -> list:
        """
        :param cv_img: open cv image

        :param fp: float precision on the confidence
        :param ack: print detections if True
        :param tabs:
        :param title:
        :return: list of dicts. each dict is a detection of an object above threshold.
            has items:
                label:str e.g. 'person'
                confidence: float
                bbox: dict with keys x0,y0,x1,y1
                    #  pt1 = (x0, y0)  # obj frame top left corner
                    #  pt2 = (x1, y1)  # obj frame bottom right corner

        cast to RBG, normalize if needed, run model, extract results
        """

        img_preprocessed = self.prepare_input(cv_img)
        self.run_network(img_preprocessed)
        detections = self.extract_results(cv_img, fp, ack, tabs, title)
        return detections

    @staticmethod
    def add_traffic_light_to_detections(detections: list, traffic_light_p: dict) -> list:
        """
        :param detections: detections from classify_cv_img()
        :param traffic_light_p: dict of loc to float percentage
            if not none get 3 2d points in a traffic_light form
            e.g. traffic_light={
                    # x of all traffic_light points is frame_width / 2
                    'up': 0.2,  # red light will be take from y = frame_height * 0.2
                    'mid': 0.3,  # yellow light will be take from y = frame_height * 0.3
                    'down': 0.4  # green light will be take from y = frame_height * 0.3
                }
        :return: for each detection in detections: add entry 'traffic_light' with a dict with keys up, mid, down
                    each has location to dict of point and color:
            e.g.
                'traffic_light'= { # x_mid = frame_width / 2
                'up': {'point': [x_mid, y_up], 'color': 'red'},  # y_up = frame_height * traffic_light['up']
                'mid': {'point': [x_mid, y_mid], 'color': 'yellow'},
                'down': {'point': [x_mid, y_down], 'color': 'green'}
                }
        """
        for detection_d in detections:
            # label = detection_d['label']
            # score = detection_d['score']
            x0 = detection_d['bbox']['x0']
            y0 = detection_d['bbox']['y0']
            x1 = detection_d['bbox']['x1']
            y1 = detection_d['bbox']['y1']
            y_dist = y0 - y1  # image is flipped on y axis
            x_dist = x1 - x0
            # prepare 'traffic_light' points
            # on x middle
            # on y 20% 30% 40% from the top
            x_mid = int(x0 + 0.5 * x_dist)
            y_up = int(y0 - traffic_light_p['up'] * y_dist)
            y_mid = int(y0 - traffic_light_p['mid'] * y_dist)
            y_down = int(y0 - traffic_light_p['down'] * y_dist)
            traffic_light_out = {
                'up': {'point': [x_mid, y_up], 'color': 'red'},
                'mid': {'point': [x_mid, y_mid], 'color': 'yellow'},
                'down': {'point': [x_mid, y_down], 'color': 'green'}
            }
            detection_d['traffic_light'] = traffic_light_out
        return detections

    @staticmethod
    def add_sub_sub_image_to_detection(detections: list, cv_img: np.array, bbox_image_p: dict) -> list:
        """
        :param detections:
        :param cv_img:
        :param bbox_image_p: dict that specify how much from the bbox to save
                bbox_image_p={  # all bbox
                    'x_start': 0,
                    'x_end': 1,
                    'y_start': 0,
                    'y_end': 1,
                },
                bbox_image_p={  # sub bbox
                    'x_start': 0.5,  # start from middle
                    'x_end': 0.9,     # go to the right until 90% of the width
                    'y_start': 0,  # 0 start from the bottom
                    'y_end': 0.4,  # end at 40% from bottom
                },
        :return: for each detection in detections: add entry 'bbox_sub_image' with a dict with keys image,x0,x1,y0,y1
                    if you imshow - you will get the bbox of the detection (according to bbox_image_p)
        """
        for detection_d in detections:
            # label = detection_d['label']
            # score = detection_d['score']
            x0 = detection_d['bbox']['x0']
            y0 = detection_d['bbox']['y0']
            x1 = detection_d['bbox']['x1']
            y1 = detection_d['bbox']['y1']
            y_dist = y0 - y1  # image is flipped on y axis
            x_dist = x1 - x0
            # prepare sub sub image (a part of the bbox)
            # y1 is the bottom
            sub_y0 = int(y1 + bbox_image_p['y_start'] * y_dist)
            sub_y1 = int(y1 + bbox_image_p['y_end'] * y_dist)
            sub_x0 = int(x0 + bbox_image_p['x_start'] * x_dist)
            sub_x1 = int(x0 + bbox_image_p['x_end'] * x_dist)
            detection_d['bbox_sub_image'] = {
                'image': cv_img[sub_y0:sub_y1, sub_x0:sub_x1],
                'x0': sub_x0,
                'y0': sub_y0,
                'x1': sub_x1,
                'y1': sub_y1,
            }
        return detections

    @staticmethod
    def draw_detections(
            detections: list,
            colors_d: dict,
            cv_img: np.array,
            draw_labels: bool = True,
            ack: bool = False,
            tabs: int = 1,
            title: str = None
    ) -> None:
        """
        :param detections: output of self.classify_cv_img()
        :param colors_d: colors in BGR form:
            bbox color
            label_bbox color
            text color
            if class_id_bbox exist - color the bbox of that class in the given color
                e.g. colors_d={
                        'bbox': pyplt.get_BGR_color('r'),
                        'label_bbox': pyplt.get_BGR_color('black'),
                        'text': pyplt.get_BGR_color('white'),
                        'person_bbox': pyplt.get_BGR_color('lightgreen'),
                    },
        :param cv_img: the same that was given input to self.classify_cv_img()
        :param draw_labels: draw label(label_bbox and text on it) on the bbox
        :param ack: if True print the results
        :param tabs:
        :param title:
        :return:
        draw detections on cv_img
        """
        if ack:
            print('{}{} - detections:'.format(tabs * '\t', title if title is not None else 'img'))
        for detection in detections:
            label = detection['label']
            score = detection['score']
            x0 = detection['bbox']['x0']
            y0 = detection['bbox']['y0']
            x1 = detection['bbox']['x1']
            y1 = detection['bbox']['y1']
            traffic_light_d = detection['traffic_light'] if 'traffic_light' in detection else {}
            bbox_sub_image_d = detection['bbox_sub_image'] if 'bbox_sub_image' in detection else None

            k = '{}_bbox'.format(label)
            color_bgr = colors_d[k] if k in colors_d else colors_d['bbox']
            cv2.rectangle(img=cv_img, pt1=(x0, y0), pt2=(x1, y1), color=color_bgr, thickness=2)

            for loc, point_and_color in traffic_light_d.items():
                cv2.circle(cv_img, center=tuple(point_and_color['point']), radius=2,
                           color=pyplt.get_BGR_color(point_and_color['color']), thickness=-1)

            if bbox_sub_image_d is not None:
                pt1 = (bbox_sub_image_d['x0'], bbox_sub_image_d['y0'])
                pt2 = (bbox_sub_image_d['x1'], bbox_sub_image_d['y1'])
                cv2.rectangle(img=cv_img, pt1=pt1, pt2=pt2, color=colors_d['sub_image'], thickness=1)  # sub image

            if draw_labels:
                # text black box at the bottom
                cv2.rectangle(img=cv_img, pt1=(x0, y1), pt2=(x1, y1 - 10), color=colors_d['label_bbox'], thickness=-1)

                # text inside the black box
                label_conf = '{}({:.1f}%)'.format(label, score)
                cv2.putText(cv_img, text=label_conf, org=(x0, y1), fontFace=2, fontScale=0.5, color=colors_d['text'])

            if ack:
                d_msg = '{}\tDetected {}({}%) in top left=({}), bottom right=({}){}'
                tl_msg = ' traffic_light: {}'.format(traffic_light_d) if traffic_light_d is not None else ''
                print(d_msg.format(tabs * '\t', label, score, (x0, y0), (x1, y1), tl_msg))
        return
