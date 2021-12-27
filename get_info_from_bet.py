from bs4 import BeautifulSoup

import conversion_val

def format_string(s: str):
    s = s.strip()
    category_name = s
    rep = [" "]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    key = category_name
    return key


def get_info_from_bet_1(content_from_page):

    soup = BeautifulSoup(content_from_page, 'lxml')

    id = 'Элемент не найден'
    try:
        id = soup.find('div', class_='bet-confirmation-header-ref').text
        id = format_string(id)
    except Exception as er:
        print(er)
        pass

    data_day = 'Элемент не найден'
    data_time = 'Элемент не найден'
    try:
        data_text = soup.find('div', class_='bet-confirmation-header-datetime').text
        data_text = data_text.strip()
        data_content = data_text.split(' ')
        data_day = format_string(data_content[0])
        data_time = format_string(data_content[-1])
    except Exception as er:
        print(er)
        pass

    selectionname = 'Элемент не найден'  # 1 строка под заголовком
    try:
        selectionname = soup.find('div', class_='bet-confirmation-details-row-selectionname').text
        selectionname = format_string(selectionname)
    except Exception as er:
        print(er)
        pass

    exodus_ = 'Элемент не найден'  # исход события, строка после описания
    try:
        exodus_ = soup.find('div', class_='bet-confirmation-details-row-plbtdescription').text
        exodus_ = format_string(exodus_)
    except Exception as er:
        print(er)
        pass

    row_odds = 'Элемент не найден'  # коэффициент
    try:
        row_odds = soup.find('div', class_='bet-confirmation-details-row-odds').text
        row_odds = format_string(row_odds)

        row_odds = conversion_val.row_odds_convert(row_odds)
    except Exception as er:
        print(er)
        pass

    row_eventname = 'Элемент не найден'  # информация о командах
    try:
        row_eventname = soup.find('div', class_='bet-confirmation-details-row-eventname').text
        row_eventname = format_string(row_eventname)
    except Exception as er:
        print(er)
        pass

    game_or_not = 'Элемент не найден'  # сыграла не сыграла
    try:
        game_or_not = soup.find('div', class_='bet-confirmation-details-row-status').text
        game_or_not = format_string(game_or_not)
    except Exception as er:
        print(er)
        pass

    value_bet = 'Элемент не найден'  # общий размер ставки
    try:
        value_bet = soup.find('td', class_='bet-confirmation-info-table-value-top').text
        value_bet = format_string(value_bet)

        value_bet = conversion_val.value_bet_convert(value_bet)
        value_bet = conversion_val.only_no_val(value_bet)
    except Exception as er:
        print(er)
        pass

    return_value = 'Элемент не найден'  # общий размер ставки
    try:
        return_value = soup.find('td',
                                 class_='bet-confirmation-info-table-value bet-confirmation-info-table-value-single').text
        return_value = format_string(return_value)

        return_value = conversion_val.return_val_convert(return_value)
        return_value = conversion_val.only_no_val(return_value)
    except Exception as er:
        print(er)
        pass

    content1 = {
        "код ставки": id,
        "дата": data_day,
        "время": data_time,
        "название команды-победителя": selectionname,
        "коэффициент": row_odds,
        "название команд общее": row_eventname,
        "победа/поражение": game_or_not,
        "сумма ставки": value_bet,
        "сумма выигрыша": return_value,
        "исход": exodus_
    }

    return content1