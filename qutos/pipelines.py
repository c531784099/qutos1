# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json
# from pymysql import cursors
import pymysql
from twisted.enterprise import adbapi

#数据写入到json文件
class QutosPipeline(object):
    def __init__(self):
        self.file = open('duanzi.json', 'w', encoding='utf-8')

    def open_spider(self, spider):
        print('爬虫开始了...')

    def process_item(self, item, spider):
        print("json")
        # ensure_ascii=False实现让中文写入的时候保持为中文
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        #必须有返回，没有返回的话就会丢失，后面的Itempipeline组件就会无法处理这个Item
        #  网络参考：这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理
        return item

    def close_spider(self, spider):
        self.file.close()
        print('爬虫结束了!')

#定义存储到数据库Mysql的中间件
class MysqlTwistedPipeline(object):
    def __init__(self,db_pool):
        self.db_pool = db_pool
    @classmethod
    def from_settings(cls,settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            database=settings["MYSQL_DB"],
            user=settings["MYSQL_USER"],
            port=settings["MYSQL_PORT"],
            password=settings["MYSQL_PASSWD"],
            charset="utf8",
            # 游标设置
            cursorclass=pymysql.cursors.DictCursor,
            # 设置编码是否使用Unicode
            use_unicode=True
        )
        db_pool = adbapi.ConnectionPool("pymysql",**dbparms)
        print('1'*20)
        return cls(db_pool)

    def process_item(self, item, spider):
        query = self.db_pool.runInteraction(self.insert_into, item)
        print('2' * 30)
        # 如果sql执行发送错误,自动回调addErrBack()函数
        query.addErrback(self.handle_error, item, spider)
        #  网络参考：这个方法必须返回一个 Item 对象，被丢弃的item将不会被之后的pipeline组件所处理
        return item
    def insert_into(self,cursor,item):
        # 创建sql语句
        sql =item.get_insert_sql()
        print('00000000000000000000000000'+sql)
        cursor.execute(sql)
        # 不需要commit() Twisted 会自动提交commit().
        print('3'*40)

    #错误函数
    def handle_error(self,failure,item,spider):
        # #输出错误信息
        print(failure)
    def close_spider(self, spider):
        #不需要关闭数据库连接，这是从数据库连接池中取得的交还给数据库连接pool，
        print('爬虫结束了!')

