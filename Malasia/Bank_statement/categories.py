categories = ["AUTOPAY","JomPAY", "IBG", "FPX", "MEPS", 'UPI', 'NEFT', 'IMPS', 'RTGS', 'ATM', 'SALARY', 'CASH', 'EMI', 'LOAN', 'POS', 'CHEQUE', 'CARD']
expenseCategories = {
    "FOOD": ['SWIGGY', 'FOOD', 'ZOMATO', 'DOORDASH', 'KFC', 'G2DEAL', 'UBEREAT', 'GRUBHUB', 'MACDONALDS', 'PIZZAHUT', 'BEHROUZ', 'FAASOS', 'BIRYANI', 'BURGER', 'SUBWAY', 'BREAKFAST', 'DHABA', 'PANDA', 'DINER', 'DINING',
           "Grab Superapp","Snacks", "FoodPanda", "McDonald's", "Air Asia Super App", "Pop Meals", "KFC Malaysia", "Easi My", "Halo Delivery", "Lolol", "DeliveryEat", "Beep", "Tapau", "FoodTime", "NMooMoo", "Odamakan"],
    "TRAVEL": ['TRAVEL', 'IRTC', 'AIRTRAVEL', 'BUS', 'RAIL', 'TRAIN', 'FERRY', 'TAXI', 'CAB', 'RIDE',],
    "ENTERTAINMENT": ['ENTERTAINMENT', 'MOVIE', 'THEATER', 'CINEMA', 'BOOK', 'MUSIC', 'SHOW', "Club"],
    "BILL PAYMENT": ['Maxis', 'Celcom', 'U Mobile','RELOADMOBILE', "mobile", 'Tune Talk', 'Yes', 'redONE', 'Altel', 'Unifi Mobile', 'TM (Telekom Malaysia)', 'Maxis Fibre', 'TIME Internet', 'Celcom Home Broadband', 'Digi Home Broadband', 'Astro IPTV',
    'Astro', 'HyppTV', 'ABNxcess', 'MNC Vision','Tenaga Nasional Berhad (TNB)', 'Syarikat Air Melaka Berhad', 'Indah Water Konsortium', 'GrabPay', 'Touch \'n Go eWallet', 'Boost', 'BigPay', 'FavePay', 'ShopeePay', 'Lazada Wallet',
    'Maybank QRPay', 'CIMB Pay','RECHARGE', 'DTH', 'ELECTRICITY', 'GAS', 'WATER', 'AIRTEL', 'IDEA', 'MYVI', 'JIO', 'VODAFONE', 'AIRCEL', 'TATASKY', 'D2H', 'FIBER', 'WIFI', 'CABLE'],

    "HEALTH": ['MEDICAL', 'HOSP', 'HOSPITAL', 'DOCTOR', 'PHARMACY', 'LAB', 'OPD', 'CLINIC', 'INSURANCE', 'HEALTH'],

    "GROCERIES": ['HappyFresh', 'Redtick', 'Jaya Grocer', 'Tesco Online', 'MyGroser', 'Lazada Fresh', 'Shopee Mart','PrestoMall Groceries', 'Potboy Groceries', 'Bigbox Asia', 'BeliBeli', 'Mydin Online', 'Bens Independent Grocer',
    'Everleaf', 'Village Grocer', 'Mercato', 'Yeoh Organic', 'PurelyB', 'Honestbee', 'Malaysia Supermarket Online','GROCERIES', 'GROCERY', 'BIGBASKET', 'JIOMART', 'FRESH', 'CHICKEN', 'MEAT', 'VEGTBLE', 'DAIRY', 'FRUITS',
             'VEGETABLES', 'POUDRIER', 'MILK', 'PANTRY', 'DMART', 'FARMER'],

    "EDUCATION": ['EDUCATION', 'SCHOOL', 'COLLEGE', 'UNIVERSITY', 'BOOKS', 'LIBRARY', 'COURSE', 'EDU', 'UDEMY', 'COURSERA',
             'SKILLSHARE', 'UDACITY', 'EDX', 'CODE', 'CODEACADEMY', 'MASTERCLASS'],
    "HOME": ['HOME', 'HOMEAPPL', 'HOMEFURN', 'HOMEFURNITURE', 'FURNITURE', 'DECOR', 'PAINT', 'FABRIC', 'KITCHEN', "Rent", "Housing", "Accommodation"],
    "TAXES": ['TAX', 'TAXES', 'GSTN'],
    "HOTEL": ['HOTEL', 'HOTELS', 'HOTELBOOKING', 'BOOKING', "restaurants", "restaurant"],
    # "ATM withdrawal": ["ATM", "atm", "Atm withdrawal", "ATM WITHDRAWAL"],
    "FUND transfer": ["FUND transfer", "transfer"],
    "SHOPPING": ['Lazada', 'Shopee', 'Zalora', '11street', 'Lelong', 'PrestoMall', 'PGMall', 'GEMFIVE','FashionValet', 'Hermo', 'Ezbuy', 'Qoo10', 'Zilingo', 'Taobao', 'AliExpress', 'Amazon',
    'eBay', 'ShopBack', 'Carousell', 'Mudah.my','SHOPPING', 'SHOP', 'STORE', 'AMAZON', 'FLIPKART','SNAPDEAL', 'AJIO', 'MYNTRA', 'RELIANCE', 'FASHION', 'CLOTHES', 'FURNITURE'],
}


