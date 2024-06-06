import pyocr
import pyocr.builders
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def get_formated_data_of_scrap(image, line_height=15, width_to_compare=30):
    print("I am in formated data")
    logger.info('Delimiting Data::line height[{}]::width to compare[{}]'.format(line_height, width_to_compare))
    coordinates_list = list()
    words_list = list()
    y1_coordinates_list = list()
    x1_coordinates_list = list()
    y2_coordinates_list = list()
    x2_coordinates_list = list()
    y1_words_list = list()
    punctuations = ['|', '.', ';', ',', '#', '#:', '=', '-', 'Rs.', 'Rs', '~']
    tool = pyocr.get_available_tools()[0]
    img = Image.open(image).convert("LA")
    word_boxes = tool.image_to_string(
        img,
        lang='eng',
        builder=pyocr.builders.WordBoxBuilder()
    )
    for word in word_boxes:
        if word.content.replace(' ', '').encode('ascii', 'ignore').decode() in punctuations or word.content.replace(' ',
                                                                                                                    '').encode(
                'ascii', 'ignore').decode() == '':
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
            if y1_coordinates_list[y] >= y1_coordinates_list[x] - line_height and y1_coordinates_list[y] <= \
                    y1_coordinates_list[x] + line_height and y != len(y1_coordinates_list) - 1:
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

                for p in range(start, breakPoint):
                    try:
                        if int(x2_coordinates_list[p]) + width_to_compare < int(x1_coordinates_list[p + 1]):
                            lineOCR = lineOCR + str(y1_words_list[p] + "$")
                        else:
                            lineOCR = lineOCR + str(y1_words_list[p] + " ")
                    except Exception as tEx:
                        logging.error(tEx)
                start = breakPoint
                break
        ocr_by_line.append(lineOCR)
        lineOCR = ""
    return list(filter(None, ocr_by_line))

#
# # Call the function to split the image
#     split_images = split_image(image)
#
#     # Create a list of image names
#     image_names = []
#     for i, image in enumerate(split_images):
#         image_name = f'part{i + 1}.jpg'
#         cv2.imwrite(image_name, image)
#         image_names.append(image_name)
#
#     # Print the list of image names
#     print(image_names)
#
#     tool = pyocr.get_available_tools()[0]
#     img = Image.open(image).convert("LA")
#     word_boxes = tool.image_to_string(
#         img,
#         lang='eng',
#         builder=pyocr.builders.LineBoxBuilder()
#     )
#     punctuations = [':', '|', '.', ';', ',', '#', '#:', '=', '-']
#     coordinates_list = []
#     words_list = []
#     for word in word_boxes:
#         if word.content.replace(' ', '').encode('ascii', 'ignore').decode() in punctuations or word.content.replace(' ',
#                                                                                                                     '').encode(
#                 'ascii', 'ignore').decode() == '':
#             continue
#         words_list.append(word.content)
#         coordinates_list.append(word.position)
#     print(words_list)
#
#     txt = ""
#     print("path", image)
#     txt = txt + "\n" + pytesseract.image_to_boxes(image)
#     print(txt)
#     lines = txt.split("\n")
#     ans = [[]]
#     for line in lines:
#         tokens = re.findall('\s+', line)
#         print("tokens: ", tokens)
#         mylist = []
#         words = re.split("\s+", line)
#         prefix = ""
#
#         for i in range(0, len(words)-1):
#             print("word: ", words)
#             if i != 0:
#                 prefix += " "+words[i]
#             else:
#                 prefix = words[i]
#
#             if len(tokens[i]) > 1:
#                 mylist.append(prefix)
#                 prefix = ""
#         mylist.append(prefix+" "+words[len(words)-1])
#         ans.append(mylist)
#
#     filtered_data = []
#     for line in ans:
#         separated_data = []
#         for item in line:
#             parts = re.findall(r'[A-Za-z\s]+|\d+\.\d+', item)
#             separated_data.extend(parts)
#             print("ans: ", separated_data)
#         filtered_data.append(separated_data)
#         # print("filtered data :", filtered_data)
#     print("ans: ", ans)
#     return ans



