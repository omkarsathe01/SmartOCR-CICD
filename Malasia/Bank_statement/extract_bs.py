from PIL import Image
import numpy as np
import cv2
import pytesseract
import re
import json
import logging


logger = logging.getLogger(__name__)
with open('Malasia/Bank_statement/config.json', 'r') as c:
    params = json.load(c)["info"]


# Only for hong leong bank
def find_deposited_amounts(img):
    # # Open the PNG image
    image = Image.open(img)

    # # Convert the image to a NumPy array
    image_np = np.array(image)
    # cv2.rectangle(image_np, (x, y), (x + w, y + h), (36, 255, 12), 2)
    cv2.rectangle(image_np, (840, 596), (840 + 336, 596 + 1648), (36, 255, 12), 2)
    #  extracted_text[y:y+h, x:x+w]
    roi = image_np[596:596 + 1648, 927:927 + 248]
    cv2.imwrite("/content/output.png", roi)
    debit_amounts = pytesseract.image_to_string(roi)
    lines = debit_amounts.split("\n")
    debit_amounts = [x for x in lines if x and x != " "]
    # Filter floating-point values using list comprehension
    floating_values = [value.replace(",", "") for value in debit_amounts if
                       isinstance(value, str) and value.replace(',', '').replace('.', '').isdigit()]
    # Print the filtered floating-point values
    return floating_values


def find_n_and_a(image_path, bank):
    # # Open the PNG image
    image = Image.open(image_path)

    # # Convert the image to a NumPy array
    image_np = np.array(image)
    print("BANKKKKKKKKK: ", bank )
    # cv2.rectangle(image_np, (x, y), (x + w, y + h), (36, 255, 12), 2)
    if bank == "maybank" or "cimb":
        print("11111111111111111111111111111111111111111111111")
        # cv2.rectangle(image_np, (params['cm'][0], params['cm'][1]), (params['cm'][0] + params['cm'][2], params['cm'][1] + params['cm'][3]), (36, 255, 12), 2)
        roi = image_np[params['cm'][1]:params['cm'][1] + params['cm'][3], params['cm'][0]:params['cm'][0] + params['cm'][2]]
    # roi = image_np[259:259 + 156, 145:145 + 495]
    # cv2.imwrite("/content/output.png", roi)
    if bank == "rhb":
        print("222222222222222222222222222222222222222222222222")
        cv2.rectangle(image_np, (params['rb'][0], params['rb'][1]), (params['rb'][0] + params['rb'][2], params['rb'][1] + params['rb'][3]), (36, 255, 12), 2)
        roi = image_np[params['rb'][1]:params['rb'][1] + params['rb'][3], params['rb'][0]:params['rb'][0] + params['rb'][2]]
        cv2.imwrite("./output.png", roi)

    if bank == "hongleong":
        print("3333333333333333333333333333333333333333333333333")
        cv2.rectangle(image_np, (params['hl'][0], params['hl'][1]), (params['hl'][0] + params['hl'][2], params['hl'][1] + params['hl'][3]), (36, 255, 12), 2)
        roi = image_np[params['hl'][1]:params['hl'][1] + params['hl'][3], params['hl'][0]:params['hl'][0] + params['hl'][2]]
        cv2.imwrite("output.png", roi)

    if bank == "RHB":
        print("44444444444444444444444444444444444444444444444444")
        cv2.rectangle(image_np, (params['rhb'][0], params['rhb'][1]), (params['rhb'][0] + params['rhb'][2], params['rhb'][1] + params['rhb'][3]), (36, 255, 12), 2)
        roi = image_np[params['rhb'][1]:params['rhb'][1] + params['rhb'][3], params['rhb'][0]:params['rhb'][0] + params['rhb'][2]]
        cv2.imwrite("output.png", roi)

    if bank == "bank_islam":
        print("555555555555555555555555555555555555555555555555555")
        # cv2.rectangle(image_np, (params['rhb'][0], params['rhb'][1]), (params['rhb'][0] + params['rhb'][2], params['rhb'][1] + params['rhb'][3]), (36, 255, 12), 2)
        roi = image_np[params['bi'][1]:params['bi'][1] + params['bi'][3], params['bi'][0]:params['bi'][0] + params['bi'][2]]
        cv2.imwrite("output.png", roi)

    if bank == "bank_maumalat":
        print("666666666666666666666666666666666666666666666666666")
        # cv2.rectangle(image_np, (params['rhb'][0], params['rhb'][1]), (params['rhb'][0] + params['rhb'][2], params['rhb'][1] + params['rhb'][3]), (36, 255, 12), 2)
        roi = image_np[params['bm'][1]:params['bm'][1] + params['bm'][3], params['bm'][0]:params['bm'][0] + params['bm'][2]]
        cv2.imwrite("output.png", roi)
    name = pytesseract.image_to_string(roi)
    print("nameEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE: ", name)
    lines = name.split("\n")
    n_and_a = [x for x in lines if x and x != " "]
    return n_and_a


def preprocess(corpus):
    txt = corpus.split("\n")
    while "" in txt:
        txt.remove("")

    txt = '\n'.join(txt)
    return txt


def passing(img):
    custom_config = r'-c preserve_interword_spaces=1 --psm 4'
    txt = pytesseract.image_to_string(img, config=custom_config)
    # print("TEXT: ", txt)
    txt = preprocess(txt)
    return txt


def get_formated_data_of_malaysian_bs(image_path):
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
    # print("ANS: ", ans)
    return ans
