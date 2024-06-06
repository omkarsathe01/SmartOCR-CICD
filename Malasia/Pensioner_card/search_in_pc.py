import re
from thefuzz import fuzz


def search_in_pensionr_card(data, keys):
    response = {
    }
    try:
        words_to_remove = [
            'NO. K/P', 'NO. AKAUN', 'ISTERVSUAMI', 'KELAYAKAN', 'WAD.', '1A',
            'KAD PESARA', 'KERAJAAN MALAYSIA Re', "NAMA"
        ]

        threshold = 60  # Adjust this threshold based on your requirements
        cleaned_data = [item for item in data if not any(fuzz.ratio(word, item) > threshold for word in words_to_remove)]
        cleaned_data = [item for item in cleaned_data if len(item) > 4]

        for n, item in enumerate(cleaned_data):
            item = re.sub(r'[^\w\s]', '', item).strip()
            # print(item.strip())
            if item.isdigit() and len(item) > 6:
                # if item.replace('-', '').replace('+ ', '').replace('>> ', '').replace('; ', '').isdigit() and len(item) > 6:
                response["identification_card_number"] = item
                break

        if "identification_card_number" not in response:
            return {
                "sucess": False,
                "response": "Document is not clear or not in actual format"
            }
        try:
            response["account_number"] = cleaned_data[n + 1]
        except:
            response["account_number"] = "not found"

        try:
            if not cleaned_data[n - 1].isdigit():
                if len(cleaned_data[n - 1]) < 15:
                    response["name"] = cleaned_data[n - 2] + " " + cleaned_data[n - 1]
                else:
                    response["name"] = cleaned_data[n - 1]
        except:
            response["name"] = "not found"

        try:
            if not cleaned_data[n + 2].isdigit() and len(cleaned_data[n + 2]) > 10:
                response["spouse_or_husband"] = cleaned_data[n + 2]
        except:
            response["spouse_or_husband"] = "not found"
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



