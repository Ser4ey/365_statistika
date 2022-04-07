from time import sleep

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

