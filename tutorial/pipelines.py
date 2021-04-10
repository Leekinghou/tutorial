# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy.exceptions import DropItem

class TextPipeline(object):
    def __init__(self):
        # 定义限制长度为50
        self.limit = 50

    def process_item(self, item, spider):
        # 判断item的text属性是否存在，不存在则抛出DropItem异常
        if item['text']:
            # 大于50就截断然后拼接省略号，再将item返回
            if len(item['text']) > self.limit:
                item['text'] = item['text'][0:self.limit].rstrip() + '…'
            return item
        else:
            return DropItem('Missing Text')

class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    # 使用@staticmethod或@classmethod，可以不需要实例化，直接类名.方法名()来调用
    # cls作为第一个参数用来表示类本身
    @classmethod
    def from_crawler(cls, crawler):
        # 用于获取setting中的全局配置
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )

    # 主要是做初始化操作
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    # 核心，执行数据的插入操作
    def process_item(self, item, spider):
        name = item.__class__.__name__
        self.db[name].insert(dict(item))
        return item

    # 关闭数据库连接
    def close_spider(self, spider):
        self.client.close()


