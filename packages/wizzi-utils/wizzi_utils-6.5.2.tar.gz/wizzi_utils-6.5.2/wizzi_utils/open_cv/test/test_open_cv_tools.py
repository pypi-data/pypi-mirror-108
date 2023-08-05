from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv import open_cv_tools as cvt
from wizzi_utils.socket import socket_tools as st
from wizzi_utils.pyplot import pyplot_tools as pyplt
import numpy as np
import os
# noinspection PyPackageRequirements
import cv2

LOOP_TESTS = 50
BLOCK_SECONDS_NORMAL = 2  # 0 to block
ITERS_CAM_TEST = 50  # 0 to block
MODEL_DELAY_FOLDER = 2
MODEL_DELAY_CAM = None
MODEL_FRAMES_CAM = 10


def load_img_from_web(dst: str) -> np.array:
    # url = 'https://cdn.sstatic.net/Sites/stackoverflow/img/logo.png'
    # dst = './logo.png'
    url = mtt.TEMP_IMAGE_LOGO_URL

    if not os.path.exists(dst):
        success = st.download_file(url, dst)
        if not success:
            mt.exception_error('download failed - creating random img')
            img = mt.np_random_integers(size=(240, 320, 3), low=0, high=255)
            img = img.astype('uint8')
            cvt.save_img(dst, img)

    img = cvt.load_img(path=dst)
    return img


def get_cv_version_test():
    mt.get_function_name(ack=True, tabs=0)
    cvt.get_cv_version(ack=True, tabs=1)
    return


