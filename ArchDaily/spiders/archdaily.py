# -*- coding: utf-8 -*-
import scrapy
import re,os
from ArchDaily.items import ArchdailyItem
from scrapy import Selector, Request, log


class ArchdailySpider(scrapy.Spider):
    name = 'archdaily'
    allowed_domains = ['www.archdaily.com']
    # start_urls = ['https://www.archdaily.com/']
    start_urls = ['https://www.archdaily.com/search/projects/categories/houses']
    custom_settings = {
        'ITEM_PIPELINES': {
            'ArchDaily.pipelines.MongoDBPipeline': 50
        },
        'MONGO_URI': "./archurl.db",
        'MONGO_DATABASE': "archurl.db"
        # 'MONGODB_SERVER': "localhost",
        # 'MONGODB_PORT': 27017,
        # 'MONGODB_DB': "archdaily",
        # 'MONGODB_COLLECTION': "urllist"
    }

    def parse(self, response):
        ignore_urls = ['https://www.archdaily.com',
                       'http://www.archdaily.com',
                       '//www.archdaily.cn',
                       '//www.plataformaarquitectura.cl',
                       '//www.archdaily.mx',
                       'http://my.archdaily.com/us/labels',
                       'http://account.archdaily.com/us/users/profile',
                       '//www.archdaily.com',
                       '#',
                       'https://chrome.google.com',
                       '//boty.archdaily.com']

        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()

        hxs = Selector(response)

        if current_url.startswith('https://www.archdaily.com/search/projects/categories/houses'):
            items = hxs.xpath('//li[@class="afd-search-list__item nrd-search-list__item"]').extract()
            # log.msg('items: ' + ''.join(items), level=log.CRITICAL)
            title = hxs.xpath(
                '//li[@class="afd-search-list__item nrd-search-list__item"]//h2[@class="afd-search-list__title"]/text()').extract()
            url = hxs.xpath(
                '//li[@class="afd-search-list__item nrd-search-list__item"]//a[@class="afd-search-list__link"]/@href').extract()
            pic = hxs.xpath(
                '//li[@class="afd-search-list__item nrd-search-list__item"]//img[@class="afd-search-list__img "]/@src').extract()
            if len({len(items), len(title), len(url), len(pic)}) is not 1:
                # Handle wrong items
                os._exit()
            item = ArchdailyItem()
            for i in range(len(items)):
                item['title'] = title[i]
                item['url'] = url[i]
                item['pic'] = pic[i]
                yield item
            # log.msg('title: '+title, level=log.CRITICAL)
            # log.msg('url: '+''.join(url), level=log.CRITICAL)
            # log.msg('pic: '+pic, level=log.CRITICAL)
        #
        # all_urls = hxs.xpath('//a/@href').extract()
        # for url in all_urls:
        #     # log.msg(url, level=log.CRITICAL)
        #     # Reduce regx match heuristic,
        #     if not url.startswith(tuple(ignore_urls)):
        #         # log.msg(url, level=log.CRITICAL)
        #         # In search result page
        #         if current_url.startswith('https://www.archdaily.com/search/projects/categories/houses'):
        #             # Get project url
        #             if re.match('/\d{6}/.*', url):
        #                 # yield Request('https://www.archdaily.com/' + url, callback=self.parse)
        #                 log.msg(url, level=log.CRITICAL)
        #                 # log.msg('--Details--' + url, level=log.CRITICAL)
        #             # Get next result page
        #             elif re.match('/search/projects/categories/houses\?page=\d*', url):
        #                 url = 'https://www.archdaily.com' + url
        #                 yield Request(url, callback=self.parse)
        #                 # log.msg('--NextPage--' + url, level=log.CRITICAL)
        #         # elif re.match('https://www.archdaily.com/\d{6}/.*', current_url):
        #         #     # Select title
        #         #     items = hxs.select('//div[@class="afd-title-big afd-title-big--left afd-title-big--full afd-title-big--bmargin-small afd-relativeposition"]/div')
        #