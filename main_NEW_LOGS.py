import json

import info
import work_with_my_logs
from selenium import webdriver
from time import sleep
from info import user_name, password, user_agent, proxy, proxy_login_and_pass, spreadsheet_id, firefox_binary
import random
from bs4 import BeautifulSoup
import lxml
import conversion_val


import httplib2
# import apiclient.discovery
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
# spreadsheet_id = 'id то таблицы'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = discovery.build('sheets', 'v4', http = httpAuth)


values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {f"range": f"A{1}:V{1}",
             "majorDimension": "ROWS",
             "values": [["код ставки", "дата", "время", "название команды-победителя", "коэффициент",
                         "название команд общее", "победа/поражение", "сумма ставки", "сумма выигрыша", "исход",


                        'вид спорта', 'процент вилки', 'время жизни вилки', 'название противоположной бк',
                         'команда 1', 'команда 2', 'вид ставки', 'коэффициент на Bet365', 'количество инициаторов у Bet365',
                         'коэффициент противоположной БК', 'количество инициаторов противоположной БК', 'кто является инициатором'

                         ]]},

        ]
    }
).execute()



line_for_google = 1
def google_table(line_for_google, a1,a2,a3,a4,a5,a6,a7,a8,a9,a10, m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {f"range": f"A{line_for_google}:V{line_for_google}",
                 "majorDimension": "ROWS",
                 "values": [[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,m1, m2, m3, m4, m5, m6, m7, m8, m9, m10, m11, m12]]},

            ]
        }
    ).execute()
line_for_google+=1





def format_string(s: str):
    s = s.strip()
    category_name = s
    rep = [" "]
    for item in rep:
        if item in category_name:
            category_name = category_name.replace(item, "_")
    key = category_name
    return key


# Загрузка информации из логов .csv
my_log_master = work_with_my_logs.Work_With_My_Logs()


driver = work_with_my_logs.FireFoxDriverWithVPN()
driver.log_in_bet365(info.user_name, info.password, '0')

driver = driver.driver


# firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
# firefox_capabilities['marionette'] = True
#
# firefox_capabilities['proxy'] = {
#     "proxyType": "MANUAL",
#     "httpProxy": proxy,
#     "ftpProxy": proxy,
#     "sslProxy": proxy
# }
#
# options = webdriver.FirefoxOptions()
# options.set_preference("dom.webdriver.enabled", False)
# options.set_preference("dom.webnotifications.enabled", False)
# options.set_preference("general.useragent.override", user_agent)
#
# driver = webdriver.Firefox(capabilities=firefox_capabilities,
#                              executable_path="geckodriver.exe",
#                              firefox_binary=firefox_binary,
#                              proxy=proxy,
#                              options=options)
#
#
#
# sleep(1)
# print(proxy_login_and_pass)
# driver.get('https://2ip.ru')
#
# input('Введите данные от прокси и нажмите Enter')
#
#
# driver.get('https://www.bet365.com/#/HO/')
#
# for i in range(10):
#     try:
#         driver.refresh()
#         sleep(0.5)
#     except:
#         pass
#
#
# sleep(5)
#
# # вход в аккамунт
# while True:
#     try:
#         driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer').click()
#         break
#     except:
#         sleep(1)
#
#
# sleep(5)
#
# while True:
#     try:
#         driver.find_element_by_class_name('lms-StandardLogin_Username').send_keys(user_name)
#         sleep(0.7)
#         driver.find_element_by_class_name('lms-StandardLogin_Password').send_keys(password)
#         sleep(0.7)
#         break
#     except:
#         sleep(1)
#
#
# driver.find_element_by_class_name('lms-StandardLogin_LoginButton').click()
# print('Вы успешно вошли в аккаунт')
# sleep(12)

try:
    # закрытие всплывающего окна
    driver.find_element_by_class_name('pm-PushTargetedMessageOverlay_CloseButton').click()
    sleep(2)
except:
    pass

driver.get('https://members.bet365.com/he/Authenticated/History/DateRangeSelection/?=&ht=4')
sleep(10)

# создание запроса


import datetime

today = datetime.datetime.now().date()
d = datetime.timedelta(days = 178)
a = today - d
a = str(a)
A = a.split('-')
a = A[-1] + '/' + A[-2]+ '/' + A[-3]


today = datetime.datetime.now().date()

# При ошибке увеличте значение переменной ниже на 1
d = datetime.timedelta(days = 1)
data_today = today - d
data_today = str(data_today)
A = data_today.split('-')
data_today = A[-1] + '/' + A[-2]+ '/' + A[-3]

