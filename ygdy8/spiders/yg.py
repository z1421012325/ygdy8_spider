# -*- coding: utf-8 -*-
import re
import scrapy
from ygdy8.items import Ygdy8Item

class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['ygdy8.com']
    start_urls = ['https://www.ygdy8.com/html/gndy/dyzz/index.html']

    def parse(self, response):
        lis = response.xpath('//div[@class="contain"]//li')
        # 最新和经典,游戏不需要
        for li in lis[2:-5]:
            tag = li.xpath('.//a/text()').get()

            link = response.urljoin(li.xpath('.//a/@href').get())

            yield scrapy.Request(url=link,
                                 callback=self.index_page,
                                 meta={'item':tag})


    def index_page(self,response):
        tag = response.meta.get('item')

        # 由于电视频道和电影频道xpath规则不同,但是re规则相同,re提取
        links = re.findall('href="(.*?)" class="ulink',response.text)
        if links:
            for link in links:
                link = response.urljoin(link)
                yield scrapy.Request(url=link,
                                     callback=self.content,
                                     meta={'item':tag})
        # 下一页
        next_url = response.urljoin(response.xpath('//a[contains(text(),"下一页")]/@href').get())
        if next_url:
            yield scrapy.Request(url=next_url,
                                 callback=self.index_page,
                                 meta={'item': tag})


    def content(self,response):
        tag = response.meta.get('item')

        item = Ygdy8Item()

        item['tag'] = tag
        item['title'] = response.xpath('//div[@class="title_all"]/h1/font/text()').get()
        item['url'] = response.url
        item['download_urls'] = re.findall('"(ftp://.*?)"',response.text)

        yield item


