# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy import Selector, Request


class ArchidailySpider(scrapy.Spider):
    name = 'archidaily'
    allowed_domains = ['www.archdaily.com']
    # start_urls = ['https://www.archdaily.com/']
    start_urls = ['https://www.archdaily.com/search/projects/categories/houses']

    def parse(self, response):
        current_url = response.url
        body = response.body
        unicode_body = response.body_as_unicode()

        hxs = Selector(response)

        all_urls = hxs.xpath('href').extract()
        for url in all_urls:
            if url.startswith('https://www.archdaily.com/'):
                if re.match('https://www.archdaily.com/\d*/.*.html', url):
                    yield Request(url, callback=self.parse)
