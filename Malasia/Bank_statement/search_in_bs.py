import re
from thefuzz import fuzz
import json
from . import categories


# logger = logging.getLogger(__name__)

with open('Malasia/Bank_statement/config.json', 'r') as c:
    params = json.load(c)["info"]


# to convert the date strings from the format "Oct 26" to "27/10/2020"
def convert_date_with_year(input_date, year):
    # Split the input date string by space
    # day, month = input_date.strip().split(' ')
    day = input_date[:2]  # Get the first two characters (day)
    month = input_date[2:]

    # Map month names to their correspondingprint numerical values
    month_mapping = {
        'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06',
        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
    }
    # Get the numerical value of the month
    month_num = month_mapping[month]

    # Build the output date string in the format "dd/mm/yyyy"
    output_date = f"{day}/{month_num}/{year}"

    return output_date


def convert_to_four_digit_year(date_str):
    day, month, year = date_str.split('/')
    year = year if len(year) == 4 else '20' + year
    return f'{day}/{month}/{year}'


def search_in_hongleong(formated_data, temp_opening_balance, deposited_amounts):
    print(deposited_amounts)
    transections = []
    total_debit_amount = 0
    total_credit_amount = 0
    print(formated_data)
    for m, line in enumerate(formated_data):
        if len(line) > 1:
            match1 = re.search(r"\d{2}-\d{2}-\d{4}", line[0])
            if match1:  # Table line identification
                data = {}
                # checking each word of line
                for i, string in enumerate(line):
                    match = False  # it's to denote table line or not
                    if match1:
                        match = True  # If table line found it's became true
                        if (i == 0):  # i == 0 means it's a first string
                            data["date"] = match1.group().replace("-", "/")
                            updated_string = re.sub(r"\d{2}-\d{2}-\d{4}", '', string)
                            particular = updated_string
                            cnt = 0
                            while len(formated_data[m + 1]) == 1 and cnt < 4 and len(formated_data[m + 1][0].strip()) < 40:
                                particular += " " + formated_data[m + 1][0]
                                m += 1
                                cnt += 1

                            data["description"] = particular
                            data["reference"] = ""
                if match:
                    if len(line) > 2:
                        amount = float(
                            line[len(line) - 1].replace(",", "") if "," in line[len(line) - 1] else line[len(line) - 1])
                    else:
                        print(line[-1].replace(",", "") in deposited_amounts, line[-1].replace(",", ""))

                        if line[-1].replace(",", "") in deposited_amounts:
                            amount = float(temp_opening_balance) + float(line[-1].replace(",", "") if "," in line[-1] else line[-1])
                        else:
                            amount = float(temp_opening_balance) - float(line[-1].replace(",", "") if "," in line[-1] else line[-1])

                if amount < float(temp_opening_balance):
                    print("i am in debit:", amount)
                    if len(line) > 2:
                        data["amount"] = float(
                            line[len(line) - params["pos_of_dep_or_with_column_from_right"]].replace(",",
                                                                                                     "").replace(
                                "+", "").replace("-", "") if "," or "+" or "-" in line[
                                len(line) - params["pos_of_dep_or_with_column_from_right"]] else \
                                line[len(line) - params["pos_of_dep_or_with_column_from_right"]])
                        data["balance"] = float(
                            line[len(line) - 1].replace(",", "") if "," in line[len(line) - 1] else line[
                                len(line) - 1])
                    else:
                        data["amount"] = float(
                            line[-1].replace(",", "").replace("+", "").replace("-", ""))
                        print("amount2:", amount)
                        data["balance"] = float(amount)

                    data["type"] = "debit"
                    total_debit_amount += float(data["amount"])
                    temp_opening_balance = amount

                else:
                    print("i am in credit:", amount)
                    if len(line) > 2:
                        data["amount"] = float(
                            line[len(line) - params["pos_of_dep_or_with_column_from_right"]].replace(",",
                                                                                                     "").replace(
                                "+", "").replace("-", "") if "," or "+" or "-" in line[
                                len(line) - params["pos_of_dep_or_with_column_from_right"]] else \
                                line[len(line) + params["pos_of_dep_or_with_column_from_right"]])
                        data["balance"] = float(amount)
                    else:
                        data["amount"] = float(
                            line[-1].replace(",", "").replace("+", "").replace("-", ""))
                        data["balance"] = float(amount)

                    data["type"] = "credit"
                    total_credit_amount += float(data["amount"])
                    temp_opening_balance = amount

                    # recognise category of transection
                    # data["category"] = categories.categorize_transection(data["particulars"])
                    # data["expense_type"] = categories.categorize_expenses(data["particulars"])
                transections.append(data)
    return transections


