# -*- coding: utf-8 -*-
import scrapy
import re, os, datetime
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
        # For remote DB
        # 'MONGO_URI': "mongodb://archdaily_0:ucBAOcwLHc8gofep@cluster0-shard-00-00-naxzz.mongodb.net:27017,cluster0-shard-00-01-naxzz.mongodb.net:27017,cluster0-shard-00-02-naxzz.mongodb.net:27017/test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin",
        # 'MONGO_DATABASE': "archdaily",
        # 'MONGO_COLLECTION': "archurl"
        # For local DB
        'MONGO_URI': "mongodb://127.0.0.1:27017",
        'MONGO_DATABASE': "archdaily",
        'MONGO_COLLECTION': "archurl"
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

        hxs = Selector(response)
        # Enter the arch list page
        if current_url.startswith('https://www.archdaily.com/search/projects/categories/houses'):
            item = ArchdailyItem()
            # Read and parser current list page
            item_anchors = hxs.xpath('//li[@class="afd-search-list__item nrd-search-list__item"]/a')
            # log.msg('\n'.join(item_anchors))
            for item_anchor in item_anchors:
                item['title'] = item_anchor.xpath('h2[@class="afd-search-list__title"]/text()').extract_first()
                item['url'] = 'https://www.archdaily.com' + item_anchor.xpath('@href').extract_first()
                item['pic'] = item_anchor.xpath('figure/img[@class="afd-search-list__img "]/@src').extract_first().replace('small_jpg', 'large_jpg')
                item['date'] = datetime.datetime.now().strftime("%Y%m%d")
                # log.msg(item)
                yield item
            # # Get next page url
            # next_url = hxs.xpath('//a[@rel="next" and @class="next" and text()="NEXT ›"]/@href').extract()
            # # Check if current page is the last one
            # # If it is, go back to the first page
            # if next_url is None:
            #     next_url = hxs.xpath('//a[@class="next" and text()="First"]/@href').extract()
            # # Add .pop() to pop url out of the list
            # next_url = 'https://www.archdaily.com' + next_url.pop()
            # yield Request(next_url, callback=self.parse)

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
