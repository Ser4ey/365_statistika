from pprint import pprint

import httplib2
# import apiclient.discovery
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials


# Файл, полученный в Google Developer Console
CREDENTIALS_FILE = 'creds.json'
# ID Google Sheets документа (можно взять из его URL)
spreadsheet_id = '1IXg91BEJ2w_yLtIs7ar340u9r6W_jng7tAZRv8eYEo0'

# Авторизуемся и получаем service — экземпляр доступа к API
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    ['https://www.googleapis.com/auth/spreadsheets',
     'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
# service = apiclient.discovery.build('sheets', 'v4', http = httpAuth)
service = discovery.build('sheets', 'v4', http = httpAuth)

# Пример чтения файла
values = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range='A1:E10',
    majorDimension='COLUMNS'
).execute()
pprint(values)

# Пример записи в файл


values = service.spreadsheets().values().batchUpdate(
    spreadsheetId=spreadsheet_id,
    body={
        "valueInputOption": "USER_ENTERED",
        "data": [
            {f"range": f"A{1}:I{1}",
             "majorDimension": "ROWS",
             "values": [["код ставки", "дата", "время", "название команды-победителя", "коэффициент",
                         "название команд общее", "победа/поражение", "сумма ставки", "сумма выигрыша"]]},

        ]
    }
).execute()


