# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import pymysql
from twisted.enterprise import adbapi
class KanqiPipeline(object):
    def __init__(self,dbpool):
        #数据库的链接池
        self.dbpool = dbpool
    #使用这个函数来应用settings配置文件。
    @classmethod
    def from_crawler(cls, crawler):
        parmas = {
        'host':crawler.settings['MYSQL_HOST'],
        'user':crawler.settings['MYSQL_USER'],
        'passwd':crawler.settings['MYSQL_PASSWORD'],
        'db':crawler.settings['MYSQL_DB'],
        'port':3306,
        'charset':'utf8',
        }
        dbpool = adbapi.ConnectionPool(
            'pymysql',
            **parmas
        )
        return cls(dbpool)

    def process_item(self, item, spider):
        #这里去调用任务分配的方法
        query = self.dbpool.runInteraction(
            self.insert_data_todb,
            item,
            spider
        )
        #数据插入失败的回调
        query.addErrback(
            self.handle_error,
            item
        )

    #执行数据插入的函数
    def insert_data_todb(self,cursor,item,spider):
        item_dict= dict(item)
        insert_str = item.get_sql_str(item_dict)
        parmas = list(item_dict.values())
        cursor.execute(insert_str,parmas)
        print('插入成功')

    def handle_error(self,failure,item):
        # print(failure)
        print('插入错误')

    def close_spider(self, spider):

        self.dbpool.close()
