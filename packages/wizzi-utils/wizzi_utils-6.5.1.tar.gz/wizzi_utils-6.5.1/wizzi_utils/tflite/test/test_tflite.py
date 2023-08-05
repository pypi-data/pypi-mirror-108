from wizzi_utils.tflite import tflite_tools as tflt
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv.test import test_open_cv_tools as cvtt
from wizzi_utils.socket import socket_tools as st
import os


def get_tflite_version_test():
    mt.get_function_name(ack=True, tabs=0)
    tflt.get_tflite_version(ack=True)
    return


def test_models_images_list():
    """
    works much nicer if the images are frames from a movie.
        also independent images are ok
    :return:
    """
    mt.get_function_name(ack=True, tabs=0)
    mt.create_dir(mtt.TEMP_FOLDER_PATH)
    for url in mtt.TEMP_IMAGE_COCO_URLS:
        st.download_file(url, '{}/{}'.format(mtt.TEMP_FOLDER_PATH, os.path.basename(url.split('?')[0]), tabs=1))

    folder_imgs = mt.find_files_in_folder(mtt.TEMP_FOLDER_PATH, file_suffix='.jpg', ack=True)

    # models = tflt.ssd_mobilenet_coco.MODEL_CONF.keys()
    # models = [
    #     'ssd_mobilenet_v3_small_coco_2020_01_14',
    #     'ssd_mobilenet_v2_mnasfpn_shared_box_predictor_320x320_coco_sync_2020_05_18',
    #     'ssd_mobilenet_v3_large_coco_2020_01_14',
    #     'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
    #     'ssd_mobilenet_v1_1_metadata_1',
    #     'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
    #     'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    # ]
    models = ['ssd_mobilenet_v3_small_coco_2020_01_14']

    for m_name in models:  # delay None - good for measuring FPS
        # model_image_list_test(model_name=m_name, images_list=['./test_img.jpg', './test_img2.jpg'], delay_secs=None)
        save_dir = mtt.TEMP_MODEL_PATH

        m = tflt.ssd_mobilenet_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            tabs=1,
        )
        print(m)
        cvtt.model_image_list_test(model=m, images_list=folder_imgs, delay_secs=cvtt.MODEL_DELAY_FOLDER)

    mt.delete_dir_with_files(mtt.TEMP_FOLDER_PATH)
    return


def test_models_cameras():
    mt.get_function_name(ack=True, tabs=0)

    # models = tflt.ssd_mobilenet_coco.MODEL_CONF.keys()
    # models = [
    #     'ssd_mobilenet_v3_small_coco_2020_01_14',
    #     'ssd_mobilenet_v2_mnasfpn_shared_box_predictor_320x320_coco_sync_2020_05_18',
    #     'ssd_mobilenet_v3_large_coco_2020_01_14',
    #     'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
    #     'ssd_mobilenet_v1_1_metadata_1',
    #     'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
    #     'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    # ]
    models = ['ssd_mobilenet_v3_small_coco_2020_01_14']

    for m_name in models:  # set frames and delay and enjoy
        save_dir = mtt.TEMP_MODEL_PATH

        m = tflt.ssd_mobilenet_coco(
            save_load_dir=save_dir,
            model_name=m_name,
            threshold=0.5,
            tabs=1,
        )
        print(m)
        cvtt.model_web_cam_test(model=m, ports=[0], frames=cvtt.MODEL_FRAMES_CAM, delay_secs=cvtt.MODEL_DELAY_CAM)
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    get_tflite_version_test()
    test_models_images_list()
    test_models_cameras()
    print('{}'.format('-' * 20))
    return