def search_in_malaysian_bs(formated_data, bank, deposited_amount):
    # logger.info("Searching bank statement data...")
    print(formated_data)
    transections = []
# getting opening balance, closing balance and other things by matching ratio
    total_data = {}
    a_c_no = []
    opening_b = ""
    for i, line in enumerate(formated_data):
        words = params['words']
        for j, word in enumerate(line):
            for w in words:
                if fuzz.ratio(w.lower(), word.lower()) >= 90:
                    print("w: ", w)
                    total_data[w.lower()] = line[j + 1].replace(":", "")
# ####################### Extra necessary things finding from all bank statements ######################################
                if bank == "rhb":
                    if "Beginning Balance as of" in word:
                        total_data["opening balance"] = line[j + 1]
                        total_data["year"] = str(re.findall(r'\b\d{4}\b', word)[0])
                if bank == "RHB":
                    if "B/F BALANCE" in word:
                        total_data["opening balance"] = line[j + 1]
                    if "RHB SMART ACCOUNT-i" in word:
                        try:
                            total_data["account number"] = line[j + 1]
                        except:
                            pass
                if bank == "abi":
                    if "STATEMENT DATE / TARIKH PENYATA" in word:
                        total_data["year"] = str(re.findall(r'\b\d{4}\b', word)[0])

                if bank == "hongleong":
                    if "No Akaun" in word:
                        ac_no = word.split(":")
                        total_data["account number"] = ac_no[1].strip()

                if bank == "bank_islam":
                    # print(i, word, line)
                    if i < 20:
                        if "ACCOUNT NO" in word:
                            total_data["account number"] = line[j+2].strip()

                if bank == "bank_maumalat":
                    # print(i, word, line)
                    if "B/F" in word:
                        modified_list = [item for item in line if ":" not in item]
                        # print("modified list: ", modified_list)
                        opening_b = modified_list[1].strip()

                if bank == "maybank":
                    pattern = r'^\d{12}$|^\d{6}-\d{6}$'
                    if re.match(pattern, word.strip()):
                        a_c_no.append(word)

    if bank == "maybank":
        print("account no: ", a_c_no)
        total_data["account number"] = a_c_no[0].strip()

    if bank == "bank_maumalat":
        total_data["opening balance"] = opening_b



# ################################### finding opening balance of all banks ######################################
    print(total_data)
    try:
        if bank == "maybank":
            temp_opening_balance = float(total_data['beginning balance'].replace(",", ""))
        elif bank == "hongleong":
            temp_opening_balance = float(total_data['balance from previous statement'].replace(",", ""))
        elif bank == "bsn":
            temp_opening_balance = float(total_data["baki hadapan"].replace(",", ""))
        elif bank == "bank_islam":
            temp_opening_balance = float(total_data["bal b/f"].replace(",", ""))
        elif bank == "abi":
            temp_opening_balance = float(total_data["baki bawa ke hadapan / balance b/f"].replace(",", ""))
        elif bank == "bank_maumalat":
            temp_opening_balance = float(total_data['opening balance'].replace(",", "").replace(".", ""))
        else:
            temp_opening_balance = float(total_data['opening balance'].replace(",", ""))
    except:
        response = {
            "error_code": -1, 
            "success": "false",
            "status": "Opening balance not found or your pdf is not clear"
        }
        return response
    # ['3/07/23', ' DUITNOW TRANSFER', " '04481600041182", ' 165.30', ' 1,790.']
