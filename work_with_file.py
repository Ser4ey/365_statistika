import os
import json
import difflib

def format_team(team: str):
    '''Возвращает название команд в нормальном формате'''
#     Guadalupe FC v Cartagines_13/03/2021 - убираем дату из этой записи
    team1 = team.strip()
    team1 = team1.split('_')
    team1 = team1[:-1]
    team1 = '_'.join(team1)

    # заменяем v и _ на vs
    team1 = team1.split(' ')
    for i in range(len(team1)):
        if team1[i] == '@' or team1[i] == 'v':
            team1[i] = 'vs'

    team1 = ' '.join(team1)

    return team1


def get_info_from_files(main_path):
    '''
    Возврашает отсортированный масив со ставками
    Вся информация берётся из файлов
    '''

    def sort_def(a: str):
        a = a.strip()
        return int(a)

    def get_files(path):
        dir1 = os.listdir(path)
        dir1.sort(key=sort_def)
        return dir1


    dir1 = get_files(main_path)
    dir1.remove('Breaked')

    List_of_Log = []

    for i in range(len(dir1)):
        path1 = main_path + '\\' + dir1[i] + r'\Logs'
        List_of_Log.append(path1)


    List_of_txt_Logs = []
    for i in List_of_Log:
        try:
            dir2 = get_files(i)
        except:
            continue

        for j in dir2:
            List_of_txt_Logs.append(i + '\\' + j + '\\' + 'LogEntry.txt')


    Data_json = []
    counter = 0
    for i in List_of_txt_Logs:
        counter += 1
        try:
            with open(file=i, mode='r', encoding='utf-8') as file:

                j = json.load(file)
                Data_json.append(j)
        except Exception as er:
            print(er)

    A = Data_json
    # переворачиваем массив A (от новых ставок, к старым)
    A = A[::-1]
    return A


def get_info_from_json_file(path_to_json):
    with open(path_to_json, 'r', encoding='utf-8') as file:
        A = json.load(file)

    return A



def find_bet_by_team_name_100_chance(team, A, only_one=True):
    '''Находит команду(ы) по полному совпадению и возврвщает её положение. Если команд не найдено возвращает False'''
    team = format_team(team)

    if only_one:
        for i in range(len(A)):
            Team = A[i]['Fork']['OneBet']['Team']
            if Team == team:
                return i
    else:
        L = []
        for i in range(len(A)):
            Team = A[i]['Fork']['OneBet']['Team']
            if Team == team:
                L.append(i)

        return L

    return False


def find_bet_by_team_name_50_chance(team, A):
    '''Находит первую самую вероятную команду и возврвщает её положение. Если команд не найдено возвращает False'''
    team = format_team(team)

    def similarity(s1, s2):
        normalized1 = str(s1)
        normalized2 = str(s2)
        matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
        return matcher.ratio()


    best = -1
    for i in range(len(A)):
        Team = A[i]['Fork']['OneBet']['Team']
        r = similarity(Team, team)

        if best <= r:
            best = r

    for i in range(len(A)):
        Team = A[i]['Fork']['OneBet']['Team']
        r = similarity(Team, team)

        if best == r:
            return i

    return False


def first_list_execute(A:list, list_of_teams:list):
    '''Сокращает список, удоляя все события до (возвращает новый список)'''
    A1 = A
    for team in list_of_teams:
        last1 = 0
        try:
            b = find_bet_by_team_name_100_chance(team, A)
            if len(b) == 1:
                i = b[0]
                A1 = A[i-last1:]
                return A1
            else:
                last1 += 25
        except:
            continue

    return A1


def find_bet_for_team_and_remove_it(team:str, A:list):
    '''Находит первое совподение команды, со ставкой и возвращает ставку + удоляя её из массива возвращает сокращенный массив.
        Если совпадения не найдено возвращает наиболее вероятный исход'''

    res = find_bet_by_team_name_100_chance(team, A)
    if type(res) == type(0):
        log1 = A[res]
        return log1, A[res+1:]
    else:
        res = find_bet_by_team_name_50_chance(team, A)
        log1 = A[res]
        return log1, A


def get_info_from_bet_log(log1: dict):
    time = 'False'
    team = 'False'
    Profit = 'False'
    Sport = 'False'
    IsInitiator = 'False'

    try:
        time = log1['Fork']['Created']
    except:
        pass

    try:
        team = log1['Fork']['OneBet']['Team']
    except:
        pass

    try:
        Profit = log1['Fork']['Profit']
    except:
        pass

    try:
        Sport = log1['Fork']['Sport']
    except:
        pass

    try:
        IsInitiator = log1['Fork']['OneBet']['IsInitiator']
        IsInitiator = str(IsInitiator)
    except:
        pass


    return time, team, Profit, Sport, IsInitiator
