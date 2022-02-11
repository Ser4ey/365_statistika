import pickle
import threading
import selenium
from selenium import webdriver
import time
import random
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from multiprocessing.dummy import Pool
import info


class FireFoxDriverMain:
    def __init__(self, bet_value):
        self.is_VPN = True
        # аккаунт рабочий, если значение меняется на False, то аккаунт закрывается
        self.is_valud_account = True
        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        fp = webdriver.FirefoxProfile(info.firefox_profile_path)
        fp.set_preference("browser.privatebrowsing.autostart", True)

        options = webdriver.FirefoxOptions()
        options.add_argument("-private")
        options.set_preference("dom.webdriver.enabled", False)
        options.set_preference("dom.webnotifications.enabled", False)
        binary = info.firefox_binary
        options.binary = binary

        driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp,
                                   firefox_binary=info.firefox_binary,
                                   executable_path=info.path_to_geckodriver,
                                   options=options)

        self.driver = driver
        self.bet_value = bet_value

    def try_click_many_class(self, class_list):
        if len(class_list) == 0:
            return 'Не удалось нажать не на один из classov'

        try:
            click_element = class_list.pop(0)
            self.driver.find_element_by_class_name(click_element).click()
            return 'Успешное нажатие на класс'
        except:
            self.try_click_many_class(class_list)

    def try_get_text_many_class(self, class_list):
        if len(class_list) == 0:
            print('Не удалось get text не на один из classov')
            return 'Не удалось get text не на один из classov'

        try:
            click_element = class_list.pop(0)
            return self.driver.find_element_by_class_name(click_element).text
        except:
            self.try_click_many_class(class_list)

    def open_bet365com(self):
        time.sleep(7)
        # self.driver.get('https://2ip.ru/')
        self.driver.set_page_load_timeout(10)
        try:
            self.driver.get('https://www.bet365.com/')
            self.driver.set_page_load_timeout(25)
            try:
                time.sleep(5)
                self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
            except:
                return 'Сайт bet365 не загрузился'
            return 'Success'
        except:
            pass

        self.driver.set_page_load_timeout(15)

        for i in range(2):
            self.open_new_window_2ip()
            time.sleep(0.3)

        try:
            self.driver.get('https://www.bet365.com/')
            self.driver.set_page_load_timeout(25)
            try:
                time.sleep(5)
                self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
            except:
                return 'Сайт bet365 не загрузился'
            return 'Success'
        except:
            print('Сайт bet365 не загрузился')
            return 'Сайт bet365 не загрузился'

    def open_new_window_2ip(self):
        current_window = self.driver.current_window_handle
        self.driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
        time.sleep(7)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.close()
        self.driver.switch_to.window(current_window)

    def log_in_bet365(self, login, password):
        self.bet365_login = login
        self.bet365_password = password

        try:
            self.driver.get('https://www.bet365.com/')
        except:
            pass

        for i in range(2):
            try:
                try:
                    time.sleep(2)
                    self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
                    break
                except:
                    print('refresh')
                    self.driver.get('https://www.bet365.com/')
            except:
                pass

        print(f'Вход в аккаунт: {login}')
        time.sleep(1.5)
        # вход в аккаунт bet365ru
        try:
            self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer').click()
        except:
            print(f'Не удалось войти в аккаунт {login}!')
            return f'Не удалось войти в аккаунт {login}!'

        time.sleep(2)
        for i in range(10):
            try:
                self.driver.find_element_by_class_name('lms-StandardLogin_Username').send_keys(login)
                time.sleep(0.7)
                self.driver.find_element_by_class_name('lms-StandardLogin_Password').send_keys(password)
                time.sleep(0.7)
                break
            except:
                time.sleep(1)
                print(f'Не удалось войти в аккаунт {login}')
                return

        # new class: 'lms-LoginButton'
        self.driver.find_element_by_class_name('lms-LoginButton').click()
        time.sleep(10)
        self.bet365_account_name = login

        # закрываем новое окно 4 дек 2021
        try:
            time.sleep(3)
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame ')
            self.driver.switch_to.frame(frame)
            # print('open page')
            self.driver.find_element_by_id('accept-button').click()
        except Exception as er:
            # print(er)
            pass
        finally:
            self.driver.switch_to.default_content()

        # закрываем окно с почтой
        try:
            time.sleep(3)
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame')
            self.driver.switch_to.frame(frame)
            # print('open page')
            self.driver.find_element_by_id('RemindMeLater').click()
        except Exception as er:
            # print(er)
            pass
        finally:
            self.driver.switch_to.default_content()

        try:
            time.sleep(3)
            self.driver.find_element_by_class_name('pm-MessageOverlayCloseButton ').click()
        except:
            pass

        print(f'Вы успешно вошли в аккаунт {login}')
        return 'Успешный вход в аккаунт'

    def log_in_bet365_v2(self, login, password):
        self.bet365_login = login
        self.bet365_password = password

        for i in range(2):
            try:
                try:
                    time.sleep(2)
                    self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
                    break
                except:
                    print('refresh')
                    self.driver.get('https://www.bet365.com/')
            except:
                pass

        print(f'Вход в аккаунт: {login}')
        time.sleep(1.5)
        # вход в аккаунт bet365ru
        try:
            self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer').click()
        except:
            print(f'Не удалось войти в аккаунт {login}!')
            return f'Не удалось войти в аккаунт {login}!'

        time.sleep(2)
        for i in range(10):
            try:
                self.driver.find_element_by_class_name('lms-StandardLogin_Username').send_keys(login)
                time.sleep(0.7)
                self.driver.find_element_by_class_name('lms-StandardLogin_Password').send_keys(password)
                time.sleep(0.7)
                break
            except:
                time.sleep(1)
                print(f'Не удалось войти в аккаунт {login}')
                return

        # new class: 'lms-LoginButton' accept-button
        self.driver.find_element_by_class_name('lms-LoginButton').click()
        time.sleep(3)
        self.bet365_account_name = login
        # self.driver.refresh()
        # time.sleep(7)

        # закрываем новое окно 4 дек 2021
        try:
            time.sleep(3)
            print('Close window!')
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame ')
            self.driver.switch_to.frame(frame)
            # print('open page')
            self.driver.find_element_by_class_name('accept-button').click()
        except Exception as er:
            print(er)
            pass
        finally:
            self.driver.switch_to.default_content()

        # закрываем окно с почтой
        try:
            time.sleep(3)
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame')
            self.driver.switch_to.frame(frame)
            # print('open page')
            self.driver.find_element_by_id('RemindMeLater').click()
        except Exception as er:
            # print(er)
            pass
        finally:
            self.driver.switch_to.default_content()

        try:
            time.sleep(3)
            self.driver.find_element_by_class_name('pm-MessageOverlayCloseButton ').click()
        except:
            pass

        print(f'Вы успешно вошли в аккаунт {login}')
        return 'Успешный вход в аккаунт'

    def relogin_in_bet365_if_take_off(self):
        try:
            self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
            print(f'Аккаунт {self.bet365_login} вылетел!')
        except:
            print(f'Аккаунт {self.bet365_login} авторизован')
            return f'Аккаунт {self.bet365_login} авторизован'

        print(f'Повторный вход в аккаунт: {self.bet365_login}')

        for i in range(10):
            try:
                self.driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer').click()
                break
            except:
                print(f'Не удалось войти в аккаунт {self.bet365_login}!')
                time.sleep(2)

        time.sleep(5)
        for i in range(10):
            try:
                self.driver.find_element_by_class_name('lms-StandardLogin_Username').clear()
                time.sleep(0.7)
                self.driver.find_element_by_class_name('lms-StandardLogin_Username').send_keys(self.bet365_login)
                time.sleep(0.7)
                self.driver.find_element_by_class_name('lms-StandardLogin_Password').send_keys(self.bet365_password)
                time.sleep(0.7)
                break
            except:
                time.sleep(1)
                print(f'Не удалось войти в аккаунт {self.bet365_login}')
                return

        self.driver.find_element_by_class_name('lms-LoginButton').click()
        time.sleep(15)

        # закрываем окно с почтой
        try:
            time.sleep(3)
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame')
            self.driver.switch_to.frame(frame)
            # print('open page')
            self.driver.find_element_by_id('RemindMeLater').click()
        except Exception as er:
            # print(er)
            pass
        finally:
            self.driver.switch_to.default_content()

        try:
            time.sleep(5)
            self.driver.find_element_by_class_name('pm-MessageOverlayCloseButton ').click()
        except:
            pass

        print(f'Вы успешно перевошли в аккаунт {self.bet365_login}')
        return f'Вы успешно перевошли в аккаунт {self.bet365_login}'

    def restart_browser_and_bet365_account(self, check_valid=True):
        # проверка, завис-ли сайт bet365

        if check_valid:
            try:
                self.driver.get('https://www.bet365.com/')
            except:
                pass
            time.sleep(5)

            try:
                account_balance = self.driver.find_element_by_class_name('hm-MainHeaderMembersWide_Balance').text
                print(f'Аккаунт: {self.bet365_login} - работает. Баланс: {account_balance}')
                return False
            except:
                print(f'Аккаунт: {self.bet365_login} - завис. Перезапуск браузера!')
                try:
                    self.driver.close()
                    self.driver.quit()
                except:
                    pass
                return True

    def get_balance(self):
        try:
            bet365balance = self.driver.find_element_by_class_name('hm-MainHeaderMembersWide_Balance').text
            return bet365balance
        except:
            return 'Не удалось получить баланс аккаунта'

    def make_a_bet(self, value, coef, element):
        '''Ставит ставку в открывшемся окошечке
        (его нужно предварительно открыть)'''

        time.sleep(1)

        if str(value)[0] == '%':
            value = value[1:]
            value = float(value)
            value = value / 100
            try:
                bet365balance = self.driver.find_element_by_class_name('hm-MainHeaderMembersWide_Balance').text
                bet365balance = bet365balance.replace(',', '')
                bet365balance = bet365balance.replace(' ', '')
                bet365balance = bet365balance.strip()
                bet365balance = bet365balance.strip('£')
                bet365balance = bet365balance.strip('€')
                # €100.00
                bet365balance = bet365balance.replace(' ', '')
                bet365balance = float(bet365balance)
                print(f'Баланс аккаунта {bet365balance}')
            except:
                bet365balance = 10
                print(f'Баланс аккаунта {bet365balance} не найден')

            print(f'bet = {bet365balance} * {value}')
            value = bet365balance * value
            value = round(value, 2)
            print('value:', value)

        # coef_now = self.driver.find_element_by_class_name('bsc-OddsDropdownLabel').text
        coef_now = self.try_get_text_many_class(['lbc-OddsDropdownLabel', 'bsc-OddsDropdownLabel'])
        # lbc-OddsDropdownLabel
        coef_now = float(coef_now)
        print(f'Текущий коэффициент - {coef_now} Нужный коэффициент - {coef}')
        coef = float(coef)
        if coef - coef_now > 0.09:
            print('Коэффициэнт сильно изменился')
            time.sleep(1)
            element.click()
            self.driver.get('https://www.bet365.com/')
            time.sleep(2)
            return

        self.try_click_many_class(['lqb-StakeBox_StakeInput', 'qbs-StakeBox_StakeInput '])
        # self.driver.find_element_by_class_name('lqb-StakeBox_StakeInput ').click()
        # self.driver.find_element_by_class_name('qbs-StakeBox_StakeInput ').click()
        time.sleep(0.3)
        for simvol in str(value):
            self.driver.find_element_by_tag_name("body").send_keys(simvol)
            time.sleep(0.3)
        time.sleep(0.5)
        try:
            # нажимаем на кнопку стандартной ставки
            self.try_click_many_class(['qbs-BetPlacement', 'lqb-BetPlacement'])
            # self.driver.find_element_by_class_name('qbs-BetPlacement').click()
            # self.driver.find_element_by_class_name('lqb-BetPlacement').click()

        except:
            # нажимаем на кнопку ставки, которую нужно одобрить
            try:
                self.try_click_many_class(['qbs-PlaceBetReferButton ', 'lqb-PlaceBetReferButton '])
                # self.driver.find_element_by_class_name('qbs-PlaceBetReferButton ').click()
                # self.driver.find_element_by_class_name('lqb-PlaceBetReferButton ').click()
            except:
                pass

        flag = False

        for i in range(15):
            try:
                self.try_click_many_class(['lqb-QuickBetHeader_DoneButton ', 'qbs-QuickBetHeader_DoneButton '])
                actions = ActionChains(self.driver)
                actions.move_by_offset(100, 100).perform()
                time.sleep(5)
                actions.click().perform()
                print('Закрываем купон!')
                # print('A')*100
                # time.sleep(100)
                # self.driver.find_element_by_class_name('qbs-QuickBetHeader_DoneButton ').click()
                # self.driver.find_element_by_class_name('lqb-QuickBetHeader_DoneButton ').click()
                print('Ставка проставлена!')
                return 'Ставка проставлена!'
            except:
                time.sleep(1)

        print('[-] Не удалось поставить ставку')
        try:
            self.try_click_many_class(['qbs-NormalBetItem_Indicator ', 'lqb-NormalBetItem_Indicator '])
            # self.driver.find_element_by_class_name('qbs-NormalBetItem_Indicator ').click()
            # self.driver.find_element_by_class_name('lqb-NormalBetItem_Indicator ').click()
        except:
            pass

        self.driver.get('https://www.bet365.com/#/HO/')

        time.sleep(2)

    def reanimaite_bet365com(self):
        # попытка закрыть окно неактивности
        try:
            self.driver.find_element_by_class_name('alm-ActivityLimitStayButton ').click()
            time.sleep(2)
        except Exception as er:
            print(f'Нет кнопки закрытия окна неактивности! {er}')

        # попытка закрыть уведомление о сообщениях (2.0 version)
        try:
            self.driver.find_element_by_class_name('pm-MessageOverlayCloseButton ').click()
            time.sleep(2)
        except:
            pass
        # попытка закрыть уведомление о почте (2.0 version)
        try:
            frame = self.driver.find_element_by_class_name('lp-UserNotificationsPopup_Frame')
            self.driver.switch_to.frame(frame)
            self.driver.find_element_by_id('RemindMeLater').click()
        except Exception as er:
            pass
        finally:
            self.driver.switch_to.default_content()

        # попытка закрыть купон
        try:
            self.try_click_many_class(['qbs-NormalBetItem_Indicator ', 'lqb-NormalBetItem_Indicator '])
            time.sleep(2)
        except:
            pass

        self.close_cupon2()

        self.relogin_in_bet365_if_take_off()

    def close_cupon2(self):
        try:
            self.try_click_many_class(['bss-DefaultContent ', 'lbs-DefaultContent'])
            # self.driver.find_element_by_class_name('bss-DefaultContent ').click()
            # lbs-DefaultContent
            time.sleep(1)
            # lbl-ControlBar_RemoveAll
            self.try_click_many_class(['lbl-ControlBar_RemoveAll ', 'bs-ControlBar_RemoveAll '])
            # self.driver.find_element_by_class_name('bs-ControlBar_RemoveAll ').click()
        except Exception as er:
            print(er)

    def make_any_sport_bet(self, sport, url, bet_type, coef):
        # Попытка закрыть окно неактивности
        try:
            # попытка закрыть окно неактивности
            self.driver.find_element_by_class_name('alm-ActivityLimitStayButton ').click()
            time.sleep(0.5)
        except:
            pass

        try:
            # попытка закрыть сообщения
            self.driver.find_element_by_class_name('pm-MessageOverlayCloseButton ').click()
        except:
            pass

        if sport == 'soccer':
            self.make_cyber_football_bet(url, bet_type, coef)
        elif sport == 'basketball':
            self.make_basketball_bet(url, bet_type, coef)
        elif sport == 'table-tennis':
            self.make_table_tennis_bet(url, bet_type, coef)
        elif sport == 'volleyball':
            self.make_volleyball_bet(url, bet_type, coef)
        elif sport == 'badminton':
            self.make_badminton_bet(url, bet_type, coef)
        else:
            print('Неизвестный вид спорта для Bet365')
            return 'Неизвестный вид спорта для Bet365'

    def make_cyber_football_bet(self, url, bet_type, coef):
        bet_value = self.bet_value

        # WIN__P1 | WIN__P2 | WIN__PX
        if bet_type == 'WIN__P1' or bet_type == 'WIN__P2' or bet_type == 'WIN__PX':
            self.make_cyber_football_bet_P1_P2_X(url, bet_type, coef, bet_value)
        elif bet_type == 'WIN__1X' or bet_type == 'WIN__X2' or bet_type == 'WIN__12':
            self.make_cyber_football_bet_double_chance_P1X_XP2_P1P2(url, bet_type, coef, bet_value)
        elif bet_type[:13] == 'TOTALS__UNDER' or bet_type[:12] == 'TOTALS__OVER':
            self.make_cyber_football_bet_totalbet_of_game(url, bet_type, coef, bet_value)
        elif bet_type[:10] == 'P1__TOTALS' or bet_type[:10] == 'P2__TOTALS':
            self.make_cyber_football_bet_totalbet_of_teme_1or2(url, bet_type, coef, bet_value)
        else:
            print('This type not supported now!')

        '''

        elif bet_type[:13] == 'Гола не будет':
            self.make_cyber_football_bet_gola_ne_budet(url, bet_type, coef, bet_value)
        elif bet_type == 'Чет' or bet_type == 'Нечет':
            self.make_cyber_football_bet_odd_or_even(url, bet_type, coef, bet_value)
        elif 'Г1' in bet_type or 'Г2' in bet_type:
            self.make_cyber_football_bet_gandikap_with_3_exists(url, bet_type, coef, bet_value)
        elif 'Ф1' in bet_type or 'Ф2' in bet_type:
            self.make_cyber_football_bet_F1_F2(url, bet_type, coef, bet_value)
        else:
            if 'Команда' in bet_type:
                if 'Тб' in bet_type or 'Тм' in bet_type:
                    self.make_cyber_football_bet_totalbet_of_teme_1or2(url, bet_type, coef, bet_value)
                    return
            if 'Тб' in bet_type or 'Тм' in bet_type:
                self.make_cyber_football_bet_totalbet_of_game(url, bet_type, coef, bet_value)
                return

            print('Неизвестный тип ставки')'''

    def make_cyber_football_bet_P1_P2_X(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку(Победа|Ничья|Поражение) url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')

        bet_element = list_of_bets[0]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != 'Результат основного времени') and (text != 'Fulltime Result'):
            print('Ставка на П1П2Х, указана колонка не результат основного времени!')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            bet_element.click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[0]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        bets = element_with_bets.find_elements_by_class_name('gl-Participant ')

        my_bet_number = 2
        if bet_type == 'WIN__P1':
            my_bet_number = 0
        elif bet_type == 'WIN__P2':
            my_bet_number = -1
        elif bet_type == 'WIN__PX':
            my_bet_number = 1
        else:
            print('Ставка на П1П2Х, неизвестный формат ставки')
            return 'Ставка на П1П2Х, неизвестный формат ставки'

        bets[my_bet_number].click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bets[my_bet_number])

    def make_cyber_football_bet_double_chance_P1X_XP2_P1P2(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку(Двойной шанс) url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == 'Двойной шанс') or (text1 == 'Double Chance'):
                line = i
                print('Ставка двойной шанс найдена')
                break

        bet_element = list_of_bets[line]

        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != 'Двойной шанс') and (text != 'Double Chance'):
            print('Ставка(Двойной шанс) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        bets = element_with_bets.find_elements_by_class_name('gl-Participant ')

        my_bet_number = 2
        if bet_type == 'WIN__1X':
            my_bet_number = 0
        elif bet_type == 'WIN__X2':
            my_bet_number = 1
        elif bet_type == 'WIN__12':
            my_bet_number = -1
        else:
            print('Ставка на (Двойной шанс) , неизвестный формат ставки')
            return 'Ставка на (Двойной шанс) , неизвестный формат ставки'

        bets[my_bet_number].click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bets[my_bet_number])

    def make_cyber_football_bet_totalbet_of_game(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку total bet url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == 'Голы матча') or (text1 == 'Match Goals'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != 'Голы матча') and (text != 'Match Goals'):
            print('Ставка(Голы матча не найдена/total bet) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        goul_count = element_with_bets.find_element_by_class_name('srb-ParticipantLabelCentered_Name ').text
        bets = element_with_bets.find_elements_by_class_name('gl-ParticipantOddsOnly ')

        number_of_gouls = bet_type.split('(')
        number_of_gouls = number_of_gouls[-1]
        number_of_gouls = number_of_gouls.strip(')')
        number_of_gouls = number_of_gouls.strip('')

        if number_of_gouls != goul_count:
            print(f'Число голов не совпадает {goul_count}|{number_of_gouls}')
            return

        if 'OVER' in bet_type:
            bets[0].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[0])
        else:
            bets[1].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[1])

    def make_cyber_football_bet_totalbet_of_teme_1or2(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку total bet team url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 'None'
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text[-4:]
            text1_2 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == 'ГОЛЫ') or (text1 == 'Goals' and len(text1_2) > 12):
                line = i
                print(f'line: {line}')
                break

        if line == 'None':
            print('Total bet на команду не найдена')
            return

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if 'P2' in bet_type:
            line += 1
            bet_element = list_of_bets[line]

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        goul_count = element_with_bets.find_element_by_class_name('srb-ParticipantLabelCentered_Name ').text
        bets = element_with_bets.find_elements_by_class_name('gl-ParticipantOddsOnly ')

        bet_type = bet_type.strip(')')
        bet_type = bet_type.split('(')
        number_of_gouls = bet_type[1]
        bet_type = bet_type[0]

        if number_of_gouls != goul_count:
            print(f'Число голов не совпадает {goul_count}|{number_of_gouls}')
            return

        bet_element_1 = bets[0]
        if 'OVER' in bet_type:
            bets[0].click()
        else:
            bets[1].click()
            bet_element_1 = bets[1]

        time.sleep(2)
        self.make_a_bet(bet_value, coef, bet_element_1)

    def make_cyber_football_bet_gola_ne_budet(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку Гола не будет url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1[1:] == '-й Гол':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text[1:] != '-й Гол':
            print('Ставка(Двойной шанс) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        bets = element_with_bets.find_elements_by_class_name('gl-Participant_General ')

        # gl-Participant_General
        my_bet_number = 1

        bets[my_bet_number].click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bets[my_bet_number])

    def make_cyber_football_bet_odd_or_even(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку ЧетНечет: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'Голы нечет/чёт':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'Голы нечет/чёт':
            print('Ставка(Голы нечет/чёт) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        bets = element_with_bets.find_elements_by_class_name('gl-Market_General-cn2 ')

        if bet_type == 'Чет':
            bets[1].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[1])
        else:
            bets[0].click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bets[0])

    def make_cyber_football_bet_gandikap_with_3_exists(self, url, bet_type, coef, bet_value):
        # Г1(1) Г2(0) Г1(-1)   (1 -> +1)
        print(f'Проставляем ставку Гандикап с 3 исходами url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'ГАНДИКАП С 3 ИСХОДАМИ':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'ГАНДИКАП С 3 ИСХОДАМИ':
            print('Ставка Гандикап с 3 исходами не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        gandicaps = element_with_bets.find_elements_by_class_name('gl-ParticipantCentered_Handicap')
        bets_list = element_with_bets.find_elements_by_class_name('gl-ParticipantCentered ')

        true_gandicap = bet_type[3:]
        true_gandicap = true_gandicap.strip('(')
        true_gandicap = true_gandicap.strip(')')

        if true_gandicap == '0':
            pass
        elif true_gandicap[0] == '-':
            pass
        else:
            true_gandicap = '+' + true_gandicap

        print(f'true gandicap: {true_gandicap}')

        if 'Г1' in bet_type:
            line_ = 0
        else:
            line_ = -1

        gandicap = gandicaps[line_]
        bet_ = bets_list[line_]

        if gandicap != true_gandicap:
            print('Гандикап изменился')
            return

        bet_.click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bet_)

    def make_cyber_football_bet_F1_F2(self, url, bet_type, coef, bet_value):
        # Ф2(-3)
        print(f'Проставляем ставку Ф url: {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if 'АЗИАТСКИЙ ГАНДИКАП' in text1:
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if not 'АЗИАТСКИЙ ГАНДИКАП' in text:
            print('Ставка Ф не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        element_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')

        bets_list = element_with_bets.find_elements_by_class_name('gl-ParticipantCentered ')

        if 'Ф1' in bet_type:
            line_ = 0
        else:
            line_ = -1

        bet_ = bets_list[line_]

        bet_.click()
        time.sleep(2)
        self.make_a_bet(bet_value, coef, bet_)

    def make_basketball_bet(self, url, bet_type, coef):
        bet_value = self.bet_value

        '''Ставка на баскетбол'''
        if bet_type == 'WIN_OT__P1' or bet_type == 'WIN_OT__P2' or bet_type == 'WIN_OT__PX':
            self.make_basketball_bet_P1P2PX(url, bet_type, coef, bet_value)
        elif bet_type[:12] == 'HANDICAP_OT_':
            self.make_basketball_bet_handicap_of_game(url, bet_type, coef, bet_value)
        elif bet_type[:11] == 'TOTALS_OT__':
            self.make_basketball_bet_total_of_game(url, bet_type, coef, bet_value)
        elif bet_type[:4] == 'SET_' and bet_type[8:14] == 'TOTALS':
            self.make_basketball_bet_set_total(url, bet_type, coef, bet_value)
        else:
            print('Неизвестный тип ставки (1)', bet_type)

    def make_basketball_bet_set_total(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку set total {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        total_value = bet_type.split('(')[-1]
        total_value = total_value.strip(')')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0

        # print(set_number, type(set_number))
        english_text = '1st Quarter Lines'
        if set_number == '2':
            english_text = '2nd Quarter Lines'
        elif set_number == '3':
            english_text = '3rd Quarter Lines'
        elif set_number == '4':
            english_text = '4th Quarter Lines'
        # print('-'*100)
        # print(english_text)

        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text
            # print(text1)
            if (text1 == english_text) or (text1 == f'Линии - {set_number}-я четверть'):
                # print('ok')
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != english_text) and (text != f'Линии - {set_number}-я четверть'):
            print('Ставка set total не найдена basketball')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('srb-ParticipantLabel')[1].text
        if (bet_text != 'Тотал') and (bet_text != 'Total'):
            print('Не удалось найти ставку тотал на сет (basketball)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Participant_General')[1]
        bet2 = columns_[2].find_elements_by_class_name('gl-Participant_General')[1]

        if 'OVER' in bet_type:
            total = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            total = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_basketball_bet_P1P2PX(self, url, bet_type, coef, bet_value):
        '''Ставка победа на основное время'''
        print(f'Проставляем ставку П1П2(basketball): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'Game Lines':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'Game Lines':
            print('Ставка П1П2(basketball) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        # колонки со ставками
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_tag_name('div')[-1].text
        if bet_text != 'Money Line':
            print('Не удалось найти ставку на победу (basketball)')
            return

        bet1 = columns_[1].find_elements_by_tag_name('div')[-1]
        bet2 = columns_[2].find_elements_by_tag_name('div')[-1]

        if 'P1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_basketball_bet_handicap_of_game(self, url, bet_type, coef, bet_value):
        '''Ставка gandicap на основное время (Spread)'''
        print(f'Проставляем ставку Spread на основное время(basketball): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'Game Lines':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'Game Lines':
            print('Ставка П1П2(basketball) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        # колонки со ставками
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_tag_name('div')[1].text
        if bet_text != 'Spread':
            print('Не удалось найти ставку на Spread (basketball)')
            return

        bet1 = columns_[1].find_elements_by_tag_name('div')[1]
        bet2 = columns_[2].find_elements_by_tag_name('div')[1]

        needed_handicap = bet_type.split('(')[-1]
        needed_handicap = needed_handicap.strip(')')
        print('Нужный гандикап:', needed_handicap)

        if 'P1' in bet_type:
            real_handicap_value = bet1.find_element_by_class_name(
                'srb-ParticipantCenteredStackedMarketRow_Handicap').text
            real_handicap_value = real_handicap_value.strip('+')
            if real_handicap_value != needed_handicap:
                print(f'Гандикап изменился {needed_handicap} -> {real_handicap_value}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            real_handicap_value = bet2.find_element_by_class_name(
                'srb-ParticipantCenteredStackedMarketRow_Handicap').text
            real_handicap_value = real_handicap_value.strip('+')
            if real_handicap_value != needed_handicap:
                print(f'Гандикап изменился {needed_handicap} -> {real_handicap_value}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_basketball_bet_total_of_game(self, url, bet_type, coef, bet_value):
        '''Ставка total на основное время'''
        print(f'Проставляем ставку total на основное время(basketball): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'Game Lines':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'Game Lines':
            print('Ставка П1П2(basketball) не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        # колонки со ставками
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('gl-Market_General-cn1')[1].text
        print(bet_text)
        if bet_text != 'Total':
            print('Не удалось найти ставку на Total (basketball)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Market_General-cn1')[1]
        bet2 = columns_[2].find_elements_by_class_name('gl-Market_General-cn1')[1]

        needed_total = bet_type.split('(')[-1]
        needed_total = needed_total.strip(')')
        print('Нужный total:', needed_total)

        if 'OVER' in bet_type:
            real_total_value = bet1.find_element_by_class_name(
                'srb-ParticipantCenteredStackedMarketRow_Handicap').text
            real_total_value = real_total_value.split(' ')[-1]

            if real_total_value != needed_total:
                print(f'Тотал изменился {needed_total} -> {real_total_value}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            real_total_value = bet2.find_element_by_class_name(
                'srb-ParticipantCenteredStackedMarketRow_Handicap').text
            real_total_value = real_total_value.split(' ')[-1]

            if real_total_value != needed_total:
                print(f'Тотал изменился {needed_total} -> {real_total_value}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet(self, url, bet_type, coef):
        '''Ставка на настольный теннис'''
        bet_value = self.bet_value

        # SET_03__WIN__P2
        if bet_type[:4] == 'SET_' and bet_type[6:14] == '__WIN__P':
            self.make_table_tennis_bet_set_winner(url, bet_type, coef, bet_value)
        # SET_03__TOTALS__UNDER(18.5)
        elif bet_type[:4] == 'SET_' and bet_type[8:14] == 'TOTALS':
            self.make_table_tennis_bet_set_total(url, bet_type, coef, bet_value)
        # SET_03__HANDICAP__P1(-2.5)
        elif bet_type[:4] == 'SET_' and bet_type[8:16] == 'HANDICAP':
            self.make_table_tennis_bet_set_handicap(url, bet_type, coef, bet_value)
        # WIN__P2
        elif bet_type == 'WIN__P1' or bet_type == 'WIN__P2':
            self.make_table_tennis_bet_game_winner(url, bet_type, coef, bet_value)
        else:
            print('Неизвестный тип ставки', bet_type)

    def make_table_tennis_bet_game_winner(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку winner {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Match Lines') or (text1 == f'ЛИНИИ МАТЧА'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Match Lines') and (text != f'ЛИНИИ МАТЧА'):
            print('Ставка П1П2 настольный теннис not found')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_tag_name('div')[1].text
        if (bet_text != 'Победитель') and (bet_text != 'Winner'):
            print('Не удалось найти ставку на победу (теннис)')
            return

        bet1 = columns_[1].find_elements_by_tag_name('div')[1]
        bet2 = columns_[2].find_elements_by_tag_name('div')[1]

        if 'P1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet_set_winner(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку set winner {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Game {set_number} Lines') or (text1 == f'ИГРА {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Game {set_number} Lines') and (text != f'ИГРА {set_number} - ЛИНИИ'):
            print('Ставка П1П2 настольный теннис')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_tag_name('div')[1].text
        if (bet_text != 'Победитель') and (bet_text != 'Winner'):
            print('Не удалось найти ставку на победу (теннис)')
            return

        bet1 = columns_[1].find_elements_by_tag_name('div')[1]
        bet2 = columns_[2].find_elements_by_tag_name('div')[1]

        if 'P1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet_set_total(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку set total {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        total_value = bet_type.split('(')[-1]
        total_value = total_value.strip(')')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Game {set_number} Lines') or (text1 == f'ИГРА {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Game {set_number} Lines') and (text != f'ИГРА {set_number} - ЛИНИИ'):
            print('Ставка set total не найдена настольный теннис')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('srb-ParticipantLabel')[-1].text
        if (bet_text != 'Тотал') and (bet_text != 'Total'):
            print('Не удалось найти ставку тотал на сет (теннис)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Participant_General')[-1]
        bet2 = columns_[2].find_elements_by_class_name('gl-Participant_General')[-1]

        if 'OVER' in bet_type:
            total = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            total = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet_set_handicap(self, url, bet_type, coef, bet_value):
        # SET_03__HANDICAP__P1(-2.5)
        print(f'Проставляем ставку set handicap {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        handicap_value = bet_type.split('(')[-1]
        handicap_value = handicap_value.strip(')')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Game {set_number} Lines') or (text1 == f'ИГРА {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Game {set_number} Lines') and (text != f'ИГРА {set_number} - ЛИНИИ'):
            print('Ставка set handicap не найдена настольный теннис')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('srb-ParticipantLabel')[1].text
        if (bet_text != 'Handicap') and (bet_text != 'Гандикап'):
            print('Не удалось найти ставку handicap на сет (теннис)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Participant_General')[1]
        bet2 = columns_[2].find_elements_by_class_name('gl-Participant_General')[1]

        if 'P1' in bet_type:
            total = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if handicap_value not in total:
                print(f'Тотал не совпадает: {handicap_value} -> {total}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            total = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if handicap_value not in total:
                print(f'Тотал не совпадает: {handicap_value} -> {total}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet_P1_P2_of_game1(self, url, bet_type, coef, bet_value):
        '''Побеа в отдельной игре, а не на всю партию целиком'''

        print(f'Проставляем ставку П1 (3 партия)(table tennis): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text
            # ИГРА 5 - ЛИНИИ
            if ('ИГРА' in text1) and ('ЛИНИИ' in text1):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if not (('ИГРА' in text) and ('ЛИНИИ' in text)):
            print('Ставка П1 на игру матча?')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        line_ = -1
        # Гандикап (Игры)
        counter_ = 0
        for bet_text1 in columns_[0].find_elements_by_tag_name('div'):
            try:
                bet_text = bet_text1.text
                print(f'{counter_}: {bet_text}')
                if bet_text == 'Победитель':
                    line_ = counter_
                    # -1 ?
                    print(line_)
                    break
            except:
                pass
            counter_ += 1
        # bet_text = columns_[0].find_elements_by_tag_name('div')[1].text

        if line_ == -1:
            print('Не удалось найти ставку на Победу на игру (теннис)')
            return

        # srb-ParticipantCenteredStackedMarketRow_Handicap

        bet1 = columns_[1].find_elements_by_tag_name('div')[line_]
        bet2 = columns_[2].find_elements_by_tag_name('div')[line_]

        if 'П1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet_F1_F2_gandikap_of_match(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку Ф1(2.5)(Гандикап) (table tennis): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')

        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if text1 == 'ЛИНИИ МАТЧА':
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if text != 'ЛИНИИ МАТЧА':
            print('Ставка Гандикап на матч?')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        line_ = -1
        # Гандикап (Игры)
        counter_ = 0
        for bet_text1 in columns_[0].find_elements_by_tag_name('div'):
            try:
                bet_text = bet_text1.text
                print(f'{counter_}: {bet_text}')
                if bet_text == 'Гандикап (Игры)':
                    line_ = counter_ - 1
                    #
                    print(line_)
                    break
            except:
                pass
            counter_ += 1
        # bet_text = columns_[0].find_elements_by_tag_name('div')[1].text

        if line_ == -1:
            print('Не удалось найти ставку на гандикап (теннис)')
            return

        # srb-ParticipantCenteredStackedMarketRow_Handicap

        bet1 = columns_[1].find_elements_by_tag_name('div')[line_]
        bet2 = columns_[2].find_elements_by_tag_name('div')[line_]

        bet1_gendikap_value = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
        bet2_gendikap_value = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
        print(f'1 gandicap: {bet1_gendikap_value}')
        print(f'2 gandicap: {bet2_gendikap_value}')

        true_gendikap_value = bet_type.split('(')
        true_gendikap_value = true_gendikap_value[-1]
        true_gendikap_value = true_gendikap_value.strip(')')
        if true_gendikap_value[0] != '-':
            true_gendikap_value = '+' + true_gendikap_value

        print(f'True gandicap: {true_gendikap_value}')

        if 'Ф1' in bet_type:
            if true_gendikap_value != bet1_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            if true_gendikap_value != bet2_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_table_tennis_bet_F1_F2_gandikap_of_game1(self, url, bet_type, coef, bet_value):
        '''Гандикап на отдельную игру, а не на всё партию целиком'''

        print(
            f'Проставляем ставку Ф1(2.5) (3 партия) (Гандикап) (table tennis): {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text
            # ИГРА 5 - ЛИНИИ
            if ('ИГРА' in text1) and ('ЛИНИИ' in text1):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if not (('ИГРА' in text) and ('ЛИНИИ' in text)):
            print('Ставка Гандикап на игру матча?')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        line_ = -1
        # Гандикап (Игры)
        counter_ = 0
        for bet_text1 in columns_[0].find_elements_by_tag_name('div'):
            try:
                bet_text = bet_text1.text
                print(f'{counter_}: {bet_text}')
                if bet_text == 'Гандикап':
                    line_ = counter_ - 1
                    # -1 ?
                    print(line_)
                    break
            except:
                pass
            counter_ += 1
        # bet_text = columns_[0].find_elements_by_tag_name('div')[1].text

        if line_ == -1:
            print('Не удалось найти ставку на гандикап на игру (теннис)')
            return

        # srb-ParticipantCenteredStackedMarketRow_Handicap

        bet1 = columns_[1].find_elements_by_tag_name('div')[line_]
        bet2 = columns_[2].find_elements_by_tag_name('div')[line_]

        bet1_gendikap_value = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
        bet2_gendikap_value = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text

        true_gendikap_value = bet_type.split(' ')[0]
        true_gendikap_value = true_gendikap_value.split('(')
        true_gendikap_value = true_gendikap_value[-1]
        true_gendikap_value = true_gendikap_value.strip(')')
        if true_gendikap_value[0] != '-':
            true_gendikap_value = '+' + true_gendikap_value

        print(f'True gandicap: {true_gendikap_value}')

        if 'Ф1' in bet_type:
            if true_gendikap_value != bet1_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            if true_gendikap_value != bet2_gendikap_value:
                print('Значение гандикапа изменилось')
                return

            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_volleyball_bet(self, url, bet_type, coef):
        '''Ставка на настольный волейбол'''
        bet_value = self.bet_value

        # SET_03__WIN__P2
        if bet_type[:4] == 'SET_' and bet_type[6:14] == '__WIN__P':
            self.make_volleyball_bet_set_winner(url, bet_type, coef, bet_value)
        # SET_03__TOTALS__UNDER(18.5)
        elif bet_type[:4] == 'SET_' and bet_type[8:14] == 'TOTALS':
            self.make_volleyball_bet_set_total(url, bet_type, coef, bet_value)
        # SET_03__HANDICAP__P1(-2.5)
        elif bet_type[:4] == 'SET_' and bet_type[8:16] == 'HANDICAP':
            self.make_volleyball_bet_set_handicap(url, bet_type, coef, bet_value)
        # WIN__P2
        elif bet_type == 'WIN__P1' or bet_type == 'WIN__P2':
            self.make_volleyball_bet_game_winner(url, bet_type, coef, bet_value)
        else:
            print('Неизвестный тип ставки', bet_type)

    def make_volleyball_bet_game_winner(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку winner {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Game Lines') or (text1 == f'ЛИНИИ ИГРЫ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Game Lines') and (text != f'ЛИНИИ ИГРЫ'):
            print('Ставка П1П2 волейбол not found')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_tag_name('div')[1].text
        if (bet_text != 'Победитель') and (bet_text != 'Winner'):
            print('Не удалось найти ставку на победу (волейбол)')
            return

        bet1 = columns_[1].find_elements_by_tag_name('div')[1]
        bet2 = columns_[2].find_elements_by_tag_name('div')[1]

        if 'P1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_volleyball_bet_set_winner(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку set winner {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Set {set_number} Lines') or (text1 == f'СЕТ {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Set {set_number} Lines') and (text != f'СЕТ {set_number} - ЛИНИИ'):
            print('Ставка П1П2 волейбол')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_tag_name('div')[1].text
        if (bet_text != 'Победитель') and (bet_text != 'Winner'):
            print('Не удалось найти ставку на победу (теннис)')
            return

        bet1 = columns_[1].find_elements_by_tag_name('div')[1]
        bet2 = columns_[2].find_elements_by_tag_name('div')[1]

        if 'P1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_volleyball_bet_set_total(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку set total {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        total_value = bet_type.split('(')[-1]
        total_value = total_value.strip(')')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Set {set_number} Lines') or (text1 == f'СЕТ {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Set {set_number} Lines') and (text != f'СЕТ {set_number} - ЛИНИИ'):
            print('Ставка set total не найдена настольный теннис')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('srb-ParticipantLabel')[-1].text
        if (bet_text != 'Тотал') and (bet_text != 'Total'):
            print('Не удалось найти ставку тотал на сет (теннис)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Participant_General')[-1]
        bet2 = columns_[2].find_elements_by_class_name('gl-Participant_General')[-1]

        if 'OVER' in bet_type:
            total = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            total = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_volleyball_bet_set_handicap(self, url, bet_type, coef, bet_value):
        # SET_03__HANDICAP__P1(-2.5)
        print(f'Проставляем ставку set handicap {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        handicap_value = bet_type.split('(')[-1]
        handicap_value = handicap_value.strip(')')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Set {set_number} Lines') or (text1 == f'СЕТ {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Set {set_number} Lines') and (text != f'СЕТ {set_number} - ЛИНИИ'):
            print('Ставка set handicap не найдена настольный теннис')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('srb-ParticipantLabel')[1].text
        if (bet_text != 'Handicap') and (bet_text != 'Гандикап'):
            print('Не удалось найти ставку handicap на сет (теннис)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Participant_General')[1]
        bet2 = columns_[2].find_elements_by_class_name('gl-Participant_General')[1]

        if 'P1' in bet_type:
            total = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if handicap_value not in total:
                print(f'Handicap не совпадает: {handicap_value} -> {total}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            total = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if handicap_value not in total:
                print(f'Тотал не совпадает: {handicap_value} -> {total}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_badminton_bet(self, url, bet_type, coef):
        '''Ставка на настольный волейбол'''
        bet_value = self.bet_value

        # SET_03__WIN__P2
        if bet_type[:4] == 'SET_' and bet_type[6:14] == '__WIN__P':
            self.make_badminton_bet_set_winner(url, bet_type, coef, bet_value)
        # SET_03__TOTALS__UNDER(18.5)
        elif bet_type[:4] == 'SET_' and bet_type[8:14] == 'TOTALS':
            self.make_badminton_bet_set_total(url, bet_type, coef, bet_value)
        # SET_03__HANDICAP__P1(-2.5)
        elif bet_type[:4] == 'SET_' and bet_type[8:16] == 'HANDICAP':
            self.make_badminton_bet_set_handicap(url, bet_type, coef, bet_value)
        else:
            print('Неизвестный тип ставки', bet_type)

    def make_badminton_bet_set_winner(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку set winner {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Game {set_number} Lines') or (text1 == f'ИГРА {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Game {set_number} Lines') and (text != f'ИГРА {set_number} - ЛИНИИ'):
            print('Ставка П1П2 badminton не найдена')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('gl-Market_General-cn1')[-1].text
        if (bet_text != 'Победитель') and (bet_text != 'Winner'):
            print('Не удалось найти ставку на победу (badminton)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Market_General-cn1')[-1]
        bet2 = columns_[2].find_elements_by_class_name('gl-Market_General-cn1')[-1]

        if 'P1' in bet_type:
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_badminton_bet_set_total(self, url, bet_type, coef, bet_value):
        print(f'Проставляем ставку set total {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        total_value = bet_type.split('(')[-1]
        total_value = total_value.strip(')')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Game {set_number} Lines') or (text1 == f'ИГРА {set_number} - ЛИНИИ'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Game {set_number} Lines') and (text != f'ИГРА {set_number} - ЛИНИИ'):
            print('Ставка set total не найдена badminton')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        columns_ = elements_with_bets.find_element_by_class_name('gl-MarketGroupContainer ')
        columns_ = columns_.find_elements_by_class_name('gl-Market_General-columnheader ')

        bet_text = columns_[0].find_elements_by_class_name('gl-Market_General-cn1')[0].text
        if (bet_text != 'Тотал') and (bet_text != 'Total'):
            print('Не удалось найти ставку тотал на сет (badminton)')
            return

        bet1 = columns_[1].find_elements_by_class_name('gl-Participant_General')[0]
        bet2 = columns_[2].find_elements_by_class_name('gl-Participant_General')[0]

        if 'OVER' in bet_type:
            total = bet1.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            total = bet2.find_element_by_class_name('srb-ParticipantCenteredStackedMarketRow_Handicap').text
            if total_value not in total:
                print(f'Тотал не совпадает: {total_value} -> {total}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def make_badminton_bet_set_handicap(self, url, bet_type, coef, bet_value):
        # SET_03__HANDICAP__P1(-2.5)
        print(f'Проставляем ставку set handicap {url}; bet_type: {bet_type}; coef: {coef}')
        self.driver.get(url)
        time.sleep(3)
        set_number = bet_type.split('__')[0]
        set_number = set_number.split('_')[1]
        set_number = set_number.strip('0')

        handicap_value = bet_type.split('(')[-1]
        handicap_value = handicap_value.strip(')')

        list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
        line = 0
        for i in range(len(list_of_bets)):
            bet_element = list_of_bets[i]
            text1 = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

            if (text1 == f'Game {set_number} Handicap') or (text1 == f'Игра {set_number} Гандикап'):
                line = i
                break

        bet_element = list_of_bets[line]
        text = bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').text

        if (text != f'Game {set_number} Handicap') and (text != f'Игра {set_number} Гандикап'):
            print('Ставка set handicap не найдена badminton')
            return

        try:
            bet_element.find_element_by_class_name('gl-MarketGroup_Wrapper ')
        except:
            print('Разворачиваем ставку')
            bet_element.find_element_by_class_name('sip-MarketGroupButton_Text ').click()
            time.sleep(0.5)
            list_of_bets = self.driver.find_elements_by_class_name('sip-MarketGroup ')
            bet_element = list_of_bets[line]

        elements_with_bets = bet_element.find_elements_by_class_name('gl-Participant_General')

        bet1 = elements_with_bets[0]
        bet2 = elements_with_bets[1]

        if 'P1' in bet_type:
            total = bet1.find_element_by_class_name('gl-ParticipantBorderless_Name').text
            if handicap_value not in total:
                print(f'Тотал не совпадает: {handicap_value} -> {total}')
                return
            bet1.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet1)
        else:
            total = bet2.find_element_by_class_name('gl-ParticipantBorderless_Name').text
            if handicap_value not in total:
                print(f'Тотал не совпадает: {handicap_value} -> {total}')
                return
            bet2.click()
            time.sleep(2)
            self.make_a_bet(bet_value, coef, bet2)

    def close_session(self):
        print('close session')
        self.driver.quit()


def cool_decorator(method_to_decorate, type_of_account):
    def wrapper(url):
        if (type_of_account == 'RU') and ('bet365' in url):
            url = url.replace('.com', '.ru')
        return method_to_decorate(url)

    return wrapper

class GetWorkAccountsList:
    def __init__(self, number_of_accounts, vpn_country):
        self.firefox_profile = info.firefox_profile_path
        self.number_of_accounts = number_of_accounts

        def check_bet365(driver):
            # провепка правильно ли открылся сайт bet365
            try:
                time.sleep(2)
                driver.find_element_by_class_name('hm-MainHeaderRHSLoggedOutWide_LoginContainer')
                return True
            except Exception as er:
                return False

        def open_new_window_2ip(driver):
            current_window = driver.current_window_handle
            driver.execute_script(f"window.open('https://2ip.ru/', '_blank')")
            time.sleep(7)
            driver.switch_to.window(driver.window_handles[-1])
            driver.close()
            driver.switch_to.window(current_window)

        def get_driver():
            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True

            fp = webdriver.FirefoxProfile(self.firefox_profile)
            fp.set_preference("browser.privatebrowsing.autostart", True)

            options = webdriver.FirefoxOptions()
            options.add_argument("-private")
            options.set_preference("dom.webdriver.enabled", False)
            options.set_preference("dom.webnotifications.enabled", False)
            binary = info.firefox_binary
            options.binary = binary

            driver = webdriver.Firefox(capabilities=firefox_capabilities, firefox_profile=fp,
                                       firefox_binary=info.firefox_binary,
                                       executable_path=info.path_to_geckodriver,
                                       options=options)

            time.sleep(10)

            # driver.get = cool_decorator(driver.get, self.vpn_country)
            driver.get('https://2ip.ru/')
            driver.set_page_load_timeout(15)
            try:
                driver.get('https://www.bet365.com/')
                input('Пройдите прокси, затем нажмите Enter:')
                driver.set_page_load_timeout(25)
                if check_bet365(driver):
                    return driver, 'OK'
            except:
                pass

            driver.set_page_load_timeout(25)
            for i in range(2):
                open_new_window_2ip(driver)
                time.sleep(0.3)

            try:
                driver.get('https://www.bet365.com/')
                if check_bet365(driver):
                    return driver, 'OK'
                else:
                    return driver, 'Сайт bet365 не загрузился'
            except:
                return driver, 'Сайт bet365 не загрузился'

        def add_accounts_to_list(Browsers_List=[]):
            # задержка
            time_to_sleep = random.randint(1, 1000) / 500
            time.sleep(time_to_sleep)
            driver, info = get_driver()
            if info == 'OK':
                Browsers_List.append(driver)
                print('+1 browser')
            else:
                try:
                    driver.close()
                    driver.quit()
                except:
                    pass

        # число браузеров, которое будет открыто
        number_of_tries = 6
        try:
            number_of_tries = info.number_of_tries
        except:
            pass
        Browser_List = []

        while len(Browser_List) < self.number_of_accounts:
            try:
                with Pool(processes=number_of_tries) as p:
                    p.map(add_accounts_to_list, [Browser_List for i in range(number_of_tries)])
            except Exception as er:
                print(f'Ошибка при выполнениии Poll: {er}')

            check_counter_i = 0
            while check_counter_i < len(Browser_List):
                if check_bet365(Browser_List[check_counter_i]):
                    check_counter_i += 1
                else:
                    print('Браузер не работает!')
                    Browser_List.pop(check_counter_i)

            print(f'Открыто {len(Browser_List)} из {self.number_of_accounts} аккаунтов')

        while len(Browser_List) > self.number_of_accounts:
            Browser_List.pop(-1).quit()
            print('1 лишний аккаунт удалён')

        self.Browser_List = Browser_List

    def return_Browser_List(self):
        return self.Browser_List


class FireFoxDriverMainNoAutoOpen(FireFoxDriverMain):
    def __init__(self, driver, bet_value, login, password, vpn_country):
        self.driver = driver
        if vpn_country == 'RU':
            try:
                self.driver.get = cool_decorator(self.driver.get, vpn_country)
            except:
                pass

        self.bet_value = bet_value

        self.bet365_login = login
        self.bet365_password = password
        self.is_VPN = True
        # аккаунт рабочий, если значение меняется на False, то аккаунт закрывается
        self.is_valud_account = True

        # путь к firefox profile
        self.firefox_profile = info.firefox_profile_path