# Function to categorize a particular transaction
def categorize_expenses(transaction):
    for category, keywords in expenseCategories.items():
        for keyword in keywords:
            if keyword.lower() in transaction.lower():
                return category
    return "other"


def categorize_transection(transection):
    for cat in categories:
        if cat.lower() in transection.lower():
            return cat
    return "other"


# Total no of transection in different category
def find_total_categories(transections, keyword):
    # Group transactions by amount, particulars, and date
    transactions_by_key = {}
    for transaction in transections:
        key = (transaction[keyword])
        if key in transactions_by_key:
            transactions_by_key[key].append(transaction)
        else:
            transactions_by_key[key] = [transaction]
    print(transactions_by_key)
    # Dictionary to store the count and total amount for each category
    if keyword == "expense_type":
        result = {}
        for category, transactions in transactions_by_key.items():
            count = len(transactions)
            total_amount = sum(float(transaction['amount']) for transaction in transactions)
            result[category] = {"count": count, "amount": total_amount}
        print(result)
    else:
        # Convert each value to its corresponding length
        result = {key: len(value) for key, value in transactions_by_key.items()}
    return result


# Total no of transection datewise
def find_total_datewise(transections):
    # Group transactions by amount, particulars, and date
    transactions_by_key = {}
    for transaction in transections:
        key = (transaction['date'])
        if key in transactions_by_key:
            transactions_by_key[key].append(transaction)
        else:
            transactions_by_key[key] = [transaction]
    print(transactions_by_key)

    # Initialize a dictionary to store totals for each date
    totals_by_date = {}
    # Iterate through the data dictionary and calculate totals for each date
    for date, transactions in transactions_by_key.items():
        credit_total = 0
        debit_total = 0
        amount_total = 0
        balance = 0

        for transaction in transactions:
            amount = float(transaction['amount'].strip())
            if transaction['type'] == 'credit':
                credit_total += amount
            elif transaction['type'] == 'debit':
                debit_total += amount

            amount_total += amount
            balance = transaction['balance']

        totals_by_date[date] = {
            'total': amount_total,
            'credit': credit_total,
            'debit': debit_total,
            'balance': balance
        }
    return totals_by_date


# to fimd top 5 credit and debit transections
def find_top_five(transections):
    # Separate credit and debit transactions
    credit_transactions = [item for item in transections if item['type'] == 'credit']
    debit_transactions = [item for item in transections if item['type'] == 'debit']

    # Sort transactions by amount (descending order)
    sorted_credit_transactions = sorted(credit_transactions, key=lambda x: float(x['amount']), reverse=True)
    sorted_debit_transactions = sorted(debit_transactions, key=lambda x: float(x['amount']), reverse=True)

    # Get the top 5 credit and debit transactions
    top_5_credit_transactions = sorted_credit_transactions[:5]
    top_5_debit_transactions = sorted_debit_transactions[:5]

    return {"top5DebitTransaction": top_5_debit_transactions,
            "top5CreditTransaction": top_5_credit_transactions}


def find_summery(transections, opening_balance):
    # Separate credit and debit transactions
    print("transections: ", transections)
    credit_transactions = [item for item in transections if item['type'] == 'credit']
    debit_transactions = [item for item in transections if item['type'] == 'debit']

    # Calculate the total amount for credit transactions
    total_credit_amount = sum(float(item['amount']) for item in credit_transactions)

    # Calculate the total amount for debit transactions
    total_debit_amount = sum(float(item['amount']) for item in debit_transactions)
    print(debit_transactions)

    return {
        "Closing_balance": float(transections[len(transections)-1]["balance"]),
        "Credits": float(total_credit_amount),
        "Debits": float(total_debit_amount),
        "Opening_balance": float(opening_balance)
    }