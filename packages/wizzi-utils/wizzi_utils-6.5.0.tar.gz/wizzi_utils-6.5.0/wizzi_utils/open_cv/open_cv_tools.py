import numpy as np
import math
import os
from wizzi_utils.pyplot import pyplot_tools as pyplt
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.socket import socket_tools as st  # TODO add to req
# noinspection PyPackageRequirements
import cv2


def get_cv_version(ack: bool = False, tabs: int = 1) -> str:
    """ see get_cv_version_test() """
    string = mt.add_color('{}* OpenCv Version {}'.format(tabs * '\t', cv2.getVersionString()), ops=mt.SUCCESS_C)
    if ack:
        print(string)
    return string


def load_img(path: str, ack: bool = True, tabs: int = 1) -> np.array:
    """ see imread_imwrite_test() """
    if os.path.exists(path):
        img = cv2.imread(path)
        if ack:
            size_s = mt.file_or_folder_size(path)
            file_msg = '{}({})'.format(path, size_s)
            print('{}{}'.format(tabs * '\t', mt.LOADED.format(file_msg)))
    else:
        mt.exception_error(mt.NOT_FOUND.format(path), tabs=tabs)
        img = None
    return img


def save_img(path: str, img: np.array, ack: bool = True, tabs: int = 1) -> None:
    """ see imread_imwrite_test() """
    cv2.imwrite(path, img)
    if ack:
        size_s = mt.file_or_folder_size(path)
        file_msg = '{}({})'.format(path, size_s)
        print('{}{}'.format(tabs * '\t', mt.SAVED.format(file_msg)))
    return


def list_to_cv_image(cv_img: [list, np.array]) -> np.array:
    """
    :param cv_img: numpy or list. if list: convert to numpy with dtype uint8
    :return: cv_img
    see list_to_cv_image_test()
    """
    if isinstance(cv_img, list):
        cv_img = np.array(cv_img, dtype='uint8')
    return cv_img


def display_open_cv_image(
        img: np.array,
        ms: int = 0,
        title: str = '',
        loc: (tuple, str) = (0, 0),
        resize: float = None
) -> None:
    """
    :param img: cv image in numpy array or list
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param loc: top left corner window location
        if tuple: x,y coordinates
        if str: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    :param resize: None for original size. else img_size *= resize (resize > 0)
    see display_open_cv_image_test()
    """
    img = list_to_cv_image(img)
    if resize is not None:
        img = resize_opencv_image(img, resize)
    cv2.imshow(title, img)
    if isinstance(loc, str):
        move_cv_img_by_str(img, title, where=loc)
    elif isinstance(loc, tuple):
        move_cv_img_x_y(title, x_y=loc)
    cv2.waitKey(ms)
    return


def resize_opencv_image(img: np.array, scale_percent: float):
    """
    :param img: cv img
    :param scale_percent: float>0(could be bigger than 1)
    img_size *= scale_percent
    see resize_opencv_image_test()
    """
    if scale_percent is None or scale_percent <= 0:
        resize_image = img
        mt.exception_error('illegal value for scale_percent={}'.format(scale_percent), tabs=0)
    else:
        width = math.ceil(img.shape[1] * scale_percent)
        height = math.ceil(img.shape[0] * scale_percent)
        dim = (width, height)
        resize_image = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    return resize_image


def move_cv_img_x_y(win_title: str, x_y: tuple) -> None:
    """
    :param win_title: cv img with win_title to be moved
    :param x_y: tuple of ints. x,y of top left corner
    Move cv img upper left corner to pixel (x, y)
    see move_cv_img_x_y_test()
    """
    cv2.moveWindow(win_title, x_y[0], x_y[1])
    return


