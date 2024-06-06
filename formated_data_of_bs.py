import re
from PIL import Image
import numpy as np
import cv2
import pytesseract
import logging

logger = logging.getLogger(__name__)


def preprocess(corpus):
    txt = corpus.split("\n")
    while "" in txt:
        txt.remove("")

    txt = '\n'.join(txt)
    return txt


def passing(img):
    custom_config = r'-c preserve_interword_spaces=1 --psm 4'
    txt = pytesseract.image_to_string(img, config=custom_config)
    txt = preprocess(txt)
    return txt

def find_name_and_address(image_path):
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






def get_formated_data_of_bs(image_path):
    logger.info("Formatting bank statement data...")
    text = passing(image_path)
    lines = text.split("\n")
    ans = [[]]
    for line in lines:
        tokens = re.findall('\s+', line)
        mylist = []
        words = re.split("\s+", line)
        prefix = ""

        for i in range(0, len(words) - 1):
            if i != 0:
                prefix += " " + words[i]
            else:
                prefix = words[i]

            if len(tokens[i]) > 1:
                mylist.append(prefix)
                prefix = ""
        mylist.append(prefix + " " + words[len(words) - 1])
        ans.append(mylist)

    filtered_data = []
    for line in ans:
        separated_data = []
        for item in line:
            parts = re.findall(r'[A-Za-z\s]+|\d+\.\d+', item)
            separated_data.extend(parts)
        filtered_data.append(separated_data)

    print("ans: ", lines)
    return ans


        # 04/01/19 9 1 5 2
# =NWD-541919XXXXXX2103-S1CPN345-NOIDA 9 2 5 2
#  9 0 4 3
# 04/01/19 9 1 5 3
# =NWD-541919XXXXXX2103-S1CPN345-NOIDA 9 2 5 3

# 00009004 23 1 5 1
# 10004322 23 2 5 1
# 04/01/19 23 3 5 1
#  23 0 4 2
# 00009004 23 1 5 2
# 10004323 23 2 5 2
# 04/01/19 23 3 5 2

# 10,000.00 27 1 5 2
#  27 0 4 3
# 5,000.00 27 1 5 3

# 22,299.06 45 1 5 2
#  45 0 4 3
# 17,299.06 45 1 5 3
#  45 0 4 4