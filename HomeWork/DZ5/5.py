from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep
from pprint import pprint
from datetime import datetime, timedelta
from pymongo import MongoClient
import json


def mail_scrapy():
    client = MongoClient('localhost', 27017)
    db = client["mail"]
    letters_dict = db.letters

    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    driver = webdriver.Chrome(options=chrome_options)

    driver.get('https://mail.ru/')

    login = driver.find_element_by_name('login')
    login.send_keys('study.ai_172@mail.ru')

    login.send_keys(Keys.ENTER)

    sleep(1)

    password = driver.find_element_by_name('password')
    password.send_keys('NextPassword172')

    password.send_keys(Keys.ENTER)

    sleep(10)
    letters_links = []
    col = int(driver.find_element_by_xpath('//a[contains(@title, "Входящие")]').get_attribute('title').split()[1])
    while col != len(set(letters_links)):
        try:
            letters = driver.find_elements_by_xpath('//a[contains(@class, "js-letter-list-item")]')
            for letter in letters:
                letters_links.append(letter.get_attribute('href'))
            footer = letters[-1]
            driver.execute_script("arguments[0].scrollIntoView();", footer)
            sleep(0.1)
        except:
            print('Что-то пошло не так...')
    letters_links = list(set(letters_links))

    letters_list = []
    for item in letters_links:
        letter = {}

        driver.get(item)
        sleep(5)

        text = driver.find_element_by_xpath('//div[@class="letter__body"]').text
        author = driver.find_element_by_xpath('//span[@class="letter-contact"]').get_attribute('title')
        topic = driver.find_element_by_xpath('//h2[@class="thread__subject"]').text
        date = driver.find_element_by_xpath('//div[@class="letter__date"]').text
        if 'Сегодня' in date:
            now_date = datetime.now().strftime("%d-%m")
            date = date.replace('Сегодня,', f'{now_date}')
        elif 'Вчера' in date:
            yesterday = datetime.now() - timedelta(days=1)
            date = date.replace('Вчера,', f'{yesterday.strftime("%d-%m")}')

        letter["text"] = text.replace('\n', '')
        letter["author"] = author
        letter["topic"] = topic
        letter["date"] = date
        letters_dict.update_one(letter, {'$set': letter}, upsert=True)
        letters_list.append(letter)

    pprint(letters_list)


def mvideo_scrapy():
    client = MongoClient()
    db = client['mvideo']
    goods_dict = db.goods

    chrome_option = Options()
    chrome_option.add_argument('start-maximized')
    driver = webdriver.Chrome(options=chrome_option)

    driver.get('https://www.mvideo.ru/')

    carousel = driver.find_element_by_xpath('//div[contains(@data-holder, "#loadSubMultiGalleryblock5260655")]')
    button = carousel.find_element_by_xpath('.//a[contains(@class, "next-btn")]')
    total = json.loads(
        carousel.find_element_by_xpath('.//ul[@class="accessories-product-list"]').get_attribute('data-init-param')
    )["ajaxContentLoad"]["total"]
    items = carousel.find_elements_by_class_name('gallery-list-item')
    while len(items) < total:
        items = carousel.find_elements_by_class_name('gallery-list-item')
        button.click()
    goods = []
    for item in items:
        good = {}
        item = item.find_element_by_xpath('.//a[contains(@class, "fl-product-tile-picture__link")]')
        item_info = json.loads(item.get_attribute('data-product-info'))

        good["title"] = item_info["productName"]
        good["price"] = float(item_info["productPriceLocal"])
        good["link"] = item.get_attribute("href")

        goods_dict.update_one(good, {'$set': good}, upsert=True)
        goods.append(good)
    pprint(goods)
    print(len(goods))


if __name__ == '__main__':
    mvideo_scrapy()
