import pytesseract
import cv2
import logging
import numpy as np


logger = logging.getLogger(__name__)


def getidtext(img):
    logger.info("Formatting id data...")
    # Load the Aadhar card image
    img = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    thresh = cv2.threshold(img, 123, 255, cv2.THRESH_BINARY_INV)[1]
    im_flood_fill = thresh.copy()
    h, w = thresh.shape[:2]
    im_flood_fill = cv2.rectangle(im_flood_fill, (0, 0), (w - 1, h - 1), 255, 2)
    mask = np.zeros((h + 2, w + 2), np.uint8)
    cv2.floodFill(im_flood_fill, mask, (0, 0), 0)
    im_flood_fill = cv2.bitwise_not(im_flood_fill)
    # cv2.imshow('clear text', im_flood_fill)
    cv2.imwrite('text.png', im_flood_fill)

    text = pytesseract.image_to_string("text.png", lang='eng')
    print("extractedtext", text)
    return text

