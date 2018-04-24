import re
from datetime import datetime as dt
from difflib import get_close_matches


ITEM_REGEX = r'((^|[\n])([\w]|[\s]|[.-]|[\/]|[0-9]{1},[0-9]{1}[A-Z])*([\d,\d]*|[xX\*])[\s]*[xX\*]([\s]|([,]*))([\d,.]*))'


def get_receipt_wordlist(receipt):
    return receipt.replace('\n', ' ').split(" ")


def get_seller_name(receipt):
    receipt_space = receipt.split("\n")
    if receipt_space[0] == '':
        return receipt_space[1]
    else:
        return receipt_space[0]


def get_receipt_date(receipt):
    date_regex = re.search(r'\d{4}\-(0?[1-9]|1[012])\-(0?[0-9]|[12][0-9]|3[01])*', receipt)
    date_regex_string = re.search(r'dn.[0-3][0-9]r[0-1][1-9].[0-9]{2}', receipt)
    if date_regex:
        return dt.strptime(date_regex.group(0), '%Y-%m-%d')
    elif date_regex_string:
        return dt.strptime(date_regex_string.group(0), 'dn.%dr%m.%y')
    else:
        return None


def total_amount_check(total):
    return re.match(r'^[0-9]{1,4}(,)[0-9]{2,}', total)


def normalize_amount(amount):
    return float(amount.replace(',', '.'))


def get_total_amount(receipt):
    receipt_wordlist = get_receipt_wordlist(receipt)
    receipt_total_currency_placers = ["pln", "zl", "zł"]
    receipt_total_word_placers = ["suma", "suma:", "razem"]

    for index, word in enumerate(receipt_wordlist):
        word_normalized = word.lower()
        if word_normalized in receipt_total_currency_placers:
            possible_total_amount = receipt_wordlist[index + 1]
            if total_amount_check(possible_total_amount):
                return normalize_amount(possible_total_amount)
            else:
                return None
        else:
            possible_total_amount = receipt_wordlist[index + 2]
            if word_normalized in receipt_total_word_placers and receipt_wordlist[index + 1].lower() != "ptu":
                if total_amount_check(possible_total_amount):
                    return normalize_amount(possible_total_amount)
                else:
                    for n in range(index + 1, index + 6):
                        if total_amount_check(receipt_wordlist[n]):
                            return normalize_amount(receipt_wordlist[n])


def get_payment_method(receipt):
    wordlist = get_receipt_wordlist(receipt)
    method_result = 2
    for word in wordlist:
        card_payment = ['karta']
        cash_payment = ['gotówka', 'gotowka']
        card_match = get_close_matches(word.lower(), card_payment, cutoff=0.8)
        cash_match = get_close_matches(word.lower(), cash_payment, cutoff=0.7)

        if card_match:
            method_result = 1

        elif cash_match:
            method_result = 0

    return method_result


def get_item_content(receipt):
    wordlist = get_receipt_wordlist(receipt)
    start_cut_receipt = receipt
    start_cut_receipt_content = []
    final_receipt_content = []

    for index, word in enumerate(wordlist):
        item_start_patterns = ['fiskalny']
        item_end_patterns = ['sprzed', 'kw.op']
        get_start_receipt_match = get_close_matches(word.lower(), item_start_patterns)
        get_end_receipt_match = get_close_matches(word.lower(), item_end_patterns)

        if get_start_receipt_match:
            start_cut_receipt = receipt.split(word)[1]
            start_cut_receipt_content.append(start_cut_receipt)

        if get_end_receipt_match:
            end_cut_receipt = start_cut_receipt.split(word)[0]
            final_receipt_content.append(end_cut_receipt)

    if final_receipt_content:
        return final_receipt_content[0]

    elif start_cut_receipt_content:
        return start_cut_receipt_content[0]

    else:
        return None


def get_items(receipt):
    item_content = get_item_content(receipt)
    item_match = re.findall(ITEM_REGEX, item_content)
    items = []

    for item in item_match:
        item_elements = []
        item_name = re.match(r'(.*^)[^xX,\n]*', item[0].strip())
        item_elements.append(item_name.group(0))
        for index, element in enumerate(item):
            if element not in ['', '\n', ' ']:
                if re.match(r'(,[\d]*)', element):
                    amount_conversion = element.replace(',', '')
                    item_elements[2] = '.'.join([item[index - 1], amount_conversion])
                elif re.match(r'([0-9]{1,},[0-9]{1,})', element):
                    price_conversion = element.replace(',', '.')
                    item_elements.append(price_conversion)
                else:
                    item_elements.append(element)

        items.append(item_elements)
    return items
