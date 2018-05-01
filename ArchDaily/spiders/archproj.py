# -*- coding: utf-8 -*-
import scrapy
import re, os
from ArchDaily.items import ArchprojItem, MyImageItem
from scrapy import Selector, Request, log


class ArchprojSpider(scrapy.Spider):
    name = 'archproj'
    allowed_domains = ['www.archdaily.com',
                       'images.adsttc.com']
    # start_urls = ['https://www.archdaily.com/']
    start_urls = ['https://www.archdaily.com/891738/loft-sao-paulo-treszerosete']
    custom_settings = {
        'ITEM_PIPELINES': {
            'ArchDaily.pipelines.MyImagesPipeline': 1
            # 'scrapy.pipelines.images.ImagesPipeline': 1
            # 'scrapy.pipelines.files.FilesPipeline': 1
        },
        'IMAGES_STORE': "./images",
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

        proj_item = ArchprojItem()
        hxs = Selector(response)
        # Get id
        proj_item['id'] = int(re.findall(r"\d{1,}", current_url)[0])
        # Get title
        title = hxs.xpath('//h1[@class="afd-title-big afd-title-big--left afd-title-big--full afd-title-big--bmargin-small afd-relativeposition"]/text()').extract()
        # Add strip() to remove \n
        proj_item['title'] = title.pop().strip()
        # log.msg(proj_item['title'])
        picurls = hxs.xpath('//li[@class="gallery-thumbs-item"]/a/img[@class="b-lazy"]/@data-src').extract()
        # See what is inside. Class name or tag name in browser may wrong!
        # picurls = hxs.xpath('//li[@class="gallery-thumbs-item"]/a/node()').extract()
        img_item = MyImageItem()
        image_paths = []
        for i in range(len(picurls)):
            picurls[i] = picurls[i].replace('thumb_jpg', 'large_jpg')
            # image_paths.append(str(proj_item['id']) + '/' + str(i))
            image_paths.append(str(proj_item['id']) + '/' + str(i) + '.jpg')
        proj_item['picurls'] = picurls
        # Download pictures
        img_item['image_paths'] = image_paths
        img_item['image_urls'] = picurls
        yield img_item
        # log.msg('\n'.join(proj_item['picurls']))
        archinfo_items = hxs.xpath('//li[@class="afd-char-item"]')
        log.msg(len(archinfo_items.extract()))
        archinfo_items.extend(hxs.xpath('//li[@class="afd-char-item article-all-manufacturers hidden"]'))
        log.msg(len(archinfo_items.extract()))
        archinfo_items.extend(hxs.xpath('//li[@class="afd-char-item hide"]'))
        log.msg(len(archinfo_items.extract()))
        for archinfo_item in archinfo_items:
            # log.msg(archinfo_item.extract())
            archinfo_title = archinfo_item.xpath('h3[@class="afd-char-title"]/text()').extract_first()
            # TODO: text and href may be more than 2! Here I need to pair them
            archinfo_text = archinfo_item.xpath('div[@class="afd-char-text"]/a/text()').extract()
            archinfo_href = archinfo_item.xpath('div[@class="afd-char-text"]/a/@href').extract()
            # log.msg(archinfo_href)
            # TODO: Yield to a new DB collection and return the id to proj_item
        # log.msg(hxs.xpath('//*[@id="single-content"]/ul[2]').extract())

