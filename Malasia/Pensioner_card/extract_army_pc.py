import re
import pytesseract


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


def get_army_p_id_text(image_path):
    # logger.info("Formatting bank statement data...")
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

    # Clean the list
    cleaned_data = [item.strip() for sublist in ans if sublist for item in sublist]

    # Remove empty strings
    cleaned_data = [item for item in cleaned_data if item]
    cleaned_data = [item for item in cleaned_data if item != ":" and item != "|" and len(item) > 2]
    return cleaned_data
