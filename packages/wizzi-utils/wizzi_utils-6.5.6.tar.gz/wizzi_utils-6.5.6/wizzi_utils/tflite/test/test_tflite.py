from wizzi_utils.tflite import tflite_tools as tflt
from wizzi_utils.misc import misc_tools as mt
from wizzi_utils.misc.test import test_misc_tools as mtt
from wizzi_utils.open_cv.test import test_open_cv_tools as cvtt


def get_tflite_version_test():
    mt.get_function_name(ack=True, tabs=0)
    tflt.get_tflite_version(ack=True)
    return


def models_images_lists_test():
    """
    works much nicer if the images are frames from a movie.
        also independent images are ok
    :return:
    """
    mt.get_function_name(ack=True, tabs=0)
    models = ['ssd_mobilenet_v3_small_coco_2020_01_14']
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

    for m_name in models:
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)

        m = tflt.ssd_mobilenet_coco(
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
        cvtt.__model_images_lists_test(model=m, delay_ms=cvtt.BLOCK_MS_NORMAL, display_im_size=(640, 480))
    return


def models_video_test():
    mt.get_function_name(ack=True, tabs=0)
    models = ['ssd_mobilenet_v3_small_coco_2020_01_14']
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

    for m_name in models:
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)

        m = tflt.ssd_mobilenet_coco(
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
        cvtt.__model_video_test(model=m, delay_ms=1, display_im_size=(640, 480))
    return


def models_cameras_test():
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

    for m_name in models:
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)

        m = tflt.ssd_mobilenet_coco(
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
        cvtt.__model_web_cam_test(model=m, ports=[0, 1], frames=cvtt.MODEL_FRAMES_CAM,
                                  delay_ms=1, display_im_size=(640, 480))
    return


def models_compare_images_test():
    mt.get_function_name(ack=True, tabs=0)

    # Prepare models to compare
    # models_names = tflt.ssd_mobilenet_coco.MODEL_CONF.keys()
    models_names = [
        'ssd_mobilenet_v3_small_coco_2020_01_14',
        'ssd_mobilenet_v2_mnasfpn_shared_box_predictor_320x320_coco_sync_2020_05_18',
        'ssd_mobilenet_v3_large_coco_2020_01_14',
        'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
        'ssd_mobilenet_v1_1_metadata_1',
        'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
        'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    ]
    # models_names = ['ssd_mobilenet_v3_small_coco_2020_01_14']

    models = []
    for m_name in models_names:
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)
        m = tflt.ssd_mobilenet_coco(
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

    cvtt.__models_images_test(models, grid=(3, 3), delay_ms=cvtt.BLOCK_MS_NORMAL, scope='tflt',
                              display_im_size=(480, 320))
    return


def models_compare_video_test():
    mt.get_function_name(ack=True, tabs=0)

    # Prepare models to compare
    # models_names = tflt.ssd_mobilenet_coco.MODEL_CONF.keys()
    models_names = [
        'ssd_mobilenet_v3_small_coco_2020_01_14',
        'ssd_mobilenet_v2_mnasfpn_shared_box_predictor_320x320_coco_sync_2020_05_18',
        'ssd_mobilenet_v3_large_coco_2020_01_14',
        'ssdlite_mobiledet_cpu_320x320_coco_2020_05_19',
        'ssd_mobilenet_v1_1_metadata_1',
        'ssdlite_mobilenet_v2_coco_300_integer_quant_with_postprocess',
        'coco_ssd_mobilenet_v1_1_0_quant_2018_06_29'
    ]
    # models_names = ['ssd_mobilenet_v3_small_coco_2020_01_14']
    models = []
    for m_name in models_names:
        save_dir = '{}/{}'.format(mtt.TFL_MODELS, m_name)
        m = tflt.ssd_mobilenet_coco(
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

    cvtt.__models_video_test(models, grid=(3, 3), delay_ms=1, display_im_size=(480, 320))
    return


def test_all():
    print('{}{}:'.format('-' * 5, mt.get_base_file_and_function_name()))
    get_tflite_version_test()
    models_images_lists_test()
    models_cameras_test()
    models_compare_images_test()
    models_compare_video_test()
    print('{}'.format('-' * 20))
    return
