# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import pymongo
import os

MONGO_URL = os.getenv("MONGO_URL")
print(f"************************\n {MONGO_URL}************************")
class MongoDBPipeline:

    def __init__(self):
        self.client = pymongo.MongoClient(MONGO_URL)
        self.db = self.client["mydatabase"]
        self.col = self.db["books"]

    def process_item(self, item, spider):
        self.col.insert_one(item)
        return item
    
    def close_spider(self, spider):
        self.client.close()


from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        return item
