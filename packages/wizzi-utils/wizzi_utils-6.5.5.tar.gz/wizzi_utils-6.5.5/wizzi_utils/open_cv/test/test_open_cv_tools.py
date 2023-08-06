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
BLOCK_MS_NORMAL = 2000  # 0 to block
ITERS_CAM_TEST = 10  # 0 to block
MODEL_FRAMES_CAM = 10


def load_img_from_web(name: str) -> np.array:
    f = mtt.IMAGES_INPUTS
    url = mtt.IMAGES_D[name]
    suffix = 'jpg'  # default
    # if '.webm' in url:
    #     suffix = 'webm'
    dst = '{}/{}.{}'.format(f, name, suffix)

    if not os.path.exists(dst):
        if not os.path.exists(f):
            mt.create_dir(f)
        success = st.download_file(url, dst)
        if not success:
            mt.exception_error('download failed - creating random img')
            img = mt.np_random_integers(size=(240, 320, 3), low=0, high=255)
            img = img.astype('uint8')
            cvt.save_img(dst, img)

    img = cvt.load_img(path=dst)
    return img


def get_vid_from_web(name: str) -> str:
    f = mtt.VIDEOS_INPUTS
    url = mtt.VIDEOS_D[name]
    suffix = 'mp4'  # default
    if '.webm' in url:
        suffix = 'webm'
    dst = '{}/{}.{}'.format(f, name, suffix)

    if not os.path.exists(dst):
        if not os.path.exists(f):
            mt.create_dir(f)
        success = st.download_file(url, dst)
        if not success:
            mt.exception_error('download failed - creating random img')
            dst = None

    return dst


def get_cv_version_test():
    mt.get_function_name(ack=True, tabs=0)
    cvt.get_cv_version(ack=True, tabs=1)
    return


def imread_imwrite_test():
    mt.get_function_name(ack=True, tabs=0)
    name = mtt.SO_LOGO
    img = load_img_from_web(name)

    f = mtt.IMAGES_INPUTS
    url = mtt.IMAGES_D[name]
    dst_path = '{}/{}'.format(f, os.path.basename(url).replace('.png', '_copy.png'))

    cvt.save_img(dst_path, img, ack=True)
    img_loaded = cvt.load_img(dst_path, ack=True)
    print(mt.to_str(img_loaded, '\timg_copy'))
    mt.delete_file(dst_path, ack=True)
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def list_to_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    img_list = img.tolist()
    print(mt.to_str(img_list, '\timg_list'))
    img = cvt.list_to_cv_image(img_list)
    print(mt.to_str(img, '\timg'))
    # mt.delete_file(file=mtt.TEMP_IMAGE_PATH, ack=True)
    return


def display_open_cv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
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
        ms=BLOCK_MS_NORMAL,  # blocking
        title='stack overflow logo moved to {} and re-sized to {}'.format(loc, resize),
        loc=loc,  # start from x =70 y = 0
        resize=resize
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def display_open_cv_image_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
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
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def resize_opencv_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    print(mt.to_str(img, '\timg'))
    img = cvt.resize_opencv_image(img, scale_percent=0.6)
    print(mt.to_str(img, '\timg re-sized to 60%'))
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def move_cv_img_x_y_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    options = [(0, 0), (100, 0), (0, 100), (150, 150), (400, 400), (250, 350)]
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for x_y in options:
        title = 'move to ({})'.format(x_y)
        cv2.imshow(title, img)
        cvt.move_cv_img_x_y(title, x_y)
    cv2.waitKey(BLOCK_MS_NORMAL)
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def move_cv_img_by_str_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    options = pyplt.Location.get_location_list_by_rows()
    print('\tVisual test: move to all options {}'.format(options))
    print('\t\tClick Esc to close all')
    for where_to in options:
        title = 'move to {}'.format(where_to)
        cv2.imshow(title, img)
        cvt.move_cv_img_by_str(img, title, where=where_to)
    cv2.waitKey(BLOCK_MS_NORMAL)
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def unpack_list_imgs_to_big_image_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
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
        ms=BLOCK_MS_NORMAL,  # blocking
        title=title,
        loc=(0, 0),
        resize=None
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def display_open_cv_images_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    title = '2x1 grid'
    print('\tVisual test: {}'.format(title))
    loc1 = (0, 0)
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=1,  # blocking
        title='{} loc={}'.format(title, loc1),
        loc=loc1,
        resize=None,
        grid=(2, 1),
        header='{} loc={}'.format(title, loc1),
    )
    loc2 = pyplt.Location.BOTTOM_CENTER.value
    cvt.display_open_cv_images(
        imgs=[img, img],
        ms=BLOCK_MS_NORMAL,  # blocking
        title='{} loc={}'.format(title, loc2),
        loc=loc2,
        resize=None,
        grid=(2, 1),
        header='{} loc={}'.format(title, loc1),
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def display_open_cv_images_loop_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
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
            grid=(2, 1),
            header=None
        )
        if i == 0:  # move just first iter
            loc = None
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def gray_to_BGR_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.SO_LOGO)
    print(mt.to_str(img, '\timgRGB'))
    gray = cvt.BGR_img_to_gray(img)
    print(mt.to_str(img, '\timg_gray'))
    img = cvt.gray_scale_img_to_BGR_form(gray)
    print(mt.to_str(img, '\timgRGB'))
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
    return


