import re
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By

from urls import *


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

    url, max_page, file_name = qa_middle()
    total_amount = []

    for page in range(1, max_page + 1):
        url += f"&page={page}"
        get_connect(url)
        time.sleep(2)

        print(f"\033[38;5;{231}m-=-= Page №{page} =-=- \033[0;0m")

        vacancies_xpath = "//div[@class='serp-item']//span[@class='bloko-header-section-3']"
        vacancies = driver.find_elements(By.XPATH, vacancies_xpath)

        for vacancy in vacancies:
            money_text = vacancy.text

            if re.search("\w{2}\s\d{1,}\s\d{1,}", money_text):
                if money_text.split()[-1] == "руб.":
                    split = money_text.split()

                    num = int(split[1] + split[2])
                    total_amount.append(num)

            elif re.search("\d{1,}\s\d{1,}\s.\s\d{1,}\s\d{1,}\s", money_text):
                if money_text.split()[-1] == "руб.":
                    split = money_text.split()

                    num_1 = int(split[0] + split[1])
                    total_amount.append(num_1)

                    num_2 = int(split[3] + split[4])
                    total_amount.append(num_2)

            else:
                print(f"Не руб: {money_text}")  # всё должно уходить в if и elif
                # 600 – 1 200 USD
                # 300 – 450 USD

    print(f"Всего: {sum(total_amount)}")
    print(f"Среднее: {int(sum(total_amount)/len(total_amount))}")  # примерно 145000 руб

    driver.close()
    driver.quit()


def main():
    parse()


if __name__ == '__main__':
    main()

# Среднее только по рублям!
