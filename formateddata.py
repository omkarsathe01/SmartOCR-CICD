import pyocr
import pyocr.builders
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def get_formated_data(image, line_height=15, width_to_compare=30):
    logger.info("Formatting data...")
    logger.info('Delimiting Data::line height[{}]::width to compare[{}]'.format(line_height, width_to_compare))
    coordinates_list = list()
    words_list = list()
    y1_coordinates_list = list()
    x1_coordinates_list = list()
    y2_coordinates_list = list()
    x2_coordinates_list = list()
    y1_words_list = list()
    punctuations = [':', '|', '.', ';', ',', '#', '#:', '=', '-', 'Rs.', 'Rs']
    tool = pyocr.get_available_tools()[0]
    img = Image.open(image).convert("LA")
    word_boxes = tool.image_to_string(
        img,
        lang='eng',
        builder=pyocr.builders.WordBoxBuilder()
    )
    for word in word_boxes:
        if word.content.replace(' ', '').encode('ascii', 'ignore').decode() in punctuations or word.content.replace(' ', '').encode('ascii', 'ignore').decode() == '':
            continue
        words_list.append(word.content.replace(' ', '').encode('ascii', 'ignore').decode())
        coordinates_list.append(word.position)

    for position, word in zip(coordinates_list, words_list):
        word_At_Position = word
        x1y1, x2y2 = position
        x1, y1 = x1y1
        x2, y2 = x2y2
        y1_coordinates_list.append(y1)
        x1_coordinates_list.append(x1)
        y2_coordinates_list.append(y2)
        x2_coordinates_list.append(x2)
        y1_words_list.append(word_At_Position)

        for curPos in range(len(y1_coordinates_list)):
            for checkPos in range(len(y1_coordinates_list)):
                if y1_coordinates_list[checkPos] >= y1_coordinates_list[curPos]:
                    temp = y1_coordinates_list[checkPos]
                    y1_coordinates_list[checkPos] = y1_coordinates_list[curPos]
                    y1_coordinates_list[curPos] = temp

                    temp = y2_coordinates_list[checkPos]
                    y2_coordinates_list[checkPos] = y2_coordinates_list[curPos]
                    y2_coordinates_list[curPos] = temp

                    temp = x1_coordinates_list[checkPos]
                    x1_coordinates_list[checkPos] = x1_coordinates_list[curPos]
                    x1_coordinates_list[curPos] = temp

                    temp = x2_coordinates_list[checkPos]
                    x2_coordinates_list[checkPos] = x2_coordinates_list[curPos]
                    x2_coordinates_list[curPos] = temp

                    temp = y1_words_list[checkPos]
                    y1_words_list[checkPos] = y1_words_list[curPos]
                    y1_words_list[curPos] = temp

    breakPoint = 0
    start = 0
    checked_list = list()
    lineOCR = ''
    ocr_by_line = list()

    for x in range(len(y1_coordinates_list)):
        if y1_coordinates_list[x] in checked_list:
            continue
        for y in range(x, len(y1_coordinates_list)):
            if y1_coordinates_list[y] >= y1_coordinates_list[x] - line_height and y1_coordinates_list[y] <= y1_coordinates_list[x] + line_height and y != len(y1_coordinates_list) - 1:
                checked_list.append(y1_coordinates_list[y])
                continue
            else:
                breakPoint = y
                for i in range(start, breakPoint):
                    for j in range(start, breakPoint):
                        if x1_coordinates_list[j] > x1_coordinates_list[i]:
                            temp = x1_coordinates_list[j]
                            x1_coordinates_list[j] = x1_coordinates_list[i]
                            x1_coordinates_list[i] = temp

                            temp = x2_coordinates_list[j]
                            x2_coordinates_list[j] = x2_coordinates_list[i]
                            x2_coordinates_list[i] = temp

                            temp = y1_words_list[j]
                            y1_words_list[j] = y1_words_list[i]
                            y1_words_list[i] = temp

                for p in range(start,breakPoint):
                    try:
                        if int(x2_coordinates_list[p])+width_to_compare < int(x1_coordinates_list[p+1]):
                            lineOCR = lineOCR + str(y1_words_list[p]+"$")
                        else:
                            lineOCR = lineOCR + str(y1_words_list[p]+" ")
                    except Exception as tEx:
                        logging.error(tEx)
                start = breakPoint
                break
        ocr_by_line.append(lineOCR)
        lineOCR = ""
    logging.info("Data formated")
    return list(filter(None, ocr_by_line))