def BGR_img_to_RGB_and_back_test():
    mt.get_function_name(ack=True, tabs=0)
    imgBGR1 = load_img_from_web(mtt.SO_LOGO)
    print(mt.to_str(imgBGR1, '\timgBGR'))
    imgRGB = cvt.BGR_img_to_RGB(imgBGR1)
    print(mt.to_str(imgRGB, '\timgRGB'))
    imgBGR2 = cvt.RGB_img_to_BGR(imgRGB)
    print(mt.to_str(imgBGR2, '\timgBGR2'))

    cvt.display_open_cv_images(
        imgs=[imgBGR1, imgRGB, imgBGR2],
        ms=BLOCK_MS_NORMAL,  # blocking
        title='imgBGR1, imgRGB, imgBGR2',
        loc=pyplt.Location.CENTER_CENTER,
        resize=None,
        grid=(3, 1),
        header='compare'
    )
    cv2.destroyAllWindows()
    # mt.delete_file(file=mtt.SO_LOGO_PATH, ack=True)
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
                    header='{}/{}'.format(i + 1, ITERS_CAM_TEST)
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


def __classify(m: (cvt.dnn_models, any), cv_img: np.array, img_title: str, fps_classify: mt.FPS) -> np.array:
    """
    AUX function
    :param m:
    :param cv_img:
    :param img_title:
    :param fps_classify:
    :return:
    """
    cvt.add_header(cv_img, header=img_title, bg_font_scale=2)
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
            'bbox': 'r',
            'label_bbox': 'black',
            'text': 'white',
            'sub_image': 'blue',
            'person_bbox': 'lightgreen',
            'dog_bbox': 'lightblue',
        },
        cv_img=cv_img,
        draw_labels=True,
        ack=True,
        tabs=1,
        title=img_title,
    )

    return cv_img


