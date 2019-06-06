# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import pymongo
from scrapy.conf import settings
from ygdy8.items import Ygdy8Item,crawlygdyItem



class Ygdy8Pipeline(object):

    def __init__(self):
        name = settings.get('BOT_NAME')

        a = ['tag','title','url','download_urls']
        self.f = open('{}.csv'.format(name),'a',newline='',encoding='utf-8')
        self.w = csv.writer(self.f)
        self.w.writerow(a)


        b = ['title', 'url', 'download_urls']
        self.f1 = open('{}1.csv'.format(name), 'a', newline='', encoding='utf-8')
        self.w1 = csv.writer(self.f1)
        self.w1.writerow(b)


        mongodb_host = settings.get('MONGODB_HOST')
        mongodb_post = settings.get('MONGODB_POST')
        self.client = pymongo.MongoClient(host=mongodb_host,port=mongodb_post)
        self.db = self.client[name]


    # TODO 可以使用这个代替 试试使用spider,setings.get('xxxx)来获取settings中的值 ???
    # def open_spider(self,spider):
    #     name = spider.name
    #
    #     a = ['tag', 'title', 'url', 'download_urls']
    #     self.f = open('{}.csv'.format(name), 'a', newline='', encoding='utf-8')
    #     self.w = csv.writer(self.f)
    #     self.w.writerow(a)
    #
    #     b = ['title', 'url', 'download_urls']
    #     self.f1 = open('{}1.csv'.format(name), 'a', newline='', encoding='utf-8')
    #     self.w1 = csv.writer(self.f1)
    #     self.w1.writerow(b)
    #
    #     mongodb_host = settings.get('MONGODB_HOST')
    #     mongodb_post = settings.get('MONGODB_POST')
    #     self.client = pymongo.MongoClient(host=mongodb_host, port=mongodb_post)
    #     self.db = self.client[name]


    def process_item(self, item, spider):
        try:
            if isinstance(item,Ygdy8Item):
                jihe = item['tag']

                ii = {}
                ii['title'] = item['title']
                ii['url'] = item['url']
                ii['download_urls'] = item['download_urls']
                # self.db[jihe].update({'url':ii['url']},{'$set':ii},True)
                self.db[jihe].insert(ii)
                self.w.writerow([item['tag'],item['title'],item['url'],item['download_urls']])


            elif isinstance(item,crawlygdyItem):
                # name = spider.name
                # self.db[name].update({'url':item['url']},{'$set':item},True)
                # self.db[name].insert(dict(item))
                self.w1.writerow([item['title'], item['url'], item['download_urls']])



        except:
            if isinstance(item, Ygdy8Item):
                with open('erorr_save.txt','a')as f:
                    f.write(str(item))
                    f.write('\n')

            elif isinstance(item, crawlygdyItem):
                with open('erorr_save1.txt','a')as f:
                    f.write(str(item))
                    f.write('\n')

        return item



    def close_spider(self,spider):
        self.f.close()
        self.f1.close()
        self.client.close()