def imread_imwrite_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    path = './v2_{}'.format(mtt.TEMP_IMAGE_NAME)
    cvt.save_img(path, img, ack=True)
    img_loaded = cvt.load_img(path, ack=True)
    print(mt.to_str(img_loaded, '\timg'))
    mt.delete_file(path, ack=True)
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def list_to_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    img_list = img.tolist()
    print(mt.to_str(img_list, '\timg_list'))
    img = cvt.list_to_cv_image(img_list)
    print(mt.to_str(img, '\timg'))
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def display_open_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    print('\tVisual test: stack overflow logo')
    loc = (70, 200)  # move to X,Y
    resize = 1.7  # enlarge to 170%
    cvt.display_open_cv_image(
        img=img,
        ms=1,  # not blocking
        title='stack overflow logo moved to {} and re-sized to {}'.format(loc, resize),
        loc=loc,  # start from x =70 y = 0
        resize=resize
    )
    loc = pyplt.Location.TOP_RIGHT.value  # move to top right corner
    resize = 1.7  # enlarge to 170%
    cvt.display_open_cv_image(
        img=img,
        ms=BLOCK_SECONDS_NORMAL * 1000,  # blocking
        title='stack overflow logo moved to {} and re-sized to {}'.format(loc, resize),
        loc=loc,  # start from x =70 y = 0
        resize=resize
    )
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def display_open_cv_image_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    loc = (70, 200)  # move to X,Y
    resize = 1.7  # enlarge to 170%
    title = 'stack overflow logo moved to {} and re-sized to {} - {} iterations'.format(loc, resize, LOOP_TESTS)
    print('\tVisual test: {}'.format(title))
    for i in range(LOOP_TESTS):
        cvt.display_open_cv_image(
            img=img,
            ms=1,  # not blocking
            title=title,
            loc=loc,  # start from x =70 y = 0
            resize=resize
        )
        if i == 0:  # move just first iter
            loc = None
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def resize_opencv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    print(mt.to_str(img, '\timg'))
    img = cvt.resize_opencv_image(img, scale_percent=0.6)
    print(mt.to_str(img, '\timg re-sized to 60%'))
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def move_cv_img_x_y_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    options = [(0, 0), (100, 0), (0, 100), (150, 150), (400, 400), (250, 350)]
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for x_y in options:
        title = 'move to ({})'.format(x_y)
        cv2.imshow(title, img)
        cvt.move_cv_img_x_y(title, x_y)
    cv2.waitKey(BLOCK_SECONDS_NORMAL * 1000)
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def move_cv_img_by_str_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    options = pyplt.Location.get_location_list_by_rows()
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for where_to in options:
        title = 'move to {}'.format(where_to)
        cv2.imshow(title, img)
        cvt.move_cv_img_by_str(img, title, where=where_to)
    cv2.waitKey(BLOCK_SECONDS_NORMAL * 1000)
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def unpack_list_imgs_to_big_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    gray = cvt.BGR_img_to_gray(img)
    big_img = cvt.unpack_list_imgs_to_big_image(
        imgs=[img, gray, img],
        resize=None,
        grid=(2, 2)
    )
    title = 'stack overflow logo 2x2(1 empty)'
    print('\tVisual test: {}'.format(title))
    cvt.display_open_cv_image(
        img=big_img,
        ms=BLOCK_SECONDS_NORMAL * 1000,  # blocking
        title=title,
        loc=(0, 0),
        resize=None
    )
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def display_open_cv_images_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    title = '2x1 grid'
    print('\tVisual test: {}'.format(title))
    loc1 = (0, 0)
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=1,  # blocking
        title='{} loc={}'.format(title, loc1),
        loc=loc1,
        resize=None,
        grid=(2, 1)
    )
    loc2 = pyplt.Location.BOTTOM_CENTER.value
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=BLOCK_SECONDS_NORMAL * 1000,  # blocking
        title='{} loc={}'.format(title, loc2),
        loc=loc2,
        resize=None,
        grid=(2, 1)
    )
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def display_open_cv_images_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    loc = (70, 200)  # move to X,Y
    title = 'stack overflow logo moved to {} - {} iterations'.format(loc, LOOP_TESTS)
    print('\tVisual test: {}'.format(title))
    for i in range(LOOP_TESTS):
        cvt.display_open_cv_images(
            imgs=[img, img],
            ms=1,  # blocking
            title=title,
            loc=loc,
            resize=None,
            grid=(2, 1)
        )
        if i == 0:  # move just first iter
            loc = None
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def gray_to_BGR_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    print(mt.to_str(img, '\timgRGB'))
    gray = cvt.BGR_img_to_gray(img)
    print(mt.to_str(img, '\timg_gray'))
    img = cvt.gray_scale_img_to_BGR_form(gray)
    print(mt.to_str(img, '\timgRGB'))
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def BGR_img_to_RGB_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    imgBGR1 = load_img_from_web(mtt.TEMP_IMAGE_PATH)
    print(mt.to_str(imgBGR1, '\timgBGR'))
    imgRGB = cvt.BGR_img_to_RGB(imgBGR1)
    print(mt.to_str(imgRGB, '\timgRGB'))
    imgBGR2 = cvt.RGB_img_to_BGR(imgRGB)
    print(mt.to_str(imgBGR2, '\timgBGR2'))

    cvt.display_open_cv_images(
        imgs=[imgBGR1, imgRGB, imgBGR2],
        ms=BLOCK_SECONDS_NORMAL * 1000,  # blocking
        title='imgBGR1, imgRGB, imgBGR2',
        loc=pyplt.Location.CENTER_CENTER,
        resize=None,
        grid=(3, 1)
    )
    cv2.destroyAllWindows()
    mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def CameraWu_test(type_cam: str):
    WITH_SLEEP = False
    ports = [0, 1, 13]
    cams = []
    for port in ports:
        cam = cvt.CameraWu.open_camera(port=port, type_cam=type_cam)
        if cam is not None:
            cams.append(cam)

    for cam in cams:
        title = 'CameraWu_test({}) on port {}'.format(cam.type_cam, cam.port)
        fps = mt.FPS(summary_title=title)
        for i in range(ITERS_CAM_TEST):
            fps.start()
            success, cv_img = cam.read_img()
            if WITH_SLEEP:
                mt.sleep(1)

            if success:
                cvt.display_open_cv_image(
                    img=cv_img,
                    ms=1,
                    title=title,
                    loc=pyplt.Location.CENTER_CENTER,
                    resize=None,
                )
            fps.update()
        fps.finalize()
    cv2.destroyAllWindows()
    return


def CameraWu_cv2_test():
    mt.get_function_name(ack=True, tabs=0)
    CameraWu_test(type_cam='cv2')
    return