##################################################################################################################
    opening_balance = temp_opening_balance
    # transections.append(total_data)
    total_debit_amount = 0
    total_credit_amount = 0
    if bank == "hongleong":
        transections = search_in_hongleong(formated_data, temp_opening_balance, deposited_amount)
        # print("transections: ", transections)
    else:
        for m, line in enumerate(formated_data):
            if len(line) > params["no_of_filled_column"]-2:  # Table line identification
                if bank == "bank_maumalat":
                    line = [item for item in line if ' .00' not in item and ' -00' not in item and ' |' not in item]
                data = {}
                if line[1] == " C/F BALANCE":
                    break
                # checking each word of line
                for i, string in enumerate(line):
                    match = False  # it's to denote table line or not
                    pos1, pos2, pos3 = params["date_format"]
                    if bank == "maybank":
                        pos3 = 2
                    try:
                        if bank == "rhb":
                            match1 = re.search(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}\b", string, re.IGNORECASE)
                        elif bank == "hongleong":
                            match1 = re.search(fr"\d{{{pos1}}}-\d{{{pos2}}}-\d{{{pos3}}}", string)
                        elif bank == "bank_islam":
                            match1 = re.search(r"\d{1,2}/\d{2}/\d{2}", string)
                        elif bank == "bank_maumalat":
                            match1 = re.search(r"\d{1,2}/\d{2}/\d{2}", string)
                            print("1", match1)
                            if not match1:
                                match1 = re.search(r"\d{1,2}/\d{2}/\d{1,2}", string)
                                print("2", match1)
                        elif bank == "bsn":
                            match1 = re.search(r"\b\d{1,2}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", string, re.IGNORECASE)
                        elif bank == "abi":
                            match1 = re.search(r"\b\d{1,2}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", string, re.IGNORECASE)
                        elif bank == "RHB":
                            match1 = re.search(r"\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", string, re.IGNORECASE)
                        else:
                            match1 = re.search(fr"\d{{{pos1}}}/\d{{{pos2}}}/\d{{{pos3}}}", string)
                    except:
                        match1 = re.search(fr"\d{{{pos1}}}/\d{{{pos2}}}", string)
                    if match1 and i == 0:
                        match = True  # If table line found it's became true
                        if (i == 0):  # i == 0 means it's a first string
                            if bank == "bank_maumalat":
                                data["date"] = convert_to_four_digit_year(match1.group())
                            else:
                                data["date"] = convert_date_with_year(match1.group(), total_data["year"]) if re.match(r"\b\d{1,2}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", match1.group(), re.IGNORECASE) else match1.group()
                            # print("match", match1.group())

                            try:
                                if bank == "rhb":
                                    updated_string = re.sub(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec) \d{1,2}\b", '', string, re.IGNORECASE)
                                elif bank == "bsn":
                                    updated_string = re.sub(r"\b\d{1,2}(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b", '', string, re.IGNORECASE)
                                elif bank == "abi":
                                    updated_string = line[1]
                                elif bank == "RHB":
                                    updated_string = line[1]
                                elif bank == "bank_maumalat":
                                    updated_string = line[1]
                                elif bank == "hongleong":
                                    updated_string = re.sub(fr"\d{{{pos1}}}-\d{{{pos2}}}-\d{{{pos3}}}", '', string)
                                elif bank == "bank_islam":
                                    updated_string = re.sub(r"\d{1,2}/\d{2}/\d{2}", '', string)
                                else:
                                    updated_string = re.sub(fr"\d{{{pos1}}}/\d{{{pos2}}}/\d{{{pos3}}}", '', string)
                            except:
                                updated_string = re.sub(fr"\d{{{pos1}}}/\d{{{pos2}}}", '', string)
                            particular = updated_string

                            cnt = 0
                            while len(formated_data[m + 1]) == 1 and cnt < 4 and len(formated_data[m + 1][0].strip()) < 40:
                                particular += " " + formated_data[m + 1][0]
                                m += 1
                                cnt += 1

                            data["description"] = particular
                            data["reference"] = ""
                    print(data)
                    if match:
                        amount = float(line[len(line) - 1].replace(",", "") if "," in line[len(line) - 1] else line[len(line) - 1])
                        print("amount: ", amount)
                        if amount < float(temp_opening_balance):
                            if "DR" in line[len(line) - params["pos_of_dep_or_with_column_from_right"]]:
                                data["amount"] = float(line[len(line) - params["pos_of_dep_or_with_column_from_right"]-1].replace(",", "").replace("+", "").replace("-", "") if "," or "+" or "-" in line[len(line) - params["pos_of_dep_or_with_column_from_right"]-1] else \
                                line[len(line) - params["pos_of_dep_or_with_column_from_right"]-1])
                            else:
                                data["amount"] = float(line[len(line) - params["pos_of_dep_or_with_column_from_right"]].replace(",", "").replace("+", "").replace("-", "").replace(":", "") if "," or "+" or "-" in line[len(line) - params["pos_of_dep_or_with_column_from_right"]] else \
                                line[len(line) - params["pos_of_dep_or_with_column_from_right"]])

                            data["type"] = "debit"
                            total_debit_amount += float(data["amount"])
                            data["balance"] = float(line[len(line) - 1].replace(",", "") if "," in line[len(line) - 1] else line[
                                len(line) - 1])
                            temp_opening_balance = amount
                            print("debit block: ", data["amount"], amount, line)
                        else:
                            try:
                                if "DR" in str(line[len(line) - params["pos_of_dep_or_with_column_from_right"]]):
                                    # print(line[len(line) - params["pos_of_dep_or_with_column_from_right"]])
                                    data["amount"] = float(line[len(line) - params["pos_of_dep_or_with_column_from_right"]-1].replace(",", "").replace("+", "").replace("-", "") if "," or "+" or "-" in line[len(line) - params["pos_of_dep_or_with_column_from_right"]-1] else \
                                    line[len(line) - params["pos_of_dep_or_with_column_from_right"]-1])
                                else:
                                    print("AMOUNT: ", line[len(line) - 2])
                                    data["amount"] = float(line[len(line) - params["pos_of_dep_or_with_column_from_right"]].replace(",", "").replace("+", "").replace("-", "").replace('"', "").replace(":", "") if "," or "+" or "-" in line[len(line) - params["pos_of_dep_or_with_column_from_right"]] else line[
                                    len(line) - params["pos_of_dep_or_with_column_from_right"]])

                                data["type"] = "credit"
                                total_credit_amount += float(data["amount"])
                                data["balance"] = float(line[len(line) - 1].replace(",", "") if "," in line[len(line) - 1] else line[
                                    len(line) - 1])
                                temp_opening_balance = amount
                                print("credit block: ", data["amount"], amount, line)
                            except:
                                pass

                        # recognise category of transection
                        # data["category"] = categories.categorize_transection(data["particulars"])
                        # data["expense_type"] = categories.categorize_expenses(data["particulars"])
                transections.append(data)

    # Adding name and address
    name = formated_data[0]
    address = ''
    for item in formated_data[1:]:
        if isinstance(item, str):
            address += ' ' + str(item)
        else:
            break

    filtered_data = [d for d in transections if d]
    address = address.strip()
    total_data['name'] = name
    total_data['address'] = address
    print("filtered_data: ", filtered_data)
    # total_data["total_credited_amount"] = total_credit_amount
    # total_data["total_debited_amount"] = total_debit_amount
    statement_from = filtered_data[0]["date"]
    statement_to = filtered_data[len(filtered_data)-1]["date"]

    # categoriesWiseAnalysis = categories.find_total_categories(filtered_data, "category")
    # typeWiseAnalysis = categories.find_total_categories(filtered_data, "type")
    # typeWiseAnalysis["total"] = len(filtered_data)
    # dateWiseAnalysis = categories.find_total_datewise(filtered_data)
    # filtered_debit = [item for item in filtered_data if item['type'] == "debit"]
    # expensesWiseAnalysis = categories.find_total_categories(filtered_debit, "expense_type")
    # top5 = categories.find_top_five(filtered_data)
    # print(filtered_data)
    summary = categories.find_summery(filtered_data, opening_balance)

    # whole_data = {
    #     "error_code": 0,
    #     {
    #     "customerInfo": total_data,
    #     "statementData": filtered_data,
    #     "categoriesWiseAnalysis": categoriesWiseAnalysis,
    #     "typeWiseAnalysis": typeWiseAnalysis,
    #     "dateWiseAnalysis": dateWiseAnalysis,
    #     "expensesWiseAnalysis": expensesWiseAnalysis,
    #     "top5CreditTransaction": top5["top5CreditTransaction"],
    #     "top5DebitTransaction": top5["top5DebitTransaction"],
    #     "summary": summary
    #     }
    # }
    if "account number" in total_data:
        account_no = total_data["account number"]
    elif "account no / no akaun" in total_data:
        account_no = total_data["account no / no akaun"]
    elif "account no" in total_data:
        account_no = total_data["account no"]
    else:
        account_no = ""

    whole_data = {
        "error_code": 0,
        "response": {
            "customer_info": {
                "account_number": [account_no],
                "address": [total_data['address']],
                "name": [total_data["name"]],
                "statement_from": statement_from,
                "statement_to": statement_to
            },
            "statements": filtered_data,
            "summary": summary
        },
        "result": "success"
    }
    # logger.info("data found in bank statement")
    return whole_data


