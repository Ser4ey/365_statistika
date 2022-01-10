import time


class LogWorker:
    def __init__(self, path_to_log_file):
        self.path_to_log_file = path_to_log_file
        self.log_info = []

    def write_row_in_log_file(self, row):
        '''row - интерируемый
        [BK1_name, BK2_name, BK1_coef, BK2_coef, BK1_game_name, count_of_BK1_plus_forks, count_of_BK2_plus_forks]
        '''
        with open(self.path_to_log_file, 'a', encoding='utf-8') as file:
            str_row = [str(i) for i in row]

            row_line = '$'.join(str_row) + '\n'
            file.write(row_line)

        print(f'Строка записана: {row_line}')

    def get_all_log_data(self):
        with open(self.path_to_log_file, 'r', encoding='utf-8') as file:
            log_info = file.readlines()
            log_info = [i.strip() for i in log_info if i != '']
        print(log_info)
        return log_info

    def get_info_from_log_string(self, log_string: str):
        # [BK1_name, BK2_name, BK1_coef, BK2_coef, BK1_game_name, count_of_BK1_plus_forks, count_of_BK2_plus_forks]

        log_list = log_string.split('$')
        if len(log_list) < 7:
            print(f'Ошибка в строке лог файла: {log_string}')
            log_list = [0] * 10

        log_dict = {
            'BK1_name': log_list[0],
            'BK2_name': log_list[1],
            'BK1_coef': log_list[2],
            'BK2_coef': log_list[3],
            'BK1_game_name': log_list[4],
            'count_of_BK1_plus_forks': log_list[5],
            'count_of_BK2_plus_forks': log_list[6]

        }

        return log_dict


logWorker1 = LogWorker('logFile.txt')


class WorkWithLog:
    '''Сопастовляет ставке результат из логов'''
    def __init__(self, cleaned_logs):
        # переворачиваем логи, чтоб они шли от новых к старым
        self.logs = cleaned_logs[::-1]

    def get_team1_and_team2(self, game_name):
        team_list = game_name.split(' vs ')
        if len(team_list) < 2:
            print(f'Ошибка при получении команд из: {game_name}')
            return '@@@@@', '@@@@@'
        return team_list[0], team_list[1]


    def get_log_string_by_game_name(self, game_name):
        '''Принимает называние игры а возвращает данные из логов'''
        log_data_string = {
            "БК1": 'не найдено',
            "БК2": 'не найдено',
            "коэффициент на БК2": 'не найдено',
            "количество инициаторов на БК1": 'не найдено',
            "количество инициаторов на БК2": 'не найдено',
        }


        del_counter = 'no'
        for i in range(min(len(self.logs), 30)):
            game_name_in_log_string = self.logs[i]['BK1_game_name']
            team1, team2 = self.get_team1_and_team2(game_name_in_log_string)
            print(team1,'+', team2,'=', game_name)
            if (team1 in game_name) and (team2 in game_name):
                del_counter = i
                break

        if del_counter == 'no':
            print('Ставка не найдена')
            return log_data_string

        log_string = self.logs[del_counter]
        self.logs = self.logs[del_counter+1:]

        log_data_string = {
            "БК1": log_string['BK1_name'],
            "БК2": log_string['BK2_name'],
            "коэффициент на БК2": log_string['BK2_coef'],
            "количество инициаторов на БК1": log_string['count_of_BK1_plus_forks'],
            "количество инициаторов на БК2": log_string['count_of_BK2_plus_forks'],
        }
        return log_data_string



log_data = logWorker1.get_all_log_data()
log_clean_data = [logWorker1.get_info_from_log_string(i) for i in log_data]

workWithLog1 = WorkWithLog(log_clean_data)