def CameraWu_acapture_test():
    mt.get_function_name(ack=True, tabs=0)
    CameraWu_test(type_cam='acapture')
    return


def CameraWu_imutils_test():
    mt.get_function_name(ack=True, tabs=0)
    CameraWu_test(type_cam='imutils')
    return


def classify(m: (cvt.yolov3_coco, any), cv_img: np.array, img_title: str, fps_classify: mt.FPS) -> np.array:
    cv2.putText(cv_img, text=img_title, org=(0, 10), fontFace=2, fontScale=0.5,
                color=pyplt.get_BGR_color('blue'))

    fps_classify.start()
    detections = m.classify_cv_img(
        cv_img=cv_img,
        fp=3,
        ack=False,
        tabs=1,
        title=img_title,
    )
    detections = m.add_traffic_light_to_detections(
        detections,
        traffic_light_p={
            'up': 0.2,
            'mid': 0.3,
            'down': 0.4
        }
    )
    detections = m.add_sub_sub_image_to_detection(
        detections,
        cv_img=cv_img,
        bbox_image_p={
            'x_start': 0.2,
            'x_end': 0.8,
            'y_start': 1,
            'y_end': 0.5,
        },
    )
    fps_classify.update(ack_progress=True, tabs=1)

    m.draw_detections(
        detections,
        # colors_d=tflt.ssd_mobilenet_coco.DEFAULT_COLOR_D,
        colors_d={
            'bbox': pyplt.get_BGR_color('r'),
            'label_bbox': pyplt.get_BGR_color('black'),
            'text': pyplt.get_BGR_color('white'),
            'sub_image': pyplt.get_BGR_color('blue'),
            'person_bbox': pyplt.get_BGR_color('lightgreen'),
        },
        cv_img=cv_img,
        draw_labels=True,
        ack=True,
        tabs=1,
        title=img_title,
    )

    return cv_img


def model_image_list_test(model: (cvt.yolov3_coco, any), delay_secs: (int, None)):
    """
    :param model:
    :param delay_secs: if None - no delay
    images_list_list: list of list of paths of images.
        works much nicer if each list is sorted as frames for a movie like folder.
        also independent images are ok
        ASSUMES all list of the same size
        dimensions will be fixed to 640,480  # not mandatory - just need one size for all
    :return:
    """
    f1 = './{}1'.format(mtt.TEMP_FOLDER_NAME)
    f2 = './{}2'.format(mtt.TEMP_FOLDER_NAME)
    mt.create_dir(f1)
    mt.create_dir(f2)
    for url in mtt.TEMP_IMAGE_COCO_URLS:
        st.download_file(url, '{}/{}'.format(f1, os.path.basename(url.split('?')[0]), tabs=1))
    for url in mtt.TEMP_IMAGE_COCO_URLS2:
        st.download_file(url, '{}/{}'.format(f2, os.path.basename(url.split('?')[0]), tabs=1))

    folder_imgs = mt.find_files_in_folder(f1, file_suffix='.jpg', ack=True)
    folder_imgs2 = mt.find_files_in_folder(f2, file_suffix='.jpg', ack=True)
    images_list_list = [folder_imgs, folder_imgs2]
    delay_ms = delay_secs * 1000 if delay_secs is not None else 1
    # assumes all port has same amount - take first
    total_round = len(images_list_list[0])

    fps_classify = mt.FPS(summary_title='classification')
    fps_rounds = mt.FPS(summary_title='rounds')
    for i in range(total_round):
        fps_rounds.start()
        cv_imgs = []
        for images_list in images_list_list:
            full_img_path = images_list[i]
            cv_img = cv2.imread(full_img_path)
            if cv_img.shape[0] != 480 or cv_img.shape[1] != 640:
                cv_img = cv2.resize(cv_img, (640, 480), interpolation=cv2.INTER_AREA)
            img_t = os.path.basename(full_img_path)
            cv_img = classify(
                m=model,
                cv_img=cv_img,
                img_title='{} on image {}/{} - {}'.format(model.name, i + 1, total_round, img_t),
                fps_classify=fps_classify
            )
            cv_imgs.append(cv_img)
        cvt.display_open_cv_images(
            cv_imgs,
            ms=delay_ms,
            title='{} on {} folders'.format(model.name, len(images_list_list)),
            loc=None if i > 0 else pyplt.Location.CENTER_CENTER.value,
            resize=None,
            grid=(1, len(images_list_list))
        )
        fps_rounds.update()

    cv2.destroyAllWindows()
    fps_classify.finalize(tabs=1)
    fps_rounds.finalize(tabs=1)
    mt.delete_dir_with_files(f1)
    mt.delete_dir_with_files(f2)
    return


