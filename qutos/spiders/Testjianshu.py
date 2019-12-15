import time

import  scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.selector.unified import SelectorList
from qutos.items import QutosItem
class TestJ(scrapy.Spider):
        # 爬虫的名称，不可更改
        name = 'pages1'
        #allowed_domains = ['formoon.github.io']  # 域名称
        start_urls = ['http://quotes.toscrape.com/',
                      # 'http://quotes.toscrape.com/page/2/',
                      # 'http://quotes.toscrape.com/page/3/',
                      # 'http://quotes.toscrape.com/page/4/',
                      # 'http://quotes.toscrape.com/page/5/',
                      # 'http://quotes.toscrape.com/page/6/',
                      # 'http://quotes.toscrape.com/page/7/',
                      # 'http://quotes.toscrape.com/page/8/',
                      # 'http://quotes.toscrape.com/page/9/',
                      # 'http://quotes.toscrape.com/page/10/',
                      ]  # 从这个网址开始执行爬虫，注意默认是http，修改成https
        # scrapy爬虫中不会主动修改页面中的链接，所以自己增加一个类变量用于将相对地址完整成为绝对地址。
        #baseurl = 'https://formoon.github.io'
        #深度爬取http://www.uml.org.cn/python/2019070421.asp
        def parse(self, response):
            udata=response.xpath('/html/body/div/div[2]/div[1]')
            # 获取 下页偏移地址 /page/2/
            url_1=udata.xpath('./nav//a[1]/@href').get()
            rdata=udata.xpath("//div[@class='quote']")
            print(rdata[1].get())
            for x1 in rdata:
                print('*>>'*20)
                content=x1.xpath('./span[@class="text"]/text()').extract_first()
                print('名言内容:'+content)
                authName=x1.xpath('.//small[@class="author"][1]/text()').extract_first()
                print('作者名字:'+authName)
                #  这个函数还是比较智能的  https://www.jianshu.com/p/a9bfc5285a9a
                authLink=response.urljoin(x1.xpath('.//a[@href][1]/@href').get())
                # authLink='http://quotes.toscrape.com'+x1.xpath('.//a[@href][1]/@href').get()
                print('作者简介:'+authLink)
                authTags=x1.xpath('./div[@class="tags"][1]/meta[@class="keywords"]/@content').get()
                print('作者标签:'+authTags)
                items=QutosItem(content='内容:'+content,authTags='作者标签:'+authTags,authName='作者名字:'+authName,authLink='作者链接:'+authLink)
                # dont_filter是一种去重设置、请求方法、地址、的重复请求会被忽略 参看地址:https://www.zhihu.com/question/19793879/answer/312467126
                yield scrapy.Request(authLink,callback=self.paser_1,meta={'item':items},dont_filter=True);
            #print(response.headers)
        # 二级采集回调函数
        def paser_1(self,response):
            items=response.meta['item']
            authJieshao=response.xpath('/html/body/div/div[2]/div/text()').get()
            items['authJieshao']=authJieshao
            # 用yield关键字把它传去管道,item构造完才会 返回。
            yield items

