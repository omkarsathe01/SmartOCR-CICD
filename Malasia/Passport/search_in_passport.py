import re
from thefuzz import fuzz


def adhaar_read_data(text, keys):
    asked_info = {}
    other_info = {}

    sex = "FEMALE" if any("female" in text.lower() for text in text) else "MALE"

    # Cleaning first names
    name = text[0]
    name = name.rstrip()
    name = name.lstrip()
    name = name.replace("8", "B")
    name = name.replace("0", "D")
    name = name.replace("6", "G")
    name = name.replace("1", "I")
    name = re.sub('[^a-zA-Z] +', ' ', name)

    # Cleaning DOB
    for t in text:
        dob_match = re.search(r"\d{2}/\d{2}/\d{4}", t)
        if dob_match:
            dob = dob_match.group()
            break

    # Cleaning pincode
    for t in text:
        pincode_match = re.search(r"\d{6}", t)
        if pincode_match:
            pincode = pincode_match.group()
            break

    # Cleaning state
    for t in text:
        pincode_match = re.search(r"\d{6}", t)
        if pincode_match:
            pincode = pincode_match.group()
            break

    #getting VID
    for data in text:
        if ":" in data:
            d = data.split(":")
            if d[1]:
                if "VID " == d[0] or "VID" == d[0]:
                    vid = d[1]

    # Cleaning Adhaar number details
    passport_number = ''
    for word in text:
        if len(word) == 14 and re.match(r"[A-Z]{1}[0-9]{6}[A-Z]{1}", word):
            passport_number = word
    passno = passport_number

    other_info['name'] = name
    other_info['date of birth'] = dob
    other_info['passport number'] = passno
    other_info['gender'] = sex
    other_info['Pincode'] = pincode

    other_info['ID Type'] = "Adhaar"


    #Finding asked information
    extracted_data = [string.replace(':', ',') for string in text]
    for key in keys:
        if key in key:
            if fuzz.ratio(key.lower(), "name") >= 80:
                asked_info['Name'] = name
                keys.remove(key)
            if fuzz.ratio(key.lower(), 'date of birth') >= 80:
                asked_info['Date Of Birth'] = dob
                keys.remove(key)
            if fuzz.ratio(key.lower(), 'aadhar number') >= 80:
                asked_info['Aadhar no'] = adh
                keys.remove(key)
            if fuzz.ratio(key.lower(), 'gender') >= 80:
                asked_info['Gender'] = sex
                keys.remove(key)
            if fuzz.ratio(key.lower(), 'vid') >= 80:
                asked_info['VID'] = vid
                keys.remove(key)

    for i in range(len(extracted_data) - 1):
        key_res = [i for key in keys if(fuzz.ratio(key.lower(), extracted_data[i].lower()) >= 80)]

        if len(key_res) > 0:
            if extracted_data[i+1]:
                if re.search(r"\d{6}", extracted_data[i+2]):
                    asked_info[extracted_data[i]] = extracted_data[i + 1] + " " + extracted_data[i + 2]
                else:
                    asked_info[extracted_data[i]] = extracted_data[i + 1]

    response = {
        "asked info": asked_info,
        "other info": other_info
    }
    return response



    # Process the extracted text to find specific fields
    # lines = text.split("\n")
    # print(lines)
    # data = {
    #     "Name": "",
    #     "Address": "",
    #     "Aadhar Number": "",
    #     "Date of Birth": "",
    #     "Gender": ""
    # }
    # for line in lines:
    #     dob_match = re.search(r"\d{2}/\d{2}/\d{4}", line)
    #     if dob_match:
    #         data["Date of Birth"] = dob_match.group()
    #
    #
    # return data
    #


