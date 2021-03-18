import requests
from pprint import pprint
from lxml import html
from datetime import datetime
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client["news"]

news_dict = db.news

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'Accept': '*/*'
}


def lenta():
    print('lenta')
    main_url = 'https://lenta.ru/'

    response = requests.get(main_url, headers=header)

    dom = html.fromstring(response.text)

    items = dom.xpath('//section[contains(@class, "js-top-seven")]/div[2]/div[contains(@class, "item")]')

    news_list = []
    for item in items:
        news = {}
        date, title = item.xpath('.//text()')
        link = item.xpath('./a/@href')
        news["title"] = title.replace('\xa0', ' ')
        news["date"] = f'{date} {datetime.now().day}/{datetime.now().month}/{datetime.now().year}'
        news["link"] = main_url[:-1] + link[0]
        news["source"] = main_url
        news_list.append(news)
        news_dict.update_one(news, {'$set': news}, upsert=True)
    pprint(news_list)


def yandex():
    print('yandex')
    main_link = 'https://yandex.ru/news/'

    response = requests.get(main_link, headers=header)

    dom = html.fromstring(response.text)

    items = dom.xpath('//div[contains(@class, "news-top-flexible-stories")]//article[contains(@class, "mg-card")]')

    news_list = []
    for item in items:
        news = {}
        date = item.xpath('.//span[@class="mg-card-source__time"]/text()')
        path = item.xpath('.//a[@class="mg-card__source-link"]')[0]
        link = path.xpath('./@href')
        source = path.xpath('./text()')
        title = item.xpath('.//h2[@class="mg-card__title"]/text()')[0]

        news["title"] = title
        news["link"] = link[0]
        news["date"] = f'{date[0]} {datetime.now().day}/{datetime.now().month}/{datetime.now().year}'
        news["source"] = source[0]
        news_list.append(news)
        news_dict.update_one(news, {'$set': news}, upsert=True)
    pprint(news_list)


def mail():
    print('mail')
    main_url = 'https://news.mail.ru/'

    response = requests.get(main_url, headers=header)

    dom = html.fromstring(response.text)

    items = dom.xpath('//div[contains(@class, "daynews__item")]/a/@href')

    news_list = []

    for item in items:
        news = {}

        response = requests.get(item, headers=header)

        if response.ok:
            item_dom = html.fromstring(response.text)

            source = item_dom.xpath('.//a[contains(@class, "breadcrumbs__link")]//text()')[0]
            title = item_dom.xpath('.//h1/text()')[0]
            date = item_dom.xpath('//span[contains(@class, "note__text")]/text()')[0]

            news["title"] = title
            news["source"] = source
            news["date"] = f'{date.split()[0]} {datetime.now().day}/{datetime.now().month}/{datetime.now().year}'

        news["link"] = item
        news_list.append(news)
        news_dict.update_one(news, {'$set': news}, upsert=True)
    pprint(news_list)


if __name__ == '__main__':
    lenta()
    yandex()
    mail()
