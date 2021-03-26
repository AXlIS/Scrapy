# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class LeroymerlinPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client["LM"]

    def process_item(self, item, spider):
        db = self.db["goods"]
        item["specifications"] = dict(zip(item["type"], item["specifications"]))
        del item["type"]
        db.update_one(item, {'$set': item}, upsert=True)
        return item


class LeroymerlinPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print()
        if item['photos']:
            for img in item['photos']:
                try:
                    print()
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def file_path(self, request, response=None, info=None, *, item=None):
        # image_guid = request.url[112:]
        return f'full/{item["art"]}/{request.url[112:]}'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
