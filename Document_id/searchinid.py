import re


def adhaar_read_data(text, keys):
    try:
        other_info = {}

        sex = "FEMALE" if any("female" in text.lower() for text in text) else "MALE"
        print("sex", sex)

        # Function to check if all words in a string are in title case
        name = ""

        def is_title_case(s):
            return all(word.istitle() for word in s.split())

        # Filter the list to include only items with all words in title case
        extracted_lines = text.split("\n")
        result = [item for item in extracted_lines if is_title_case(item) and len(item) > 5]
        if len(result) > 0:
            name = result[0]

        # Cleaning DOB
        dob = ""
        dob_match = re.search(r"\d{2}/\d{2}/\d{4}", text)
        if dob_match:
            dob = dob_match.group()

        # Cleaning pincode
        pincode = ""
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

        # getting VID
        vid = ""
        for data in text:
            if ":" in data:
                d = data.split(":")
                if d[1]:
                    if "VID " == d[0] or "VID" == d[0]:
                        vid = d[1]

        # Cleaning Adhaar number details
        aadhar = ""
        aadhar_match = re.search(r'\b\d{4}\s\d{4}\s\d{4}\b', text)
        if aadhar_match:
            aadhar = aadhar_match.group()
            if len(aadhar) == 14:
                aadhar = aadhar

        other_info['Name'] = name
        other_info['Date of Birth'] = dob
        other_info['Adhaar Number'] = aadhar
        other_info['Gender'] = sex
        result = {
            "sucess": True,
            "response": other_info,
            "error_code": 0
        }
        return result
    except:
        result = {
            "sucess": False,
            "response": "Internal server error",
            "error_code": -1
        }
        return result


