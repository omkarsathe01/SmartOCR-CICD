from pytesseract import Output
import pytesseract
# import 

def split_txt(txt):
    dict = {}
    for line in txt.split("\n"):
        print("line: ", line)
        try:
            val = line.split(":")
            dict[val[0]] = val[1]
        except:
            # print("--------------------")
            # print(f": not found for line: {line}")
            pass
    # print("The cvals arre: ")
    # print(dict)
    return dict


def extract_from_img(img):
    d = pytesseract.image_to_data(img, output_type=Output.DICT)
    # d['text'][i], d['conf'][i]
    xx = {-1:[-1]}
    for i in range(len(d['level'])):
        (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
        if x not in xx.keys():
            if d['text'][i] != "":
                xx[x] = [i]
        else:
            if d['text'][i] != "":
                xx[x] = [i]
    for item in xx.values():
        for i in item:
            print(d["text"][i], end="-") 
        print("---**---**---")
    # print(xx)
    print("----------------------")
    # print(sorted(xx))   
    pass
