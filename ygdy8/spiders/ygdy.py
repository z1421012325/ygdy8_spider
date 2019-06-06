# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ygdy8.items import crawlygdyItem

import re

class YgdySpider(CrawlSpider):
    name = 'ygdy'
    allowed_domains = ['ygdy8.com']
    start_urls = ['https://www.ygdy8.com/html/gndy/dyzz/index.html']

    rules = (
        Rule(LinkExtractor(allow=r'/html/tv/.*?/index.html'),follow=False),
        # Rule(LinkExtractor(allow=r'/html/tv/.*?/index.html', deny='game'), follow=False),
        Rule(LinkExtractor(allow=r'list_\d+_\d+.html'), follow=True),
        Rule(LinkExtractor(allow=r'/html/gndy/dyzz/\d+/\d+.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        item = crawlygdyItem()

        item['title'] = response.xpath('//div[@class="title_all"]/h1/font/text()').get()
        item['url'] = response.url
        item['download_urls'] = re.findall('"(ftp://.*?)"', response.text)

        yield item