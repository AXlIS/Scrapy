# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pprint import pprint


class HhparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client["_hh"]

    def process_item(self, item, spider):
        collection = self.db[spider.name]
        if spider.name == 'hhru':
            ready_salary = self.create_hh_salary(item["salary"])
            del item["salary"]
            item['min_salary'] = ready_salary['min']
            item['max_salary'] = ready_salary['max']
            item["currency"] = ready_salary['currency']
            collection.update_one(item, {'$set': item}, upsert=True)
        elif spider.name == 'superjob':
            ready_salary = self.create_sj_salary(item["salary"])
            del item["salary"]
            item['min_salary'] = ready_salary['min']
            item['max_salary'] = ready_salary['max']
            item["currency"] = ready_salary['currency']
            collection.update_one(item, {'$set': item}, upsert=True)
        return item

    def create_hh_salary(self, salary):
        ready_salary = {}
        if 'з/п не указана' in salary:
            ready_salary['min'] = None
            ready_salary['max'] = None
            ready_salary["currency"] = None
        elif 'от ' in salary and ' до ' in salary:
            ready_salary['min'] = salary[1].replace('\xa0', ' ')
            ready_salary['max'] = salary[3].replace('\xa0', ' ')
            ready_salary["currency"] = salary[5]
        elif 'от ' in salary:
            ready_salary['min'] = salary[1].replace('\xa0', ' ')
            ready_salary['max'] = None
            ready_salary["currency"] = salary[3]
        elif 'до ' in salary:
            ready_salary['min'] = None
            ready_salary['max'] = salary[1].replace('\xa0', ' ')
            ready_salary["currency"] = salary[3]
        return ready_salary

    def create_sj_salary(self, salary):
        ready_salary = {}
        if len(salary) == 0:
            ready_salary['min'] = None
            ready_salary['max'] = None
            ready_salary["currency"] = None
        elif 'от' in salary:
            sal = salary[2].split('\xa0')
            ready_salary['min'] = sal[0] + ' ' + sal[1]
            ready_salary["currency"] = sal[2]
            ready_salary['max'] = None
        elif 'до' in salary:
            sal = salary[2].split('\xa0')
            ready_salary['min'] = None
            ready_salary["currency"] = sal[2]
            ready_salary['max'] = sal[0] + ' ' + sal[1]
        else:
            ready_salary['min'] = salary[0].replace('\xa0', ' ')
            ready_salary['max'] = salary[1].replace('\xa0', ' ')
            ready_salary["currency"] = salary[3]
        return ready_salary
