import os
import time
import logging

logger = logging.getLogger(__name__)


def borderRemove(image_path):
    # print("Remove border executed: ", image_path)
    logger.info(' * REMOVING BORDERS IN IMAGE *')
    if os.name == "nt":
        cmd_str = 'convert {} -type Grayscale -negate -define morphology:compose=darken -morphology Thinning "Rectangle:1x80+0+0<" -negate {}'.format(image_path, image_path)
        os.system(cmd_str)

    else:
        cmd = "convert {} -type Grayscale -negate -define morphology:compose=darken -morphology Thinning 'Rectangle:1x80+0+0<' -negate {}".format(image_path, image_path)
        os.system(cmd)
        # time.sleep(7)
    logger.info('Image borders removed: {}'.format(image_path))
    return image_path
