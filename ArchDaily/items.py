# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArchdailyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    pic = scrapy.Field()
    id = scrapy.Field()
    date = scrapy.Field()


class ArchprojItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field()
    picurls = scrapy.Field()
    archinfo = scrapy.Field()


class MyImageItem(scrapy.Item):
    image_paths = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