def __model_images_lists_test(model: (cvt.dnn_models, any), delay_ms: int, display_im_size: tuple):
    """
    AUX function
    :param model:
    :param delay_ms: 0 to block
    images_list_list: list of list of paths of images.
        works much nicer if each list is sorted as frames for a movie like folder.
        also independent images are ok
        ASSUMES all list of the same size
        dimensions will be fixed to 640,480  # not mandatory - just need one size for all
    :return:
    """
    resources_f1 = [mtt.KITE, mtt.GIRAFFE, mtt.HORSES]
    resources_f2 = [mtt.DOG, mtt.EAGLE, mtt.PERSON]
    resources = resources_f1 + resources_f2
    for res in resources:
        _ = load_img_from_web(res)
    # create 2 dirs
    f1 = mtt.TEMP_FOLDER1

    for f1_name in resources_f1:
        target_fp = '{}/{}.jpg'.format(f1, f1_name)
        if not os.path.exists(target_fp):
            if not os.path.exists(f1):
                mt.create_dir(f1, ack=True)
            mt.copy_file(file_src='{}/{}.jpg'.format(mtt.IMAGES_INPUTS, f1_name), file_dst=target_fp)

    f2 = mtt.TEMP_FOLDER2
    for f2_name in resources_f2:
        target_fp = '{}/{}.jpg'.format(f2, f2_name)
        if not os.path.exists(target_fp):
            if not os.path.exists(f2):
                mt.create_dir(f2, ack=True)
            mt.copy_file(file_src='{}/{}.jpg'.format(mtt.IMAGES_INPUTS, f2_name), file_dst=target_fp)

    folder_imgs = mt.find_files_in_folder(f1, file_suffix='.jpg', ack=True)
    folder_imgs2 = mt.find_files_in_folder(f2, file_suffix='.jpg', ack=True)
    images_list_list = [folder_imgs, folder_imgs2]

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
            img_t = os.path.basename(full_img_path)
            cv_img = __classify(
                m=model,
                cv_img=cv_img,
                img_title='image {}/{} - {}'.format(i + 1, total_round, img_t),
                fps_classify=fps_classify
            )
            cv_img = cv2.resize(cv_img, display_im_size, interpolation=cv2.INTER_AREA)
            cv_imgs.append(cv_img)
        cvt.display_open_cv_images(
            cv_imgs,
            ms=delay_ms,
            title='{} on {} folders'.format(model.name, len(images_list_list)),
            loc=None if i > 0 else pyplt.Location.CENTER_CENTER.value,
            resize=None,
            grid=(1, len(images_list_list)),
            header=None
        )
        fps_rounds.update()

    cv2.destroyAllWindows()
    fps_classify.finalize(tabs=1)
    fps_rounds.finalize(tabs=1)
    mt.delete_dir_with_files(f1)
    mt.delete_dir_with_files(f2)
    return


def __model_video_test(model: (cvt.dnn_models, any), delay_ms: int, display_im_size: tuple):
    """
    AUX FUNCTION
    :param model:
    :param delay_ms:
    :return:
    """
    __models_video_test(models=[model], grid=(1, 1), delay_ms=delay_ms, display_im_size=display_im_size)
    return


def __model_web_cam_test(model: (cvt.dnn_models, any), ports: list, frames: int,
                         delay_ms: int, display_im_size: tuple):
    """
    AUX function
    :param model:
    :param ports:
    :param frames:
    :param delay_ms: if None - no delay
    :return:
    """
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
                cv_img = __classify(
                    m=model,
                    cv_img=cv_img,
                    img_title='image {}/{} - {}'.format(i + 1, frames, img_t),
                    fps_classify=fps_classify
                )
                cv_img = cv2.resize(cv_img, display_im_size, interpolation=cv2.INTER_AREA)
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


def __models_images_test(models: list, grid: tuple, delay_ms: int, scope: str, display_im_size: tuple):
    """
    AUX FUNCTION
    :param models:
    :param grid:
    :param delay_ms:
    :param scope:
    :param display_im_size:
    :return:
    """
    # Prepare cv images list
    images_names = [mtt.DOGS1, mtt.PERSON]
    cv_imgs_orig = [load_img_from_web(image_name) for image_name in images_names]

    for cv_img, img_name in zip(cv_imgs_orig, images_names):
        cv_img_per_model = []
        for model in models:
            cv_img_clone = cv_img.copy()

            detections = model.classify_cv_img(cv_img=cv_img_clone)
            # detections = model.add_traffic_light_to_detections(
            #     detections,
            #     traffic_light_p={
            #         'up': 0.2,
            #         'mid': 0.3,
            #         'down': 0.4
            #     }
            # )
            # detections = model.add_sub_sub_image_to_detection(
            #     detections,
            #     cv_img=cv_img_clone,
            #     bbox_image_p={
            #         'x_start': 0.2,
            #         'x_end': 0.8,
            #         'y_start': 1,
            #         'y_end': 0.5,
            #     },
            # )
            cvt.add_header(cv_img_clone, header=model.name, bg_font_scale=1)
            model.draw_detections(
                detections,
                # colors_d=tflt.ssd_mobilenet_coco.DEFAULT_COLOR_D,
                colors_d={
                    'bbox': 'r',
                    'label_bbox': 'black',
                    'text': 'white',
                    'sub_image': 'blue',
                    'person_bbox': 'lightgreen',
                    'dog_bbox': 'lightblue',
                },
                cv_img=cv_img_clone,
                draw_labels=True,
                ack=True,
                tabs=1,
                title='{} on {}'.format(model.name, img_name),
            )
            cv_img_clone = cv2.resize(cv_img_clone, display_im_size, interpolation=cv2.INTER_AREA)
            cv_img_per_model.append(cv_img_clone)
        save_path = '{}/models_compare_images_test/{}/{}.jpg'.format(mtt.IMAGES_OUTPUTS, scope, img_name)
        mt.create_dir(os.path.dirname(save_path))
        cvt.display_open_cv_images(
            cv_img_per_model,
            ms=delay_ms,
            title='{}'.format(img_name),
            loc=pyplt.Location.CENTER_CENTER.value,
            resize=None,
            grid=grid,
            header=None,
            save_path=save_path
        )
        cv2.destroyAllWindows()
    return


