from PIL import Image
import numpy as np
import cv2
import pytesseract
import re
import json
import logging


# logger = logging.getLogger(__name__)


def get_formated_data_of_ctos(image_path):
    # Open the PNG image
    image = Image.open(image_path)

    # Convert the image to RGB mode if it has an alpha channel
    if image.mode == "RGBA":
        image = image.convert("RGB")

    # Convert the image to a NumPy array
    image_np = np.array(image)

    # Apply Canny edge detection
    edged = cv2.Canny(image_np, 30, 200)

    # Find contours
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Draw all contours
    cv2.drawContours(image_np, contours, -1, (0, 255, 0), 3)

    # Perform text extraction from contours
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

        if h > 300 and h < 320 and w > 770 and w < 800:
            cv2.rectangle(image_np, (x, y), (x + w, y + h), (36, 255, 12), 2)
            roi = image_np[y:y + h, x:x + w]
            name = pytesseract.image_to_string(roi)
            lines = name.split("\n")
            n_and_a = [x for x in lines if x]
            return n_and_a
