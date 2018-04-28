# -*- coding: utf-8 -*-
import scrapy
import re, os
from ArchDaily.items import ArchprojItem
from scrapy import Selector, Request, log


class ArchprojSpider(scrapy.Spider):
    name = 'archproj'
    allowed_domains = ['www.archdaily.com',
                       'images.adsttc.com']
    # start_urls = ['https://www.archdaily.com/']
    start_urls = ['https://www.archdaily.com/891738/loft-sao-paulo-treszerosete']
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
        'MONGO_COLLECTION': "archproj"
    }

    def parse(self, response):
        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()
        item = ArchprojItem()

        hxs = Selector(response)
        # Get title
        title = hxs.xpath('//h1[@class="afd-title-big afd-title-big--left afd-title-big--full afd-title-big--bmargin-small afd-relativeposition"]/text()').extract()
        # Add strip() to remove \n
        item['title'] = title.pop().strip()
        log.msg(item['title'])
        picurls = hxs.xpath('//li[@class="gallery-thumbs-item"]/a/img[@class="b-lazy b-loaded"]/@src').extract()
        log.msg(len(picurls))
        for i in range(len(picurls)):
            picurls[i] = picurls[i].replace('thumb_jpg', 'slideshow')
        item['picurls'] = picurls
        log.msg('\n'.join(item['picurls']))


