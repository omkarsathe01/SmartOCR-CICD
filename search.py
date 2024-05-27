import re
from thefuzz import fuzz
import logging


logger = logging.getLogger(__name__)


def is_word_in_files(word):
    file_paths = ["Static/EmpDetails.txt", "Static/Earnings.txt", "Static/Deductions.txt", ]
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            for line in file:
                # print(word.lower(), line.lower())
                if fuzz.ratio(word.lower().strip(), line.lower().strip()) > 80:
                    # print(word.lower(), line.lower())
                    # print(fuzz.ratio(word.lower(), line.lower()))
                    return [True, file_path]
    return [False, "not found"]

def find_company_name(lst):
    keywords = [
        "pvt", "LTD", "limited", "Public", "private","Company","Solutions", "Technologies",
        "Systems", "Services", "Global", "International", "techonology", "companies",
        "Innovations", "Group", "Consulting", "Enterprises", "Digital", "Tech",
        "Software", "Network", "Communications", "Media", "Analytics", "Cloud", "Data",
        "Security", "Innovation", "Partners", "Labs", "Automation", "Creative",
        "Development", "Strategy", "Vision", "Future", "Innovators", "Smart", "Edge",
        "World", "Agile", "Partnerships", "Advanced", "Ventures", "Mobility",
        "AI"
    ]
    for i in range(5):
        for word in keywords:
            for string in lst:
                if word.lower() in string.lower():
                    return string
    return False


def process(lst):
    new_list = [[]]
    for line in lst:
        mylist = []
        for word in line:
            new_word = re.sub("[^A-Za-z0-9./ ]+", "", word, 0,) #here added .
            new_word = re.sub("^ +", "", new_word, 0)
            new_word = re.sub(" +$", "", new_word, 0)
            mylist.append(new_word)
        new_list.append(mylist)
    return new_list


def is_numeric(str):
    string = str.replace(",", '')
    if string.isdigit():
        return True
    try:
        float(string)
        return True
    except ValueError:
        return False


def search(lst, keys):
    logger.info("searching...")
    lst = [string.replace(':', '$') for string in lst]
    extracted_data = []
    for element in lst:
        extracted_data.extend([item for item in element.split('$')])
    extracted_data = [x for x in extracted_data if x]
    # print(extracted_data)
    asked_info = {}
    other_info = {}

    company_name = find_company_name(extracted_data)
    # print("list: ", lst)
    if "company name" in keys:
        asked_info["company name"] = company_name
    else:
        other_info["company name"] = company_name
    # Earnings = {}
    # Deductions = {}
    # Employee_details = {}
    for i in range(len(extracted_data) - 1):
        key_res = [i for key in keys if(fuzz.ratio(key.lower(), extracted_data[i].lower()) >= 80)]
        result = is_word_in_files(extracted_data[i])
        if result[0]:
            data = []
            if is_numeric(extracted_data[i + 1]):
                if is_numeric(extracted_data[i + 1 + 1]):
                    data.append(extracted_data[i + 1])
                    data.append(extracted_data[i + 1 + 1])
                    other_info[extracted_data[i]] = data
                else:
                    if result[1] != "Static/EmpDetails.txt":
                        if is_numeric(extracted_data[i + 1]):
                            value = extracted_data[i + 1]
                        else:
                            value = ""
                        other_info[extracted_data[i]] = [value]
                    else:
                        other_info[extracted_data[i]] = [extracted_data[i + 1]]
            else:
                if result[1] != "Static/EmpDetails.txt":
                    if is_numeric(extracted_data[i + 1]):
                        value = extracted_data[i + 1]
                    else:
                        value = ""
                    other_info[extracted_data[i]] = value
                else:
                    other_info[extracted_data[i]] = extracted_data[i + 1]

        if len(key_res) > 0:
            data = []
            if is_numeric(extracted_data[i+1]):
                if is_numeric(extracted_data[i+1+1]):
                    data.append(extracted_data[i+1])
                    data.append(extracted_data[i+1+1])
                    asked_info[extracted_data[i]] = data
                else:
                    asked_info[extracted_data[i]] = extracted_data[i + 1]
            else:
                asked_info[extracted_data[i]] = extracted_data[i+1]

    response = {
        "sucess": True,
        "asked_info": asked_info,
        "other_info": other_info
    }
    return response



