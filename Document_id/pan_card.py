# from icr_ocr import support
import logging
import re
import pytesseract
from PIL import Image, ImageEnhance
# import difflib
import copy
import random
import string
import os
import cv2
import numpy as np

template_image_process_dir = "image_folder"

logger = logging.getLogger(__name__)


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    this will generate random name
    :param size:
    :param chars:
    :return:
    """
    return ''.join(random.choice(chars) for _ in range(size))


def remove_special_and_lowercase(input_string):
    pattern = r'[^A-Z\s]+'
    result_string = re.sub(pattern, '', input_string)
    return result_string


def pan_card(base_64_string):
    try:
        logger.info('In Pancard defination')
        response = {
            'Date_of_Birth': '-',
            'PAN': '-',
            'Father_Name': '-',
            'Name': '-',
        }

        img = base_64_string

        img_cv2 = cv2.imread(img)

        try:
            enhance_img = Image.open(img)
            enhancer = ImageEnhance.Contrast(enhance_img)
            factor = 1.3  # increase contrast
            im_output = enhancer.enhance(factor)
            improved_image = os.path.join(template_image_process_dir, "{}.jpg".format(id_generator()))
            im_output.save(improved_image)

            img_new = cv2.imread(improved_image)
            img_gray = cv2.cvtColor(img_new, cv2.COLOR_BGR2GRAY)
            logger.info("image has been successfully pre-processed")

        except:
            logger.error("Error found while pre-processing image")

        if img is False:
            return {"response": "Invalid file extention"}

        try:
            test_img = Image.open(img)
            tw, th = test_img.size

            logging.info("{}x{} image resolution".format(tw, th))

            if os.name == "nt":
                test_img.close()

        except Exception as ex:
            logger.error("{} in image test".format(type(ex).__name__))

        # image orientation and resolution test for live scenario

        fixed_size = 1200, 900
        image = Image.open(img).convert('LA')

        image = image.resize(fixed_size, Image.LANCZOS)

        # Declaring Variables-----------------------------------
        lined_txt = []
        names = []
        found = True

        # Removing empty values from data-------------------------
        text = pytesseract.image_to_string(image, config="--psm 4")
        lines = text.split("\n")
        lines = [line for line in lines if line]
        # print(lines)

        # if system is nt
        if os.name == "nt":
            image.close()

        for line in text.split('\n'):
            lined_txt.append(' '.join(line.split()))
        lined_txt = filter(None, lined_txt)
        lined_txt = list(lined_txt)

        # Printing lines------------------------------
        # for line in lined_txt:
        #     print(line)

        # New code starts from here-----------------------------
        copid_list = copy.copy(lined_txt)
        for line in copid_list:
            if "GOVT" in line.upper() or "INCOME" in line.upper() or "TAX" in line.upper():

                lined_txt.pop(lined_txt.index(line))
                break
            else:
                lined_txt.pop(lined_txt.index(line))

        while found == True:
            if len(lined_txt) == 0:
                break
            for idx, line in enumerate(lined_txt):
                if re.search(
                        '(GOVERNMENT|OVERNMENT|VERNMENT|DEPARTMENT|EPARTMENT|PARTMENT|ARTMENT|INDIA|NDIA|GOVT|INCOME|TAX|SEE|ZINA|SRY)',
                        line):
                    lined_txt.pop(idx)
                    found = True
                    break

                if re.findall('(\d+/\d+/\d+)', line):
                    response["Date_of_Birth"] = re.findall('(\d+/\d+/\d+)', line)[0]

                    lined_txt.pop(idx)
                    found = True
                    break
                elif re.findall('\d{10}', line):
                    response["Date_of_Birth"] = re.findall('\d{10}', line)[0]

                    lined_txt.pop(idx)
                    found = True
                    break

                pattern = r"^(?=\s*[A-Z\s]+\s*$).{6,}$"

                pattern = r"^(?=\s*[A-Z\s]+\s*$).{6,}$"
                line = remove_special_and_lowercase(line)

                if re.match(pattern, line):
                    # print(len(line.split()))
                    # print(len(line))

                    if len(line.split()) > 1 and len(line) > 5:
                        if "INCOME" not in line and "GOVT" not in line and "Account" not in line:
                            names.append(' '.join(re.findall(pattern, line)))
                else:
                    # print("Not matched")

                    lined_txt.pop(idx)
                    found = True
                    break

                found = False

        if re.findall(r"^\d{1,2}[./ -]\d{1,2}[./ -]\d{4}$", line):
            response["Date_of_Birth"] = re.findall(r"^\d{1,2}[./ -]\d{1,2}[./ -]\d{4}$", line)[0]

        # print("text: ", text)
        if re.findall('[A-Z]{5}[0-9]{4}[A-Z]{1}', text):
            response["PAN"] = re.findall('[A-Z]{5}[0-9]{4}[A-Z]{1}', text)[0]

        for i, line in enumerate(lines):
            if "Name" in line and "Father's" not in line:

                response["Name"] = remove_special_and_lowercase(lines[i + 1])
            elif "Father's Name" in line:
                response["Father_Name"] = remove_special_and_lowercase(lines[i + 1])
            else:
                pattern = r"^(?=\s*[A-Z\s]+\s*$).{6,}$"
                line = remove_special_and_lowercase(line)
                if re.match(pattern, line):
                    if len(line.split()) > 1 and len(line.split()) < 4 and len(line) > 7:
                        if "INCOME" not in line and "GOVT" not in line and "Account" not in line:
                            names.append(' '.join(re.findall(pattern, line)))

        # print("name not present", response)
        if "Name" not in response or len(response["Name"]) < 2:
            if len(names) > 0:
                response["Name"] = names[0]

        if "Father_Name" not in response or len(response["Father_Name"]) < 2:
            if len(names) > 0:
                response["Father_Name"] = names[1]

        result = {
            "sucess": True,
            "response": response,
            "error_code": 0
        }
        return result
    except:
        result = {
            "sucess": False,
            "response": response,
            "error_code": -1
        }
        return result



