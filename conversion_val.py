def format_string2(s: str):
    s = s.strip()
    category_name = s
    rep = ["."]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, ",")
    key = category_name
    return key

def format_string_val(s: str):
    s = s.strip()
    category_name = s
    rep = ["£", "$"]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "")
    key = category_name
    return key


def row_odds_convert(r_odds):
    '''Замена точки на запятую в коэффициенте'''
    n = format_string2(r_odds)
    return n


def value_bet_convert(val_bet):
    '''Замена точки на запятую + убрать валюту в сумма ставки'''
    res1 = val_bet

    try:
        n = res1.split(' ')
        n = n[0]
        res1 = n
    except Exception as er:
        print(er)

    res1 = format_string2(res1)
    res1 = format_string_val(res1)
    return res1


def return_val_convert(val_bet):
    '''Замена точки на запятую + изминения формата вывода итоговой суммы выигрыша'''
    res1 = val_bet

    try:
        n = res1.split(' ')
        n = n[1]
        res1 = n
    except Exception as er:
        print(er)

    res1 = format_string2(res1)
    return res1

def only_no_val(s: str):
    '''Убрать всё, кроме цифр'''
    s = s.strip()
    good_s = ''
    set_of_s = '1234567890,'

    for i in s:
        if i in set_of_s:
            good_s += i
    return good_s