def model_web_cam_test(model: (cvt.yolov3_coco, any), ports: list, frames: int, delay_secs: (int, None)):
    """
    :param model:
    :param ports:
    :param frames:
    :param delay_secs: if None - no delay
    :return:
    """
    delay_ms = delay_secs * 1000 if delay_secs is not None else 1
    cams = []
    valid_cams = []
    for port in ports:
        cam = cvt.CameraWu.open_camera(port=port, type_cam='cv2')
        if cam is not None:
            cams.append(cam)
            valid_cams.append(port)
    if len(valid_cams) == 0:
        mt.exception_error('\tfailed to open any camera from ports {}'.format(ports))
        return
    fps_classify = mt.FPS(summary_title='classification')
    fps_rounds = mt.FPS(summary_title='rounds')
    for i in range(frames):
        fps_rounds.start()
        cv_imgs = []
        for cam in cams:
            success, cv_img = cam.read_img()
            if success:
                img_t = mt.get_time_stamp()
                cv_img = classify(
                    m=model,
                    cv_img=cv_img,
                    img_title='{} on cam {} image {}/{} - {}'.format(model.name, cam.port, i + 1, frames, img_t),
                    fps_classify=fps_classify
                )
                cv_imgs.append(cv_img)
        if len(cv_imgs) > 0:
            cvt.display_open_cv_images(
                cv_imgs,
                ms=delay_ms,
                title='{} on cams {}'.format(model.name, valid_cams),
                loc=None if i > 0 else pyplt.Location.CENTER_CENTER.value,
                resize=None,
                grid=(1, len(cams))
            )
        fps_rounds.update()

    cv2.destroyAllWindows()
    fps_classify.finalize(tabs=1)
    fps_rounds.finalize(tabs=1)
    return


def test_models_images_list():
    mt.get_function_name(ack=True, tabs=0)
    models = cvt.yolov3_coco.MODEL_CONF.keys()

    for m_name in models:
        save_dir = '{}/{}'.format(mtt.TEMP_MODEL_PATH, m_name)

        m = cvt.yolov3_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            tabs=1,
        )
        print(m)
        # delay None - good for measuring FPS
        model_image_list_test(model=m, delay_secs=MODEL_DELAY_FOLDER)
    return


def test_models_cameras():
    mt.get_function_name(ack=True, tabs=0)
    models = cvt.yolov3_coco.MODEL_CONF.keys()

    for m_name in models:
        save_dir = '{}/{}'.format(mtt.TEMP_MODEL_PATH, m_name)

        m = cvt.yolov3_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            tabs=1,
        )
        print(m)
        # delay None - good for measuring FPS
        model_web_cam_test(model=m, ports=[0, 1], frames=MODEL_FRAMES_CAM, delay_secs=MODEL_DELAY_CAM)
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    get_cv_version_test()
    imread_imwrite_test()
    list_to_cv_image_test()
    display_open_cv_image_test()
    display_open_cv_image_loop_test()
    resize_opencv_image_test()
    move_cv_img_x_y_test()
    move_cv_img_by_str_test()
    unpack_list_imgs_to_big_image_test()
    display_open_cv_images_test()
    display_open_cv_images_loop_test()
    gray_to_BGR_and_back_test()
    BGR_img_to_RGB_and_back_test()
    CameraWu_cv2_test()
    CameraWu_acapture_test()
    CameraWu_imutils_test()
    test_models_images_list()
    test_models_cameras()
    print('{}'.format('-' * 20))
    return
