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
ITERS_CAM_TEST = 100  # 0 to block
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
    try:
        cam = cvt.CameraWu(port=0, type_cam=type_cam)
    except ModuleNotFoundError:
        print('\tCan\'t complete tests due to import issues')
        return

    times_ti = []
    for i in range(ITERS_CAM_TEST):
        round_timer = mt.get_timer()
        success, cv_img = cam.read_img()
        if WITH_SLEEP:
            mt.sleep(1)

        if success:
            cvt.display_open_cv_image(
                img=cv_img,
                ms=1,
                title='CameraWu_test {}'.format(type_cam),
                loc=pyplt.Location.CENTER_CENTER,
                resize=None,
            )
        times_ti.append(mt.get_timer() - round_timer)
    cv2.destroyAllWindows()
    # mt.delete_dir_with_files(save_dir)
    print('\ttype_cam {}:'.format(type_cam))
    st.rounds_summary(times_ti, tabs=1)
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


def classify(m: (cvt.yolov3_coco, any), cv_img: np.array, img_title: str, cv_title: str, delay_ms: int,
             loc: str, fps_classify: mt.FPS) -> None:
    cv_img_orig = np.copy(cv_img)
    cv2.putText(cv_img_orig, text=img_title, org=(0, 10), fontFace=2, fontScale=0.5,
                color=pyplt.get_BGR_color('blue'))
    # classify_timer_begin = mt.get_timer()
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

    cvt.display_open_cv_images(
        [cv_img_orig, cv_img],
        ms=delay_ms,
        title=cv_title,
        loc=loc,
        resize=None,
        grid=(1, 2)
    )

    return


def model_image_list_test(model: (cvt.yolov3_coco, any), images_list: list, delay_secs: (int, None)):
    """
    :param model:
    :param images_list: paths of images. works much nicer if the images are frames from a movie.
        also independent images are ok
    :param delay_secs: if None - no delay
    :return:
    """
    delay_ms = delay_secs * 1000 if delay_secs is not None else 1
    fps_classify = mt.FPS(summary_title='classification')
    fps_rounds = mt.FPS(summary_title='rounds')
    for i, img_path in enumerate(images_list):
        fps_rounds.start()
        # round_timer_begin = mt.get_timer()
        cv_img = cvt.load_img(path=img_path, ack=True, tabs=1)
        classify(
            m=model,
            cv_img=cv_img,
            img_title='{} on image {}'.format(model.name, os.path.basename(img_path)),
            cv_title='{} detections'.format(model.name),
            delay_ms=delay_ms,
            loc=None if i > 0 else pyplt.Location.TOP_LEFT.value,
            fps_classify=fps_classify
        )
        fps_rounds.update()

    cv2.destroyAllWindows()
    fps_classify.finalize(tabs=1)
    fps_rounds.finalize(tabs=1)
    return


def model_web_cam_test(model: (cvt.yolov3_coco, any), ports: list, frames: int, delay_secs: (int, None)):
    """
    :param model:
    :param ports:
    :param frames:
    :param delay_secs: if None - no delay
    :return:
    """
    cams = []
    for port in ports:
        cam = cvt.CameraWu(port=port, type_cam='cv2')
        cams.append(cam)

    fps_classify = mt.FPS(summary_title='classification({} cams work)'.format(len(cams)))
    fps_rounds = mt.FPS(summary_title='rounds({} cams work)'.format(len(cams)))
    delay_ms = delay_secs * 1000 if delay_secs is not None else 1
    locations = pyplt.Location.get_location_list_by_cols()
    for i in range(frames):
        fps_rounds.start()
        for cam in cams:
            success, cv_img = cam.read_img()
            classify(
                m=model,
                cv_img=cv_img,
                img_title='{} on cam {} image {}/{}'.format(model.name, cam.port, i + 1, frames),
                cv_title='{} on cam {}'.format(model.name, cam.port),
                delay_ms=delay_ms,
                loc=None if i > 0 else locations[cam.port % len(locations)],
                fps_classify=fps_classify
            )
        fps_rounds.update()
    cv2.destroyAllWindows()
    fps_classify.finalize(tabs=1)
    fps_rounds.finalize(tabs=1)
    return


def test_models_images_list():
    mt.get_function_name(ack=True, tabs=0)
    mt.create_dir(mtt.TEMP_FOLDER_PATH)
    for url in mtt.TEMP_IMAGE_COCO_URLS:
        st.download_file(url, '{}/{}'.format(mtt.TEMP_FOLDER_PATH, os.path.basename(url.split('?')[0]), tabs=1))

    folder_imgs = mt.find_files_in_folder(mtt.TEMP_FOLDER_PATH, file_suffix='.jpg', ack=True)

    models = cvt.yolov3_coco.MODEL_CONF.keys()

    for m_name in models:  # delay None - good for measuring FPS
        # model_image_list_test(model_name=m_name, images_list=['./test_img.jpg', './test_img2.jpg'], delay_secs=None)
        save_dir = '{}/{}'.format(mtt.TEMP_MODEL_PATH, m_name)

        m = cvt.yolov3_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            tabs=1,
        )
        print(m)
        model_image_list_test(model=m, images_list=folder_imgs, delay_secs=MODEL_DELAY_FOLDER)

    mt.delete_dir_with_files(mtt.TEMP_FOLDER_PATH)
    return


def test_models_cameras():
    mt.get_function_name(ack=True, tabs=0)

    models = cvt.yolov3_coco.MODEL_CONF.keys()

    for m_name in models:  # delay None - good for measuring FPS
        # model_image_list_test(model_name=m_name, images_list=['./test_img.jpg', './test_img2.jpg'], delay_secs=None)
        save_dir = '{}/{}'.format(mtt.TEMP_MODEL_PATH, m_name)

        m = cvt.yolov3_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            tabs=1,
        )
        print(m)
        model_web_cam_test(model=m, ports=[0], frames=MODEL_FRAMES_CAM, delay_secs=MODEL_DELAY_CAM)
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
