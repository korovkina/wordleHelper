#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import configparser

config_path = 'config.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(config_path, encoding='UTF-8')

URL = CONFIG['general']['url']
CHROME_DRIVER_PATH = CONFIG['general']['chrome_driver_path']
SAVE_PATH = CONFIG['general']['save_path']


def parse_words():
    result = []
    pages = get_urls()
    s = Service(CHROME_DRIVER_PATH)
    driver = webdriver.Chrome(service=s)
    driver.maximize_window()
    for page in pages:
        result.extend(get_words_from_page(driver, page))
    driver.close()
    save_result(result)


def get_urls():
    pages = [URL]
    for i in range(2, 16):
        pages.append(URL.replace('.htm', '') + f'page{i}.htm')
    return pages


def get_words_from_page(driver, page):
    words_on_page = []
    driver.get(page)
    time.sleep(1)
    elements = driver.find_elements(By.CLASS_NAME, "mot")
    elements.extend(driver.find_elements(By.CLASS_NAME, "mot2"))
    for element in elements:
        words_on_page.extend(element.text.split())
    return words_on_page


def save_result(result):
    with open(SAVE_PATH, 'w') as f:
        f.write('\n'.join(result))


if __name__ == "__main__":
    parse_words()



