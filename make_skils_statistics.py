import time
import datetime
from urls import *
from selenium import webdriver
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def saving(file_name):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    with open(f"skils_statistics_reports/{file_name} [{now}].txt", "w", encoding="utf-8") as file:
        ans = list(D.items())
        ans.sort(key=lambda x: x[1], reverse=True)

        for item in ans:
            file.write(f"""{item[0].ljust(20, "-")}| {item[1]}\n""")


def get_connect(url, retry=3):
    """Prevents from possible connection breaks"""
    try:
        driver.get(url=url)

    except Exception as exception:
        if retry:
            print(f"Exception: {exception}")
            print(f"\033[38;5;{196}mReconnecting\033[0;0m")
            return get_connect(url, retry=(retry - 1))
        else:
            raise

    else:
        return driver.get(url=url)


def reg():
    url = "https://hh.ru/login"

    global driver
    driver = webdriver.Chrome()
    # driver.maximize_window()

    try:
        get_connect(url)
        time.sleep(1)

        log_in_button_xpath = "//div[@class='account-login-actions']/button[@class='bloko-link bloko-link_pseudo']"
        log_in_button = driver.find_element(By.XPATH, log_in_button_xpath)
        log_in_button.click()
        time.sleep(0.2)

        print_email = driver.find_element(By.XPATH, "//input[@placeholder='Электронная почта или телефон']")
        print_email.send_keys(" ")  # 1) your login
        time.sleep(0.2)

        print_email = driver.find_element(By.XPATH, "//input[@placeholder='Пароль']")
        print_email.send_keys(" ")  # 2) your password
        time.sleep(0.2)

        email_xpath = "//div[@class='account-login-actions']/button[@class='bloko-button bloko-button_kind-primary']"
        print_email = driver.find_element(By.XPATH, email_xpath)
        print_email.click()
        time.sleep(0.2)

        # time.sleep(30)  # ручное заполнение проверки на бота

    except Exception as exception:
        print(f"\033[38;5;{196}mWasted ψ(▼へ▼メ)\033[0;0m" + f"\n{exception}")


def parse():
    url, max_page, file_name = qa_middle()

    global D
    D = defaultdict(int)

    try:
        for page in range(1, max_page + 1):
            url += f"&page={page}"
            get_connect(url)
            time.sleep(3)

            print(f"\033[38;5;{231}m-=-= Page №{page} =-=- \033[0;0m")

            vacancys_xpath = "//div[@class='serp-item']//a[@class='serp-item__title']"
            vacancys = [vacancy.get_attribute("href") for vacancy in driver.find_elements(By.XPATH, vacancys_xpath)]

            for url in vacancys:
                get_connect(url)
                time.sleep(3)

                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    try:
                        xpath = "//h1[text()='Отзывы о компании']"  # //h1[text()='Отзывы о компании']
                        loading = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath)))
                        print(f"\033[38;5;{82}mPage loaded \033[0;0m")
                        break
                    except:
                        print(f"\033[38;5;{208}mIt takes too long to load! \033[0;0m")
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                try:
                    vacancy_info = driver.find_element(By.XPATH, "//div[@class='vacancy-description']")

                    info = vacancy_info.text.lower()
                    for item in """.,?!:;/\•−–—―+=№©()"«»“”$%&*'""" + "0123456789":
                        info = info.replace(item, "")
                    info = info.split()

                    for elem in info:
                        D[elem] += 1
                except:
                    print(f"\033[38;5;{197}m{'Description not found!'} \033[0;0m")

                    print(f"\033[38;5;{208}m{'Emergency saving!'} \033[0;0m")
                    saving(file_name)

        print()
        print(f"\033[38;5;{82}m{'Saving'} \033[0;0m")
        saving(file_name)
        # не забыть исключить из ответа всякие лишние слова, союзы, предлоги, цифры и тому подобное

        driver.close()
        driver.quit()

    except:
        print(f"\033[38;5;{208}m{'Emergency saving!'} \033[0;0m")
        saving(file_name)


def main():
    reg()
    parse()


if __name__ == '__main__':
    main()
