# -*- coding: utf-8 -*-
import scrapy
import re

from scrapy import Selector, Request, log


class ArchidailySpider(scrapy.Spider):
    name = 'archidaily'
    allowed_domains = ['www.archdaily.com']
    # start_urls = ['https://www.archdaily.com/']
    start_urls = ['https://www.archdaily.com/search/projects/categories/houses']

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

        all_urls = hxs.xpath('//a/@href').extract()
        for url in all_urls:
            # log.msg(url, level=log.CRITICAL)
            # Reduce regx match heuristic,
            if not url.startswith(tuple(ignore_urls)):
                log.msg(url, level=log.CRITICAL)
                # In search result page
                if current_url.startswith('https://www.archdaily.com/search/projects/categories/houses'):
                    # Get project url
                    if re.match('/\d{6}/.*', url):
                        yield Request('https://www.archdaily.com/' + url, callback=self.parse)
                        # log.msg('--Details--' + url, level=log.CRITICAL)
                    # Get next result page
                    elif re.match('/search/projects/categories/houses\?page=\d*', url):
                        yield Request('https://www.archdaily.com/' + url, callback=self.parse)
                        # log.msg('--NextPage--' + url, level=log.CRITICAL)
                # elif re.match('https://www.archdaily.com/\d{6}/.*', current_url):
                #     # Select title
                #     items = hxs.select('//div[@class="afd-title-big afd-title-big--left afd-title-big--full afd-title-big--bmargin-small afd-relativeposition"]/div')
