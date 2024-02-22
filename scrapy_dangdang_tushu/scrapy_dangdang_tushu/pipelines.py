# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import urllib.request
import pymysql

class ScrapyDangdangTushuPipeline:
    def open_spider(self, spider):
        self.fp = open('book.json', 'w', encoding='utf-8')
    def process_item(self, item, spider):
            self.fp.write(str(item))
            return item
    def close_spider(self, spider):
        self.fp.close()


class PicturePipeline:
    def process_item(self, item, spider):
            url = "http:" + item.get("src")
            filename = './books/'+item.get('name') + ".jpg"
            urllib.request.urlretrieve(url = url , filename=filename)
            return item

class MySQLPipeline:
    def __init__(self):
        self.conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='ddts')
        self.cursor = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0 :
            self._write_to_db()
        self.conn.close()
    def process_item(self, item, spider):
        src = item.get("src","")
        name = item.get("name")
        price = item.get("price")
        self.data.append((name,src,price))
        if len(self.data) == 60:
            self._write_to_db()
            self.data.clear()

        return item

    def _write_to_db(self):
        self.cursor.executemany(
                  "insert into books(name,src,price) values(%s,%s,%s)",
                  self.data)
        self.conn.commit()