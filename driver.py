import json
# import img_preprocess
import time
import search
from flask import jsonify
from Document_id.formatediddata import getidtext
from Document_id.searchinid import adhaar_read_data
from removeborder import borderRemove
from formateddata import get_formated_data
from formateddataforscrap import get_formated_data_of_scrap
# from Bank_statement.search_in_bs import searchinbs
from Document_id.pan_card import pan_card
from blur_image_detector import blur_detection
from formated_data_of_bs import get_formated_data_of_bs, find_name_and_address
from Malasia.Passport.extract_passport import get_passport_text
from Malasia.Bank_statement.extract_bs import get_formated_data_of_malaysian_bs, find_n_and_a, find_deposited_amounts
from Malasia.Bank_statement.search_in_bs import search_in_malaysian_bs
from Malasia.Ctos.extract_ctos import get_formated_data_of_ctos
from Malasia.Ctos.search_in_ctos import search_in_ctos
from Malasia.Pensioner_card.extract_pc import get_p_id_text
from Malasia.Pensioner_card.search_in_pc import search_in_pensionr_card
from Malasia.Pensioner_card.extract_army_pc import get_army_p_id_text
from Malasia.Pensioner_card.search_in_army_pc import search_in_army_pensionr_card
import logging

logger = logging.getLogger(__name__)

# converting to json
def to_json(dic):
    json_object = json.dumps(dic, indent=4)
    return json_object


def func(path, keys, doc):
    print("doc", doc)
    if doc == "bank_statement":
        logger.info("Extracting bank statement...")
        return extract_from_bank_statement(path, keys)
    elif doc == "salary_slip":
        logger.info("Extracting salary slip...")
        return extract_from_salaryslip(path, keys)
    elif doc == "pensioner_card":
        print("hello", doc)
        logger.info("Extracting pensioner card...")
        return extract_from_pensionr_card(path, keys)
    elif doc == "army_pensioner_card":
        logger.info("Extracting army_pensioner_card...")
        return extract_from_army_pensionr_card(path, keys)
    elif doc == "ctos":
        logger.info("Extracting Ctos report...")
        return extract_from_ctos(path, keys)
    elif doc == "pancard":
        return extract_from_pancard(path)
    elif doc == "aadhar":
        logger.info("Extracting aadhar card...")
        return extract_from_aadhar(path, keys)
    elif doc == "scrap":
        logger.info("Extracting scrap data...")
        return extract_from_scrap(path, keys)
    elif doc == "passport":
        logger.info("Extracting passport...")
        return extract_from_passport(path, keys)
    elif doc == "malaysian_bank_statement":
        logger.info("Extracting malaysian bank statement...")
        return extract_from_malaysian_bank_statement(path, keys)
    else:
        response = {
            "success": "false",
            "status": "OCR of this document is not available"
        }
        return response


def extract_from_img(path, keys, ind):
    # img = img_preprocess.process_from_path(path)
    path = borderRemove(path)
    formated_data = get_formated_data(path, ind)
    dic = search.search(formated_data, keys)
    return to_json(dic)


def extract_from_salaryslip(path, keys):
    formated_data = []
    for p in path:
        start_time = time.time()
        # p = borderRemove(p)
        end_time = time.time()
        print("Time required for image processing: ", end_time - start_time)
        start_time = time.time()
        formated_data.extend(get_formated_data(p))
        end_time = time.time()
        print("Time required for ocr and format data: ", end_time - start_time)
    start_time = time.time()
    dic = search.search(formated_data, keys)
    end_time = time.time()
    print("Time required to find required data in raw text: ", end_time - start_time)
    return to_json(dic)


def extract_from_scrap(path, keys):
    formated_data = []
    for p in path:
        p = borderRemove(p)
        formated_data.extend(get_formated_data_of_scrap(p))
    print("F:", formated_data)
    dic = search.searchinscrap(formated_data, keys)
    return to_json(dic)


def extract_from_bank_statement(path, keys):
    formated_data = []
    for p in path:
        # Finding name and address field seprately
        name_and_address = find_name_and_address(p)
        if name_and_address:
            formated_data.extend(name_and_address)
        p = borderRemove(p)
        formated_data.extend(get_formated_data_of_bs(p))
    print("F:", formated_data)
    dic = search.searchinbs(formated_data, keys)
    return to_json(dic)


# def extract_from_invoice(path, keys):
#     formated_data = []
#     for p in path:
#         # p = borderRemove(p)
#         formated_data.extend(get_formated_data_of_bs(p))
#     print("formated data: ", formated_data)
#     dic = search.search(formated_data, keys)
#     return to_json(dic)

def extract_from_aadhar(path, keys):
    formated_data = getidtext(path[0])
    #print("formated data: ", formated_data)
    dic = adhaar_read_data(formated_data, keys)
    return jsonify(dic)


def extract_from_pancard(path):
    dic = pan_card(path[0])
    return jsonify(dic)

# ################################################# MALAYSIAN DOC ###############################################################


def extract_from_passport(path, keys):
    formated_data = []
    for p in path:
        print("path in driver", p)
        formated_data.extend(get_passport_text(p))
    print("formated data: ", formated_data)
    dic = adhaar_read_data(formated_data, keys)
    return to_json(dic)


def extract_from_pensionr_card(path, keys):
    formated_data = []
    blur, text = blur_detection(path[0])
    if blur:
        return text
    for p in path:
        print("path in driver", p)
        formated_data.extend(get_p_id_text(p))
    print("formated data: ", formated_data)
    dic = search_in_pensionr_card(formated_data, keys)
    return jsonify(dic)


def extract_from_army_pensionr_card(path, keys):
    formated_data = []
    blur, text = blur_detection(path[0])
    if blur:
        return text
    for p in path:
        formated_data.extend(get_army_p_id_text(p))
    print("formated data: ", formated_data)
    dic = search_in_army_pensionr_card(formated_data, keys)
    return jsonify(dic)


def extract_from_malaysian_bank_statement(path, keys):
    formated_data = []
    deposited_amounts = []
    # Finding name and address field seprately
    name_and_address = find_n_and_a(path[0], keys)
    if name_and_address:
        formated_data.extend(name_and_address)
    for p in path:
        start_time = time.time()
        p = borderRemove(p)
        end_time = time.time()
        print("Time required for image processing: ", end_time - start_time)
        start_time = time.time()
        if keys == "hongleong":
            deposited_amounts.extend(find_deposited_amounts(p))
        formated_data.extend(get_formated_data_of_malaysian_bs(p))
        end_time = time.time()
        print("Time required for ocr and format data: ", end_time - start_time)
    print("F:", formated_data)
    start_time = time.time()
    dic = search_in_malaysian_bs(formated_data, keys, deposited_amounts)
    end_time = time.time()
    print("Time required to find required data in raw text: ", end_time - start_time)
    return jsonify(dic)


def extract_from_ctos(path, keys):
    formated_data = []
    for p in path:
        print("path in driver", p)
        formated_data.extend(get_formated_data_of_ctos(p))
    print("formated data: ", formated_data)
    dic = search_in_ctos(formated_data, keys)
    return to_json(dic)