def __models_video_test(models: list, grid: tuple, delay_ms: int, display_im_size: tuple):
    """
    AUX FUNCTION
    :param models:
    :param grid:
    :param delay_ms:
    :param display_im_size:
    :return:
    """
    # video_path = '{}/vids/Dogs_Playing_on_Field.mp4'.format(mtt.PLAY_GROUND)
    # video_path = '{}/vids/Dogs_Tested.mp4'.format(mtt.PLAY_GROUND)
    vid_name = mtt.DOG1
    video_path = get_vid_from_web(name=vid_name)
    # vid_name = 'vid2'
    # video_path = '{}/{}.mp4'.format(mtt.VIDEOS_INPUTS, vid_name)

    if not os.path.exists(video_path):
        mt.exception_error(mt.NOT_FOUND.format(video_path))
        return
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        video_total_frames = cvt.get_frames_from_cap(cap)
        print('\tvid {} has {} frames'.format(vid_name, video_total_frames))
    else:
        mt.exception_error('cap is closed.')
        return

    fps_classify = mt.FPS(summary_title='classification')
    for i in range(video_total_frames):
        success, cv_img = cap.read()
        if i % int(video_total_frames / 10) != 0:  # s
            # do only 10 frames
            continue
        print('\tframe {}/{}:'.format(i + 1, video_total_frames))
        if success:
            cv_img_per_model = []
            for model in models:
                cv_img_clone = cv_img.copy()
                fps_classify.start()
                detections = model.classify_cv_img(cv_img=cv_img_clone)
                fps_classify.update(ack_progress=True, tabs=2)
                # detections = model.add_traffic_light_to_detections(
                #     detections,
                #     traffic_light_p={
                #         'up': 0.2,
                #         'mid': 0.3,
                #         'down': 0.4
                #     }
                # )
                # detections = model.add_sub_sub_image_to_detection(
                #     detections,
                #     cv_img=cv_img_clone,
                #     bbox_image_p={
                #         'x_start': 0.2,
                #         'x_end': 0.8,
                #         'y_start': 1,
                #         'y_end': 0.5,
                #     },
                # )
                cvt.add_header(cv_img_clone,
                               header='{} on image {}/{}'.format(model.name, i + 1, video_total_frames),
                               bg_font_scale=2)
                model.draw_detections(
                    detections,
                    # colors_d=tflt.ssd_mobilenet_coco.DEFAULT_COLOR_D,
                    colors_d={
                        'bbox': 'r',
                        'label_bbox': 'black',
                        'text': 'white',
                        'sub_image': 'blue',
                        'person_bbox': 'lightgreen',
                        'dog_bbox': 'lightblue',
                    },
                    cv_img=cv_img_clone,
                    draw_labels=True,
                    ack=True,
                    tabs=2,
                    title='{} on image {}/{}'.format(model.name, i + 1, video_total_frames),
                )
                cv_img_clone = cv2.resize(cv_img_clone, display_im_size, interpolation=cv2.INTER_AREA)
                cv_img_per_model.append(cv_img_clone)

            cvt.display_open_cv_images(
                cv_img_per_model,
                ms=delay_ms,
                title=video_path,
                loc=pyplt.Location.CENTER_CENTER.value,
                resize=None,
                grid=grid,
                header=None,
                save_path=None
            )
    cv2.destroyAllWindows()
    return


