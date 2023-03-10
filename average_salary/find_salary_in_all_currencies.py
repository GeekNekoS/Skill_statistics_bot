import re
import time
import datetime
from selenium import webdriver
from collections import defaultdict
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urls import *


def saving(file_name):
    now = datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S')
    with open(f"{file_name} [{now}].txt", "w", encoding="utf-8") as file:
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


def parse():
    global driver
    driver = webdriver.Chrome()
    get_connect("https://hh.ru/")

    url, max_page, file_name = qa_middle()  # qa_manual()

    total_amount = []

    check = []  #

    for page in range(1, max_page + 1):
        url += f"&page={page}"
        get_connect(url)
        time.sleep(2)

        print(f"\033[38;5;{231}m-=-= Page №{page} =-=- \033[0;0m")

        vacancies_xpath = "//div[@class='serp-item']//span[@class='bloko-header-section-3']"
        vacancies = driver.find_elements(By.XPATH, vacancies_xpath)

        for vacancy in vacancies:
            money_text = vacancy.text

            # 1] от, 2], до 3] от и до
            # "\w{2}\s\d{1,}\s\d{1,}"  # <= от, до
            # "\d{1,}\s\d{1,}\s.\s\d{1,}\s\d{1,}\s\w{3,}"  # <= от и до

            if re.search("\d{1,}\s\d{1,}\s.\s\d{1,}\s\d{1,}\s", money_text):
                # if money_text.split()[-1] != "сум":
                if money_text.split()[-1] == "руб.":
                    split = money_text.split()

                    num_1 = int(split[0] + split[1])
                    total_amount.append(num_1)

                    num_2 = int(split[3] + split[4])
                    total_amount.append(num_2)

                # if money_text.split()[-1] == "сум":
                #     print(money_text)  #
                #     check.append(money_text)  #
                #
                #     # split = money_text.split()
                #     #
                #     # num_1 = int(split[0] + split[1] + split[3])
                #     # total_amount.append(num_1)
                #     #
                #     # num_2 = int(split[5] + split[6] + split[7])
                #     # total_amount.append(num_2)

            elif re.search("\w{2}\s\d{1,}\s\d{1,}", money_text):
                if money_text.split()[-1] == "руб.":
                    print("от, до")
                    print(money_text)

                    split = money_text.split()

                    num = int(split[1] + split[2])
                    check.append(num)

            else:
                print(f"Не руб: {money_text}")  # всё должно уходить в if и elif
                # 300 – 450 USD
                # 600 – 1 200 USD

    print(check)

    print(f"Всего: {sum(total_amount)}")
    print(f"Среднее: {sum(total_amount)/len(total_amount)}")  # ещё не верно, так как не было перевода валют

    driver.close()
    driver.quit()


def main():
    parse()


if __name__ == '__main__':
    main()

# Во всех валютах!