def move_cv_img_by_str(img: np.array, win_title: str, where: str = pyplt.Location.TOP_LEFT.value) -> None:
    """
    :param img: to get the dims of the image
    :param win_title: cv img with win_title to be moved
    :param where: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    Move cv img upper left corner to pixel (x, y)
    see move_cv_img_by_str_test()
    """
    try:
        window_w, window_h = pyplt.screen_dims()  # screen dims in pixels
        if window_w != -1 and window_h != -1:
            fig_w, fig_h = img.shape[1], img.shape[0]
            task_bar_offset = 75  # about 75 pixels due to task bar

            x, y = 0, 0  # Location.TOP_LEFT.value: default
            if where == pyplt.Location.TOP_CENTER.value:
                x = (window_w - fig_w) / 2
                y = 0
            elif where == pyplt.Location.TOP_RIGHT.value:
                x = window_w - fig_w
                y = 0
            elif where == pyplt.Location.CENTER_LEFT.value:
                x = 0
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.CENTER_CENTER.value:
                x = (window_w - fig_w) / 2
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.CENTER_RIGHT.value:
                x = window_w - fig_w
                y = (window_h - fig_h - task_bar_offset) / 2
            elif where == pyplt.Location.BOTTOM_LEFT.value:
                x = 0
                y = window_h - fig_h - task_bar_offset
            elif where == pyplt.Location.BOTTOM_CENTER.value:
                x = (window_w - fig_w) / 2
                y = window_h - fig_h - task_bar_offset
            elif where == pyplt.Location.BOTTOM_RIGHT.value:
                x = window_w - fig_w
                y = window_h - fig_h - task_bar_offset
            x, y = int(x), int(y)
            move_cv_img_x_y(win_title, x_y=(x, y))
        else:
            move_cv_img_x_y(win_title, x_y=(0, 0))
    except (ValueError, Exception) as e:
        mt.exception_error(e)
        move_cv_img_x_y(win_title, x_y=(0, 0))
    return


def unpack_list_imgs_to_big_image(imgs: list, grid: tuple, resize: float = None) -> np.array:
    """
    :param imgs: list of cv images
    :param resize: resize factor
    :param grid: the layout you want as output
        (1,len(imgs)): 1 row
        (len(imgs),1): 1 col
        (2,2): 2x2 grid - supports len(imgs)<=4 but not more
    see unpack_list_imgs_to_big_image_test()
    """
    for i in range(len(imgs)):
        imgs[i] = list_to_cv_image(imgs[i])
        if resize is not None:
            imgs[i] = resize_opencv_image(imgs[i], resize)
        if len(imgs[i].shape) == 2:  # if gray - see as rgb
            imgs[i] = gray_scale_img_to_BGR_form(imgs[i])

    imgs_n = len(imgs)
    if imgs_n == 1:
        big_img = imgs[0]
    else:
        padding_bgr = list(pyplt.get_BGR_color('red'))
        height, width, cnls = imgs[0].shape
        rows, cols = grid
        big_img = np.zeros(shape=(height * rows, width * cols, cnls), dtype='uint8') + 255  # white big image

        row_ind, col_ind = 1, 1
        for i, img in enumerate(imgs):
            h_begin, h_end = height * (row_ind - 1), height * row_ind
            w_begin, w_end = width * (col_ind - 1), width * col_ind
            big_img[h_begin:h_end, w_begin:w_end, :] = img  # 0

            if rows > 1:  # draw bounding box on the edges. no need if there is 1 row or 1 col
                big_img[h_begin, w_begin:w_end, :] = padding_bgr
                big_img[h_end - 1, w_begin:w_end - 1, :] = padding_bgr
            if cols > 1:
                big_img[h_begin:h_end, w_begin, :] = padding_bgr
                big_img[h_begin:h_end, w_end - 1, :] = padding_bgr

            col_ind += 1
            if col_ind > cols:
                col_ind = 1
                row_ind += 1
    return big_img


def display_open_cv_images(
        imgs: list,
        ms: int = 0,
        title: str = '',
        loc: (tuple, str) = (0, 0),
        resize: float = None,
        grid: tuple = (1, 2)
) -> None:
    """
    :param imgs: list of RGB or gray scale images
    :param ms: 0 blocks, else time in milliseconds before image is closed
    :param title: window title
    :param loc: top left corner window location
        if tuple: x,y coordinates
        if str: see Location enum in pyplt. e.g. pyplt.Location.TOP_LEFT.value (which is 'top_left')
    :param resize: None for original size. else img_size *= resize (resize > 0)
    :param grid: size of rows and cols of the new image. e.g. (2,1) 2 rows with 1 img on each
        grid slots must be >= len(imgs)
    see display_open_cv_images_test()
    """
    imgs_n = len(imgs)
    if imgs_n > 0:
        total_slots = grid[0] * grid[1]
        assert imgs_n <= total_slots, 'grid has {} total_slots, but len(imgs)={}'.format(total_slots, imgs_n)
        big_img = unpack_list_imgs_to_big_image(imgs, grid=grid, resize=resize)
        display_open_cv_image(big_img, ms, title, loc, resize=None)
    return


