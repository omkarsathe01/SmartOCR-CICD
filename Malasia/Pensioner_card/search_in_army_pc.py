import re


def search_in_army_pensionr_card(data, keys):
    english_response = {}
    try:
        key_value_pairs = {}
        # Define the keywords you want to extract
        keywords = ['NO. KAD PENGENALAN', 'NO. TENTERA', 'PANGKAT', 'TARIKH TTP', 'NAMA ISTERI/SUAMI', 'No.Siri']
        not_name = ["LEMBAGA", "PEMASARAN", "PERTANIAN", "PERSEKUTUAN", "MALAYSIA", "ARMED", "FORCES", "VETERAN", "CARD"]

        # Check the first 5 items in the list for names
        for item in data[:5]:
            contains_not_name = any(word in item for word in not_name)
            if not contains_not_name:
                # Check if the item is a valid name based on length and absence of special characters/numbers
                name = item.strip()
                if len(name) > 8 and re.match(r'^[A-Za-z\s]+$', name):
                    key_value_pairs['NAMA'] = name

        # Iterate through the data and extract the key-value pairs
        for item in data:
            for keyword in keywords:
                if keyword in item:
                    # Split the item based on the keyword and take the second part as the value
                    value = item.split(keyword + ':')[1].strip()
                    key_value_pairs[keyword] = value

        malay_to_english = {
            "NAMA": "NAME",
            "NAMA ISTERI/SUAMI": "SPOUSE NAME",
            "NO. KAD PENGENALAN": "IDENTIFICATION CARD NUMBER",
            "NO. TENTERA": "ARMY NUMBER",
            "No.Siri": "SERIAL NUMBER",
            "PANGKAT": "RANK",
            "TARIKH TTP": "RETIREMENT DATE"
        }

        english_response = {malay_to_english[key]: value for key, value in key_value_pairs.items()}

        print(english_response)

        result = {
            "sucess": True,
            "response": english_response,
            "error_code": 0
        }
        return result
    except:
        result = {
            "sucess": False,
            "response": english_response,
            "error_code": -1
        }
        return result