def searchinscrap(lst, keys):
    asked_info = {}
    other_info = {}

    extracted_data = []
    for element in lst:
        extracted_data.extend([item for item in element.split('$')])
    extracted_data = [x for x in extracted_data if x]

    for data in extracted_data:
        if ":" in data:
            d = data.split(":")
            if d[1]:
                other_info[d[0]] = d[1]
            extracted_data.remove(data)

    for i, data in enumerate(extracted_data):
        if is_numeric(data):
            if not is_numeric(extracted_data[i-1]) and i > 1:
                other_info[extracted_data[i-1]] = extracted_data[i]

    for i in range(len(extracted_data) - 1):
        key_res = [i for key in keys if(fuzz.ratio(key.lower(), extracted_data[i].lower()) >= 80)]

        if len(key_res) > 0:
            data = []
            if is_numeric(extracted_data[i+1]):
                if is_numeric(extracted_data[i+1+1]):
                    data.append(extracted_data[i+1])
                    data.append(extracted_data[i+1+1])
                    asked_info[extracted_data[i]] = data
                else:
                    asked_info[extracted_data[i]] = extracted_data[i + 1]
            else:
                asked_info[extracted_data[i]] = extracted_data[i+1]

    sorted_info = {key.replace("\t", ""): value for key, value in other_info.items() if len(value) != 1}
    response = {
        "sucess": True,
        "asked_info": asked_info,
        "other_info": sorted_info
    }
    return response


####################################### FOR BANK STATEMENT ########################################
def is_word_in_file(word):
    file_path = "Static/userinfo_for_bs.txt"
    with open(file_path, 'r') as file:
        for line in file:
            if fuzz.ratio(str(word.lower()), str(line.lower())) > 80 or str(word.lower()) == str(line.lower()):
                return True

        return False
# to search required data in bank statement
def searchinbs(formated_data, keys):
    logger.info("Searching in bank statement")
    transections = []
    # getting opening balance, total debits, credits, closing balance, dr count, cr count
    total_data = {}
    for i, line in enumerate(formated_data):
        for j, word in enumerate(line):
            if (fuzz.ratio('opening Balance', word.lower()) >= 80):
                total_data[word] = formated_data[i + 1][j]
                total_data[line[j + 1]] = formated_data[i + 1][j + 1]
                total_data[line[j + 2]] = formated_data[i + 1][j + 2]
                total_data[line[j + 3]] = formated_data[i + 1][j + 3]
                total_data[line[j + 4]] = formated_data[i + 1][j + 4]
                total_data[line[j + 5]] = formated_data[i + 1][j + 5]

    temp_opening_balance = float(total_data['Opening Balance'].replace(",", ''))

    # transections.append(total_data)
    for line in formated_data:
        if len(line) > 3:  # Table line identification
            data = {}

            # checking each word of line
            for i, string in enumerate(line):
                match = False  # it's to denote table line or not
                match1 = re.search(r"\d{2}/\d{2}/\d{2}", string)
                match2 = re.search(r"\d{2}/\d{2}/\d{4}", string)
                if match1:
                    # match = True               #If table line found it's became true
                    if (i == 0):  # i == 0 means it's a first string
                        data["date"] = match1.group()
                        updated_string = re.sub(r"\d{2}/\d{2}/\d{2}", '', string)
                        data["particulars"] = updated_string
                    else:
                        match = True
                        data["value_date"] = match1.group()
                        updated_string = re.sub(r"\d{2}/\d{2}/\d{2}", '', string)
                        data["cheque_no"] = updated_string
                if match2:
                    if (i == 1):  # i == 0 means it's a first string
                        data["date"].append(match2.group())
                        updated_string = re.sub(r"\d{2}/\d{2}/\d{4}", '', string)
                        data["particulars"].append(updated_string)
                    else:
                        match = True
                        data["value_date"].append(match2.group())
                        updated_string = re.sub(r"\d{2}/\d{2}/\d{4}", '', string)
                        data["cheque_no"].append(updated_string)

                if match:
                    amount = float(line[3].replace(",", ''))
                    if amount < temp_opening_balance:
                        data["withdrawal"] = line[2]
                        data["balance"] = line[3]
                        temp_opening_balance = amount
                    else:
                        data["deposite"] = line[2]
                        data["balance"] = line[3]
                        temp_opening_balance = amount
            transections.append(data)

    # getting other information
    split_data = []
    for sublist in formated_data:
        split_sublist = []
        for item in sublist:
            if ':' in item:
                split_item = item.split(':', 1)
                split_sublist.extend(split_item)
            else:
                split_sublist.append(item)
        splited_sublist = [x for x in split_sublist if x != " " or ""]
        split_data.append(splited_sublist)

    user_info = {}
    for line in split_data:
        for i, word in enumerate(line):
            result = is_word_in_file(word)
            if result:
                user_info[word.strip()] = line[i + 1].strip()

    # Adding name and address
    name = formated_data[0]

    address = ''
    for item in formated_data[1:]:
        if isinstance(item, str):
            address += ' ' + str(item)
        else:
            break

    address = address.strip()

    user_info["Customer name"] = name
    user_info["Customer Address"] = address
    filtered_data = [d for d in transections if d]
    whole_data = {
        "sucess": True,
        "header info": user_info,
        "total data": total_data,
        "transections": filtered_data
    }

    return whole_data