def gray_scale_img_to_BGR_form(gray_img: np.array) -> np.array:
    """
    :param gray_img: from shape (x,y) - 1 channel (gray)
    e.g 480,640
    :return: RGB form image e.g 480,640,3. no real colors added - just shape as RGB
    see gray_to_BGR_and_back_test()
    """
    BGR_image = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2BGR)
    return BGR_image


def BGR_img_to_gray(bgr_img: np.array) -> np.array:
    """
    :param bgr_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: gray image e.g 480,640. colors are replaced to gray colors
    see gray_to_BGR_and_back_test()
    """
    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    return gray


def BGR_img_to_RGB(bgr_img: np.array) -> np.array:
    """
    :param bgr_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: rgb image
    see BGR_img_to_RGB_and_back_test()
    """
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    return rgb_img


def RGB_img_to_BGR(rgb_img: np.array) -> np.array:
    """
    :param rgb_img: from shape (x,y,3) - 3 channels
    e.g 480,640,3
    :return: bgr image
    see BGR_img_to_RGB_and_back_test()
    """
    bgr_img = cv2.cvtColor(rgb_img, cv2.COLOR_RGB2BGR)
    return bgr_img


class CameraWu:
    def __init__(self, port: int, type_cam: str = 'cv2'):
        self.port = port
        self.type_cam = type_cam
        if type_cam == 'acapture':
            # noinspection PyPackageRequirements
            import acapture  # pip install acapture
            if mt.is_linux():  # NOT TESTED
                acapture.camera_info()
            self.cam = acapture.open(0)
        elif type_cam == 'imutils':
            # noinspection PyPackageRequirements
            from imutils import video  # pip install imutils
            self.cam = video.VideoStream(src=port).start()
        else:  # type_cam == 'cv2'
            self.cam = cv2.VideoCapture(port)
        return

    def __del__(self):
        print('Closing {}'.format(self.type_cam))
        if self.type_cam == 'acapture':
            # noinspection PyUnresolvedReferences
            self.cam.destroy()
        elif self.type_cam == 'imutils':
            # noinspection PyUnresolvedReferences
            self.cam.stop()
        else:  # type_cam == 'cv2'
            if self.cam.isOpened():
                self.cam.release()
        return

    def read_img(self) -> (bool, np.array):
        success, frame = False, None
        if self.type_cam == 'acapture':
            # import acapture
            # self.cam.destroy()
            # self.cam = acapture.open(self.port)
            success, frame = self.cam.read()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif self.type_cam == 'imutils':
            success = True
            frame = self.cam.read()
        else:  # type_cam == 'cv2'
            if self.cam.isOpened():
                # self.cam.release()
                # self.cam = cv2.VideoCapture(self.port)
                success, frame = self.cam.read()
                # self.cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
            else:
                mt.exception_error('CameraWu is closed')
        return success, frame