def models_images_lists_test():
    mt.get_function_name(ack=True, tabs=0)
    # models = cvt.yolov3_coco.MODEL_CONF.keys()
    # models = [
    #     'yolov3',
    #     'yolov3_tiny',
    #     'yolov3-ssp',
    # ]
    models = ['yolov3']

    for m_name in models:
        save_dir = '{}/{}/{}'.format(mtt.CV2_MODELS, cvt.dnn_models.MODEL_CONF[m_name]['family'], m_name)

        m = cvt.dnn_models(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        # delay None - good for measuring FPS
        __model_images_lists_test(model=m, delay_ms=BLOCK_MS_NORMAL, display_im_size=(640, 480))
    return


def models_video_test():
    mt.get_function_name(ack=True, tabs=0)
    # models = cvt.yolov3_coco.MODEL_CONF.keys()
    # models = [
    #     'yolov3',
    #     'yolov3_tiny',
    #     'yolov3-ssp',
    # ]
    models = ['yolov3']

    for m_name in models:
        save_dir = '{}/{}/{}'.format(mtt.CV2_MODELS, cvt.dnn_models.MODEL_CONF[m_name]['family'], m_name)

        m = cvt.dnn_models(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        # delay None - good for measuring FPS
        __model_video_test(model=m, delay_ms=1, display_im_size=(640, 480))
    return


def models_cameras_test():
    mt.get_function_name(ack=True, tabs=0)
    # models = cvt.yolov3_coco.MODEL_CONF.keys()
    # models = [
    #     'yolov3',
    #     'yolov3_tiny',
    #     'yolov3-ssp',
    # ]
    models = ['yolov3']
    for m_name in models:
        save_dir = '{}/{}/{}'.format(mtt.CV2_MODELS, cvt.dnn_models.MODEL_CONF[m_name]['family'], m_name)

        m = cvt.dnn_models(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        # delay None - good for measuring FPS
        __model_web_cam_test(model=m, ports=[0, 1],
                             frames=MODEL_FRAMES_CAM, delay_ms=1,
                             display_im_size=(640, 480))
    return


def models_compare_images_test():
    mt.get_function_name(ack=True, tabs=0)

    # Prepare models to compare
    models_names = ['yolov3', 'yolov3_tiny', 'yolov3-ssp']
    models = []
    for m_name in models_names:
        save_dir = '{}/{}/{}'.format(mtt.CV2_MODELS, cvt.dnn_models.MODEL_CONF[m_name]['family'], m_name)
        m = cvt.dnn_models(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        models.append(m)

    __models_images_test(models, grid=(2, 2), delay_ms=BLOCK_MS_NORMAL, scope='cv2', display_im_size=(640, 480))
    return


def models_compare_video_test():
    mt.get_function_name(ack=True, tabs=0)

    # Prepare models to compare
    models_names = ['yolov3', 'yolov3_tiny', 'yolov3-ssp']
    models = []
    for m_name in models_names:
        save_dir = '{}/{}/{}'.format(mtt.CV2_MODELS, cvt.dnn_models.MODEL_CONF[m_name]['family'], m_name)
        m = cvt.dnn_models(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            # allowed_class=[  # if you care about specific classes
            #     'person',
            #     'dog'
            # ],
            tabs=1,
        )
        print(m)
        models.append(m)

    __models_video_test(models, grid=(2, 2), delay_ms=1, display_im_size=(640, 480))
    return


def add_text_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.HORSES)
    cvt.add_text(img, header='test text', pos=(100, 100), text_color='r', with_rect=True, bg_color='y', bg_font_scale=2)
    cvt.add_text(img, header='test text', pos=(100, 200), text_color='black', with_rect=True, bg_color='b',
                 bg_font_scale=1)
    cvt.display_open_cv_image(img, ms=BLOCK_MS_NORMAL, loc=pyplt.Location.CENTER_CENTER.value)
    cv2.destroyAllWindows()
    return


def add_header_test():
    mt.get_function_name(ack=True, tabs=0)
    img = load_img_from_web(mtt.HORSES)

    cvt.add_header(img, header='TOP_LEFT', loc=pyplt.Location.TOP_LEFT.value,
                   text_color='lime', with_rect=True, bg_color='azure', bg_font_scale=1)
    cvt.add_header(img, header='BOTTOM_LEFT', loc=pyplt.Location.BOTTOM_LEFT.value,
                   text_color='fuchsia', with_rect=True, bg_color='black', bg_font_scale=2)
    cvt.display_open_cv_image(img, ms=BLOCK_MS_NORMAL, loc=pyplt.Location.CENTER_CENTER.value)
    cv2.destroyAllWindows()

    img = load_img_from_web(mtt.DOG)
    cvt.display_open_cv_image(
        img,
        ms=BLOCK_MS_NORMAL,
        loc=pyplt.Location.CENTER_CENTER.value,
        header='direct header into display_open_cv_image'
    )
    cv2.destroyAllWindows()
    return


def Mp4_creator_test():
    mt.get_function_name(ack=True, tabs=0)
    # now open video file
    vid_name = mtt.DOG1
    video_path = get_vid_from_web(name=vid_name)

    if not os.path.exists(video_path):
        mt.exception_error(mt.NOT_FOUND.format(video_path))
        return
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        out_dims = cvt.get_dims_from_cap(cap)
        video_total_frames = cvt.get_frames_from_cap(cap)
        print('\tvid {} has {} frames'.format(vid_name, video_total_frames))
        print('\tvid size is {}'.format(out_dims))
    else:
        mt.exception_error('cap is closed.')
        return

    out_dir = '{}/create_mp4_test'.format(mtt.VIDEOS_OUTPUTS)
    mt.create_dir(out_dir)
    out_fp = '{}/{}_output.mp4'.format(out_dir, vid_name)

    mp4_creator = cvt.Mp4_creator(
        out_full_path=out_fp,
        out_fps=20.0,
        out_dims=out_dims
    )
    print(mp4_creator)

    for i in range(video_total_frames):
        success, frame = cap.read()
        if i % int(video_total_frames / 10) != 0:  # s
            # do only 10 frames
            continue
        print('\tframe {}/{}:'.format(i + 1, video_total_frames))
        # print('\t\t{}'.format(mt.to_str(frame)))
        if success:
            cvt.add_header(
                frame,
                header='create_mp4_test frame {}/{}'.format(i + 1, video_total_frames),
                loc=pyplt.Location.BOTTOM_LEFT.value,
                text_color=pyplt.get_random_color(),
                bg_color=pyplt.get_random_color(),
            )
            cvt.display_open_cv_image(frame, ms=1, title=vid_name, loc=None,
                                      header='{}/{}'.format(i + 1, video_total_frames))
            mp4_creator.add_frame(frame, ack=True, tabs=2)

    cap.release()
    mp4_creator.finalize()
    return


def readNetFromCaffe():
    """
    https://automaticaddison.com/how-to-detect-objects-in-video-using-mobilenet-ssd-in-opencv/
    raw example
    TODO next time search on google: cv2.dnn.readNetFromCaffe R-CNN
    opencv-mask-rcnn-cuda
    opencv-ssd-cuda
    :return:
    """
    # Project: How to Detect Objects in Video Using MobileNet SSD in OpenCV
    # Author: Addison Sears-Collins
    # Date created: March 1, 2021
    # Description: Object detection using OpenCV

    # filename = 'tf/edmonton_canada.mp4'
    # file_size = (1920, 1080)  # Assumes 1920x1080 mp4

    # start with loading model:
    m_name = 'MobileNetSSD_deploy'
    RESIZED_DIMENSIONS = (300, 300)  # Dimensions that SSD was trained on.
    IMG_NORM_RATIO = 0.007843  # In grayscale a pixel can range between 0 and 255
    classes = [
        "background", "aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
        "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"
    ]
    bbox_colors = np.random.uniform(255, 0, size=(len(classes), 3))
    caffe_model_dir = '{}/{}/{}'.format(mtt.CV2_MODELS, 'Caffe', m_name)

    neural_network = cv2.dnn.readNetFromCaffe(  # Load the pre-trained neural network
        '{}/{}.prototxt.txt'.format(caffe_model_dir, m_name),
        '{}/{}.caffemodel'.format(caffe_model_dir, m_name)
    )
    # neural_network.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    # neural_network.setPreferableBackend(cv2.dnn.DNN_TARGET_CUDA)

    # now open video file
    vid_name = mtt.DOG1
    video_path = get_vid_from_web(name=vid_name)
    # vid_name = 'vid2'
    # video_path = '{}/{}.mp4'.format(mtt.VIDEOS_INPUTS, vid_name)

    if not os.path.exists(video_path):
        mt.exception_error(mt.NOT_FOUND.format(video_path))
        return
    cap = cv2.VideoCapture(video_path)
    if cap.isOpened():
        out_dims = cvt.get_dims_from_cap(cap)
        video_total_frames = cvt.get_frames_from_cap(cap)
        print('\tvid {} has {} frames'.format(vid_name, video_total_frames))
        print('\tvid size is {}'.format(out_dims))
    else:
        mt.exception_error('cap is closed.')
        return

    out_dir = '{}/models_video_test/{}'.format(mtt.VIDEOS_OUTPUTS, m_name)
    mt.create_dir(out_dir)
    out_fp = '{}/{}_output.mp4'.format(out_dir, vid_name)
    print('\toutput will be saved to {}'.format(out_fp))
    output_frames_per_second = 20.0
    fourcc = cv2.VideoWriter_fourcc(c1='m', c2='p', c3='4', c4='v')

    result = cv2.VideoWriter(
        filename=out_fp,
        fourcc=fourcc,
        fps=output_frames_per_second,
        frameSize=out_dims
    )
    # Process the video
    for i in range(video_total_frames):
        success, frame = cap.read()
        if i % int(video_total_frames / 10) != 0:  # s
            # do only 10 frames
            continue
        print('\tframe {}/{}:'.format(i + 1, video_total_frames))
        # print('\t\t{}'.format(mt.to_str(frame)))
        if success:
            # Capture the frame's height and width
            (h, w) = frame.shape[:2]

            # Create a blob. A blob is a group of connected pixels in a binary
            # frame that share some common property (e.g. grayscale value)
            # Preprocess the frame to prepare it for deep learning classification
            frame_processed = cv2.resize(frame, RESIZED_DIMENSIONS)
            frame_blob = cv2.dnn.blobFromImage(frame_processed, scalefactor=IMG_NORM_RATIO, size=RESIZED_DIMENSIONS,
                                               mean=127.5)

            # Set the input for the neural network
            neural_network.setInput(frame_blob)

            # Predict the objects in the image
            neural_network_output = neural_network.forward()

            # Put the bounding boxes around the detected objects
            for res_ind in np.arange(0, neural_network_output.shape[2]):

                confidence = neural_network_output[0, 0, res_ind, 2]

                # Confidence must be at least 30%
                if confidence > 0.30:
                    idx = int(neural_network_output[0, 0, res_ind, 1])

                    bounding_box = neural_network_output[0, 0, res_ind, 3:7] * np.array([w, h, w, h])

                    (startX, startY, endX, endY) = bounding_box.astype("int")

                    label = "{}: {:.2f}%".format(classes[idx], confidence * 100)

                    cv2.rectangle(frame, (startX, startY), (endX, endY), bbox_colors[idx], 2)

                    y = startY - 15 if startY - 15 > 15 else startY + 15

                    cv2.putText(frame, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, bbox_colors[idx], 2)
                    print('\t\t{} {}'.format(label, idx))

            # Write the frame to the output video file
            cvt.display_open_cv_image(frame, ms=1, title=vid_name, loc=None,
                                      header='{}/{}'.format(i, video_total_frames))
            result.write(frame)
    cap.release()
    result.release()
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
    add_header_test()
    add_text_test()
    CameraWu_cv2_test()
    CameraWu_acapture_test()
    CameraWu_imutils_test()
    models_images_lists_test()
    models_video_test()
    models_cameras_test()
    models_compare_images_test()
    models_compare_video_test()
    print('{}'.format('-' * 20))
    return