# data_today = driver.find_element_by_id('ctl00_Main_ctl00_ctlDateRangePicker_lblToDate').text
# print(data_today)
# sleep(10)

url = f'https://members.bet365.com/members/Services/History/SportsHistory/HistorySearch/?BetStatus=0&SearchScope=3&datefrom={a} 00:00:00&dateto={data_today} 23:59:59&displaymode=Mobile'

# url = f'https://members.bet365.com/members/Services/History/SportsHistory/HistorySearch/?BetStatus=0&SearchScope=3&datefrom=06/10/2020 00:00:00&dateto=24/02/2021 23:59:59&displaymode=Mobile'
# url = f'https://members.bet365.com/members/Services/History/SportsHistory/HistorySearch/?BetStatus=0&SearchScope=3&datefrom=01/09/2020 00:00:00&dateto=24/02/2021 23:59:59&displaymode=Mobile'

print(url)


driver.get(url)
sleep(12)



# input('Введите enter')
# загрузка всего контента на странице

counter = 0
counter_to_count = 1
while counter < 3:
# while counter < 3 and counter_to_count < 5:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_class_name('bet365-show-more-button').click()
        sleep(3)
        counter = 0

        print(f'Загрузка контента {counter_to_count}')
        counter_to_count+=1

    except Exception as er:
        counter += 1
        sleep(1)
        print(er)
print(f'Загрузка контента завершена')



# list_of_blocks = driver.find_elements_by_class_name('bet-summary')
SportsBetting = []



page_content = driver.page_source
soup = BeautifulSoup(page_content, 'lxml')

blocks_list = soup.find_all('div', class_='bet-summary')

link_list = []


for block1 in blocks_list:
    data_betid = block1.get("data-betid")
    data_bash = block1.get("data-bash")
    link = f"https://members.bet365.com/members/services/History/SportsHistory/GetBetConfirmation?displaymode=mobile&_=1614152844166&Id={data_betid}&BetStatus=0&Bcar=0&Bash={data_bash}&Pebs=0"
    link_list.append(link)

print(link_list)
sleep(5)

# Проверка всех блоков
counter = 1
for link1 in link_list:


    print(f'Проверка блока {counter} из {len(link_list)}')
    counter += 1

    try:
        driver.get(link1)
        sleep(1)
    except Exception as er:
        print(er)
        print('()()()Блок пропущен()()()')
        continue

    sleep(1)
    page_content = driver.page_source

    soup = BeautifulSoup(page_content, 'lxml')


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


    selectionname = 'Элемент не найден' #1 строка под заголовком
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


    row_odds = 'Элемент не найден' #коэффициент
    try:
        row_odds = soup.find('div', class_='bet-confirmation-details-row-odds').text
        row_odds = format_string(row_odds)

        row_odds = conversion_val.row_odds_convert(row_odds)
    except Exception as er:
        print(er)
        pass


    row_eventname = 'Элемент не найден' #информация о командах
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
        return_value = soup.find('td', class_='bet-confirmation-info-table-value bet-confirmation-info-table-value-single').text
        return_value = format_string(return_value)

        return_value = conversion_val.return_val_convert(return_value)
        return_value = conversion_val.only_no_val(return_value)
    except Exception as er:
        print(er)
        pass

    my_logs_data = my_log_master.get_info(row_eventname)
    print(my_logs_data)

    print(id)
    print(data_day)
    print(data_time)
    print(selectionname)
    print(row_odds)
    print(row_eventname)
    print(game_or_not)
    print(value_bet)
    print(return_value)
    print(exodus_)


    if id == 'Элемент не найден':
        print('Задание не действительно')
    else:

        # SportsBetting.append({
        #     "код ставки": id,
        #     "дата": data_day,
        #     "время": data_time,
        #     "название команды-победителя": selectionname,
        #     "коэффициент": row_odds,
        #     "название команд общее": row_eventname,
        #     "победа/поражение": game_or_not,
        #     "сумма ставки": value_bet,
        #     "сумма выигрыша": return_value,
        #     "исход": exodus_
        #
        # })



        google_table(line_for_google, id, data_day, data_time, selectionname, row_odds, row_eventname,
                     game_or_not, value_bet, return_value, exodus_,
                     my_logs_data[0], my_logs_data[1], my_logs_data[2],
                     my_logs_data[3], my_logs_data[4], my_logs_data[5],
                     my_logs_data[6], my_logs_data[7], my_logs_data[8],
                     my_logs_data[9], my_logs_data[10], my_logs_data[11])
        line_for_google+=1

# with open(f"mega.json", "w", encoding="utf-8") as file:
#     json.dump(SportsBetting, file, indent=4, ensure_ascii=False)



