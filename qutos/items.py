# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import pymysql
import scrapy


class QutosItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    content=scrapy.Field()
    authName = scrapy.Field()
    authLink=scrapy.Field()
    authTags=scrapy.Field()
    authJieshao=scrapy.Field()
    # https://www.cnblogs.com/Chai-zz/p/8407322.html
    #

    def get_insert_sql(self):
        an = self['authName'].replace("'","\\\'")
        con=self["content"].replace("'","\\\'")
        au=self["authTags"].replace("'","\\\'")
        aul=self["authLink"].replace("'","\\\'")

        # 字符串代替
        # auj=self["authJieshao"].replace("'","\\\'")
        # 参考地址：https://blog.csdn.net/loujun2016/article/details/82349655
        auj=pymysql.escape_string(self["authJieshao"])
        # auj=repr(self["authJieshao"])
        sql="insert into mingyan(`authName`,`content`,`authTags`,`authLink`,`authJieshao`) values ('%s','%s','%s','%s','%s');" % (an,con,au,aul,auj)

        return sql