from chrome_driver import GetWorkAccountsList, FireFoxDriverMainNoAutoOpen, GetWorkAccountWithHands
from time import sleep
import time
import info
from bs4 import BeautifulSoup
import conversion_val
from multiprocessing.dummy import Pool

import httplib2
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


def log_in_driver(driver_class):
    login = driver_class.bet365_login
    passwd = driver_class.bet365_password
    driver_class.log_in_bet365_v2(login, passwd)


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
    spreadsheetId=info.spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {f"range": f"A{1}:J{1}",
             "majorDimension": "ROWS",
             "values": [["код ставки", "дата", "время", "название команды-победителя", "коэффициент",
                         "название команд общее", "победа/поражение", "сумма ставки", "сумма выигрыша", "исход"]]},

        ]
    }
).execute()



line_for_google = 1
def google_table(line_for_google, a1,a2,a3,a4,a5,a6,a7,a8,a9,a10):
    values = service.spreadsheets().values().batchUpdate(
        spreadsheetId=info.spreadsheet_id,
        body={
            "valueInputOption": "USER_ENTERED",
            "data": [
                {f"range": f"A{line_for_google}:J{line_for_google}",
                 "majorDimension": "ROWS",
                 "values": [[a1,a2,a3,a4,a5,a6,a7,a8,a9,a10]]},

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


def get_new_accounts_from_info(list_of_start_info):
    'Запускаем рабочий аккаунт'
    # запускаем аккаунты
    List_of_bet_account = []
    countries = []
    Set_of_countries = set()

    for i in list_of_start_info:
        countries.append(i[3])

    for i in countries:
        Set_of_countries.add(i)

    Dict_of_Drivers_count = {}

    for i in Set_of_countries:
        Dict_of_Drivers_count[i] = countries.count(i)

    start_time_for_all = time.time()
    for i in Set_of_countries:
        print(f'Открываем {Dict_of_Drivers_count[i]} аккаунта для {i}')
        start_time_for_type = time.time()
        accounts_get_class = GetWorkAccountsList(number_of_accounts=Dict_of_Drivers_count[i], vpn_country=i)
        Accounts = accounts_get_class.return_Browser_List()

        for account_info in list_of_start_info:
            bet365login, bet365password, bet_value, vpn_country = account_info
            if vpn_country != i:
                continue

            driver_class = FireFoxDriverMainNoAutoOpen(
                driver=Accounts.pop(-1),
                login=bet365login,
                password=bet365password,
                bet_value=bet_value,
                vpn_country=vpn_country
            )

            List_of_bet_account.append(driver_class)
        print(f'{Dict_of_Drivers_count[i]} аккаунтов для {i} открыты за {time.time() - start_time_for_type}')

    print(f'Все аккаунты успешно открыты за {time.time() - start_time_for_all}')
    # авторизация аккаунтов
    with Pool(processes=len(List_of_bet_account)) as p:
        p.map(log_in_driver, List_of_bet_account)

    print(f'Все аккаунты успешно авторизованы!')

    return List_of_bet_account


print(f'Login: {info.user_name} Password: {info.password}')
# driver_class = GetWorkAccountWithHands()
# driver_class = driver_class.get_driver()
#
# # driver_class.log_in_bet365_v2(info.user_name, info.password)
# driver = FireFoxDriverMainNoAutoOpen(
#     driver=driver_class,
#     login=info.user_name,
#     password=info.password,
#     bet_value='0.1',
#     vpn_country='UK'
# )
#

def get_account():
    from selenium import webdriver

    options = webdriver.ChromeOptions()

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    path_to_chromedriver = r'C:\Users\Sergey\PycharmProjects\365_statistika\chromedriver.exe'

    path_to_user_dir = r'C:\Users\Sergey\AppData\Local\Google\Chrome\User Data'
    profile_name = 'Default'
    options.add_argument(f'user-data-dir={path_to_user_dir}')
    options.add_argument(f"profile-directory={profile_name}")

    driver = webdriver.Chrome(options=options)
    input('Войдите в аккаунт и нажмите Enter:')

    return driver


driver = get_account()
input('Аккаунт готов')

# driver1 = get_new_accounts_from_info(
#     [
#         [info.user_name, info.password, '0.1', 'UK']
#     ],
# )
#
# driver1 = driver1[0]
#
# driver = driver1.driver



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

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
while counter < 3:
# while counter < 3 and counter_to_count < 5:
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_class_name('bet365-show-more-button').click()
        sleep(3)
        print(f'Загрузка контента {counter_to_count}')
        counter_to_count += 1

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print(f'Весь контент загружен {counter}!')
            counter += 1
        else:
            counter = 0
        last_height = new_height

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
        # old class
        # value_bet = soup.find('td', class_='bet-confirmation-info-table-value-top').text
        value_bet = soup.find('td', class_='bet-confirmation-amounts-table-value-top').text
        value_bet = format_string(value_bet)

        value_bet = conversion_val.value_bet_convert(value_bet)
        value_bet = conversion_val.only_no_val(value_bet)
    except Exception as er:
        print(er)
        pass


    return_value = 'Элемент не найден'  # общий размер ставки
    try:
        # old class
        # return_value = soup.find('td', class_='bet-confirmation-info-table-value bet-confirmation-info-table-value-single').text
        return_value = soup.find('td', class_='bet-confirmation-amounts-table-value bet-confirmation-amounts-table-value-single').text
        return_value = format_string(return_value)

        return_value = conversion_val.return_val_convert(return_value)
        return_value = conversion_val.only_no_val(return_value)
    except Exception as er:
        print(er)
        pass


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
            "исход": exodus_

        })

        google_table(line_for_google, id, data_day, data_time, selectionname, row_odds, row_eventname,
                     game_or_not, value_bet, return_value, exodus_)
        line_for_google+=1
#
# with open(f"mega.json", "w", encoding="utf-8") as file:
#     json.dump(SportsBetting, file, indent=4, ensure_ascii=False)
#
#

