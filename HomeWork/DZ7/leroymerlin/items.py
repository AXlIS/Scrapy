# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def clear(value):
    while '\n' in value:
        value = value.replace('\n', '')
    return value.strip()


def url_format(url):
    return url.replace('w_82,h_82', 'w_1200,h_1200')


class LeroymerlinItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field(output_processor=TakeFirst())
    type = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(url_format))
    specifications = scrapy.Field(input_processor=MapCompose(clear))
    art = scrapy.Field(output_processor=TakeFirst())
    _id = scrapy.Field()