class yolov3_coco:
    # TODO FPS TEST AGAIN
    # TODO download img? upload to lib resources?
    # TODO cuda support?
    """
    """
    MODEL_CONF = {
        'yolov3': {  # m1 - https://github.com/rydercalmdown/dog_detector
            'input_dim': (320, 320),
            'input_type': np.uint8,
            'normalize_RGB': False,
            'info': 'https://github.com/arunponnusamy/object-detection-opencv',
            'weights_url': 'https://pjreddie.com/media/files/yolov3.weights',
            'cfg_url': 'https://github.com/arunponnusamy/object-detection-opencv/blob/master/yolov3.cfg',
        },
    }
    # TODO more models: https://github.com/pjreddie/darknet
    # TODO more models: https://github.com/ultralytics/yolov3
    COCO_LABELS = ['person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 'boat',
                   'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird', 'cat', 'dog',
                   'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag',
                   'tie', 'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat',
                   'baseball glove', 'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 'fork',
                   'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog',
                   'pizza', 'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed', 'dining table', 'toilet', 'tv',
                   'laptop', 'mouse', 'remote', 'keyboard', 'cell phone', 'microwave', 'oven', 'toaster', 'sink',
                   'refrigerator', 'book', 'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush']

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
                 nms_threshold: float = 0.3,
                 tabs: int = 1
                 ):
        """
        :param save_load_dir: where the model is saved (or will be if not exists)
        :param model_name: valid name in MODEL_CONF.keys()
        :param threshold: only detection above this threshold will be returned
        :param nms_threshold: non maximum suppression threshold
        :param tabs:
        see
        """

        if model_name not in self.MODEL_CONF:
            mt.exception_error('model name must be one of {}'.format(list(self.MODEL_CONF.keys())), tabs=tabs)
            exit(-1)
        else:  # supported model
            self.model_conf = self.MODEL_CONF[model_name]

        self.tabs = tabs
        self.threshold = threshold  # detection threshold
        self.nms_threshold = nms_threshold  # non maximum suppression threshold
        self.name = model_name
        self.model_w = '{}/{}.weights'.format(save_load_dir, model_name)
        self.model_cfg = '{}/{}.cfg'.format(save_load_dir, model_name)
        self.time_since_last_detection = -np.inf

        # noinspection PyPackageRequirements
        # import pyttsx3  # pip install pyttsx3  # HANDLE REQ
        # self.speech_engine = pyttsx3.init()
        # self.announcement_timeout_frame = 10  # param
        # self.announcement_frames = self.announcement_timeout_frame  # on first detection say and wait

        if not os.path.exists(save_load_dir):
            mt.create_dir(save_load_dir)

        if not os.path.exists(self.model_w):
            # strait download
            st.download_file(url=self.model_conf['weights_url'], dst_path=self.model_w)

        if not os.path.exists(self.model_cfg):
            # strait download
            st.download_file(url=self.model_conf['cfg_url'], dst_path=self.model_cfg)

        print('{}Loading model weights and Config'.format(self.tabs * '\t'))
        self.network = cv2.dnn.readNetFromDarknet(cfgFile=self.model_cfg, darknetModel=self.model_w)
        self.layer_names = [self.network.getLayerNames()[i[0] - 1] for i in self.network.getUnconnectedOutLayers()]
        return

    def __str__(self):
        string = '{}{}'.format(self.tabs * '\t', mt.add_color(string='ssd_mobilenet_coco:', ops='underlined'))
        string += '\n\t{}name={}'.format(self.tabs * '\t', self.name)
        string += '\n\t{}model weights={}'.format(self.tabs * '\t', self.model_w)
        string += '\n\t{}model cfg={}'.format(self.tabs * '\t', self.model_cfg)
        string += '\n\t{}threshold={}'.format(self.tabs * '\t', self.threshold)
        string += '\n\t{}model_conf={}'.format(self.tabs * '\t', self.model_conf)
        string += '\n\t{}{}'.format(self.tabs * '\t', mt.to_str(self.COCO_LABELS, 'COCO_LABELS', chars=200))
        string += '\n\t{}tabs={}'.format(self.tabs * '\t', self.tabs)
        return string

    @staticmethod
    def prepare_input(cv_img: np.array) -> np.array:
        """
        :param cv_img:
        :return:
        """
        img_processed = cv2.dnn.blobFromImage(cv_img, scalefactor=1 / 255.0, size=(416, 416), swapRB=True, crop=False)
        # print(mt.to_str(img_processed, 'img_processed'))
        # img_processed_cv = img_processed[0]
        # img_processed_cv = np.swapaxes(img_processed_cv, 0, 1)  # 3x416x416 -> 416x3x416
        # img_processed_cv = np.swapaxes(img_processed_cv, 1, 2)  # 416x3x416 -> 416x416x3
        # img_processed_cv = RGB_img_to_BGR(img_processed_cv)
        # print(mt.to_str(img_processed_cv, 'img_processed_cv'))
        # cv2.imshow("img_processed_cv", img_processed_cv)
        # cv2.waitKey(0)
        # exit(22)
        return img_processed

    def run_network(self, img_preprocessed: np.array) -> list:
        self.network.setInput(img_preprocessed)
        outputs = self.network.forward(self.layer_names)
        # |output| = 3 - the scales of detections
        # probably related to self.network.getUnconnectedOutLayers() >>> ['yolo_82', 'yolo_94', 'yolo_106']
        # print(mt.to_str(outputs, 'outputs'))
        # print(mt.to_str(outputs[0], 'yolo_82'))
        # print(mt.to_str(outputs[1], 'yolo_94'))
        # print(mt.to_str(outputs[2], 'yolo_106'))
        # exit(22)
        return outputs

    def extract_results(
            self,
            outputs: list,
            cv_img: np.array,
            fp: int = 2,
            ack: bool = False,
            tabs: int = 1,
            title: str = None
    ) -> (list, list, list):
        h, w = cv_img.shape[0], cv_img.shape[1]
        bbox_list, confidence_list, class_id_list = [], [], []  # needed for non maximum suppression

        if ack:
            msg = '{}{} - detections:'
            print(msg.format(tabs * '\t', title if title is not None else '{} on image'.format(self.name)))

        for output in outputs:
            # |outputs| - one for each output scale
            for detection in output:
                # |detection| = 85.
                # 0-3(first 4) are the bbox x,y,w(width),h(height)
                # 5-84(last 80 |COCO_LABELS|) are scores per class
                # TODO figure out what is detection[4]
                confidences = detection[-len(self.COCO_LABELS):]  # take last |COCO_LABELS|
                class_id = int(np.argmax(confidences))
                confidence = confidences[class_id]
                if confidence >= self.threshold:
                    label = self.COCO_LABELS[class_id]
                    score = round(confidence * 100, fp)

                    box = (detection[0:4] * np.array([w, h, w, h])).astype("int")
                    (center_x, center_y, prediction_width, prediction_height) = box

                    # get top left corner
                    x0 = int(center_x - (prediction_width / 2))
                    y0 = int(center_y - (prediction_height / 2))
                    x1 = x0 + prediction_width
                    y1 = y0 + prediction_height
                    bbox = [x0, y0, int(prediction_width), int(prediction_height)]
                    bbox_list.append(bbox)
                    confidence_list.append(float(confidence))
                    class_id_list.append(class_id)
                    if ack:
                        d_msg = '{}\tDetected {}({}%) in top left=({}), bottom right=({}) - pre NMS'
                        print(d_msg.format(tabs * '\t', label, score, (x0, y0), (x1, y1)))
        results = cv2.dnn.NMSBoxes(
            bbox_list,
            confidence_list,
            self.threshold,
            self.nms_threshold
        )
        # best_detection_label = None
        # best_detection_conf = 0.0
        detections = []
        if len(results) > 0:
            # print(mt.to_str(bbox_list, 'bbox_list'))
            # print(mt.to_str(confidence_list, 'confidence_list'))
            # print(mt.to_str(results.flatten(), 'results'))

            for res in results.flatten():
                bbox = bbox_list[res]
                confidence = confidence_list[res]
                class_id = class_id_list[res]
                # print(mt.to_str(bbox, 'bbox'))
                # print(mt.to_str(confidence, 'confidence'))
                # print(mt.to_str(class_id, 'class_id'))

                label = self.COCO_LABELS[class_id]
                score = round(confidence * 100, fp)
                # print(mt.to_str(label, 'label'))
                # print(mt.to_str(score, 'score'))

                # if confidence > best_detection_conf:
                #     best_detection_conf = confidence
                #     best_detection_label = class_id

                (x0, y0) = (bbox[0], bbox[1])
                (w, h) = (bbox[2], bbox[3])

                x1 = x0 + w
                y1 = y0 + h
                # colour = pyplt.get_BGR_color('r')
                # cv2.rectangle(cv_img, (x, y), (x + w, y + h), colour, 2)

                # label_conf = '{}({:.1f}%)'.format(class_id, confidence)
                # cv2.putText(cv_img, text=label_conf, org=(x, y - 5), fontFace=2, fontScale=0.5, color=colour)
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
                    d_msg = '{}\tDetected {}({}%) in top left=({}), bottom right=({}) - post NMS'
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
                class_id:str e.g. 'person'
                confidence: float
                bbox: dict with keys x0,y0,x1,y1
                    #  pt1 = (x0, y0)  # obj frame top left corner
                    #  pt2 = (x1, y1)  # obj frame bottom right corner

        cast to RBG, normalize if needed, run model, extract results
        """
        blob = self.prepare_input(cv_img)
        outputs = self.run_network(blob)

        detections = self.extract_results(outputs, cv_img, fp, ack, tabs, title)

        # if self.announcement_frames >= self.announcement_timeout_frame:
        #     if best_detection_label is not None:
        #         speech = "Attention. There is a {} outside.".format(best_detection_label)
        #     else:
        #         speech = "There is nothing outside"
        #     self.speech_engine.say(speech)
        #     self.speech_engine.runAndWait()
        #     self.announcement_frames = 1
        # else:
        #     self.announcement_frames += 1

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
            # confidence = detection_d['score']
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
