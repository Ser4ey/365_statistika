import json

from selenium import webdriver
from time import sleep
from info import user_name, password, user_agent, proxy, proxy_login_and_pass, spreadsheet_id, firefox_binary, main_path_to_logs
import random
from bs4 import BeautifulSoup
import lxml
import conversion_val
import get_info_from_bet
import work_with_file


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
            {f"range": f"A{1}:M{1}",
             "majorDimension": "ROWS",
             "values": [["код ставки", "дата", "время", "название команды-победителя", "коэффициент",
                         "название команд общее", "победа/поражение", "сумма ставки", "сумма выигрыша", "исход",
                         "Profit", "Sport", "IsInitiator"]]},

        ]
    }
).execute()



line_for_google = 1
def google_table(line_for_google, a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {f"range": f"A{line_for_google}:M{line_for_google}",
                 "majorDimension": "ROWS",
                 "values": [[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13]]},

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





firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
firefox_capabilities['marionette'] = True

firefox_capabilities['proxy'] = {
    "proxyType": "MANUAL",
    "httpProxy": proxy,
    "ftpProxy": proxy,
    "sslProxy": proxy
}

options = webdriver.FirefoxOptions()
options.set_preference("dom.webdriver.enabled", False)
options.set_preference("dom.webnotifications.enabled", False)
options.set_preference("general.useragent.override", user_agent)

driver = webdriver.Firefox(capabilities=firefox_capabilities,
                             executable_path="geckodriver.exe",
                             firefox_binary=firefox_binary,
                             proxy=proxy,
                             options=options)



sleep(1)
print(proxy_login_and_pass)
driver.get('https://2ip.ru')

input('Введите данные от прокси и нажмите Enter')

driver.get('https://www.bet365.com/#/HO/')
for i in range(10):
    try:

        driver.refresh()
        sleep(0.5)
    except:
        pass

sleep(5)

# вход в аккамунт
while True:
    try:
        driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer').click()
        break
    except:
        sleep(1)


sleep(5)

while True:
    try:
        driver.find_element_by_class_name('lms-StandardLogin_Username').send_keys(user_name)
        sleep(0.7)
        driver.find_element_by_class_name('lms-StandardLogin_Password').send_keys(password)
        sleep(0.7)
        break
    except:
        sleep(1)


driver.find_element_by_class_name('lms-StandardLogin_LoginButton').click()
print('Вы успешно вошли в аккаунт')
sleep(12)

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
sleep(2)

# Получение логов
print('[+] Получение логов')
# A_log = work_with_file.get_info_from_json_file('mega_logs.json')
# A_log = A_log[::-1]
A_log = work_with_file.get_info_from_files(main_path_to_logs)
print('[+] Получение логов завершено')


# загрузка всего контента на странице
counter = 0
counter_to_count = 1
while counter < 3:
# while counter < 3 and counter_to_count < 30:
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


# Сокращение логов
Team_list = []
for link1 in link_list[0:10]:
    try:
        driver.get(link1)
        sleep(1)
    except Exception as er:
        print(er)
        print('()()()Блок пропущен()()()')
        continue
    sleep(1)
    page_content = driver.page_source
    content1 = get_info_from_bet.get_info_from_bet_1(page_content)
    Team_list.append(content1["название команд общее"])

A_log = work_with_file.first_list_execute(A_log, Team_list)



# Проверка всех блоков
print('[+] Начало записи в таблицу')
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


    content1 = get_info_from_bet.get_info_from_bet_1(page_content)

    id = content1["код ставки"]
    data_day = content1["дата"]
    data_time = content1["время"]
    selectionname = content1["название команды-победителя"]
    row_odds = content1["коэффициент"]
    row_eventname = content1["название команд общее"]
    game_or_not = content1["победа/поражение"]
    value_bet = content1["сумма ставки"]
    return_value = content1["сумма выигрыша"]
    exodus_ = content1["исход"]


    if id == 'Элемент не найден':
        print('Задание не действительно')
        continue


    # получение данных из лога
    log_main, A_log = work_with_file.find_bet_for_team_and_remove_it(content1["название команд общее"], A_log)

    print('-'*30)
    print(data_day, data_time, '-', row_eventname)
    time_log, team1, Profit1, Sport1, IsInitiator1 = work_with_file.get_info_from_bet_log(log_main)
    print(time_log.split(' ')[0], '-', team1, Profit1, Sport1, IsInitiator1)
    print('-' * 30)
    # input('Нажмите Enter для родолжения')




    SportsBetting.append({
        "код ставки": id,
        "дата": data_day,
        "время": data_time,
        "название команды-победителя": selectionname,
        "коэффициент": row_odds,
        "название команд общее": row_eventname,
        "победа/поражение": game_or_not,
        "сумма ставки": value_bet,
        "сумма выигрыша": return_value,
        "исход": exodus_,
        "Profit": Profit1,
        'Sport': Sport1,
        'IsInitiator': IsInitiator1

    })

    google_table(line_for_google, id, data_day, data_time, selectionname, row_odds, row_eventname,
                    game_or_not, value_bet, return_value, exodus_, Profit1, Sport1, IsInitiator1)
    line_for_google+=1

with open(f"mega.json", "w", encoding="utf-8") as file:
    json.dump(SportsBetting, file, indent=4, ensure_ascii=False)


print('[+] Парсинг завершён')


