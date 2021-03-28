# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SubscriberItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    status = scrapy.Field()
    user_id = scrapy.Field()
    subscriber_id = scrapy.Field()
    subscriber_name = scrapy.Field()
    photo = scrapy.Field()


class SubscriptionItem(scrapy.Item):
    _id = scrapy.Field()
    status = scrapy.Field()
    user_id = scrapy.Field()
    subscription_id = scrapy.Field()
    subscription_name = scrapy.Field()
    photo = scrapy.Field()

    pass
