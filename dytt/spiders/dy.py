# -*- coding: utf-8 -*-
import re
import scrapy

# 爬取电影天堂
from dytt.items import DyttItem


class DySpider(scrapy.Spider):
    name = 'dy'
    allowed_domains = ['www.dytt8.net']
    start_urls = ['http://www.ygdy8.net/html/gndy/dyzz/index.html']

    page = 1
    url = 'http://www.dytt8.net/html/gndy/dyzz/list_23_%s.html'

    def parse(self, response):
        table_list = response.xpath('//div[@class="co_content8"]/ul//table')
        for table in table_list:
            item = DyttItem()
            item['name'] = table.xpath('.//tr[2]/td[2]//a/text()').extract_first()
            item['time'] = table.xpath('.//tr[3]/td[2]/font/text()').extract_first()
            print(item['name'])
            print(item['time'])
            # 获取详情页面的url
            detail_url = 'http://www.ygdy8.net' + table.xpath('.//tr[2]/td[2]/b/a/@href').extract_first()
            print(detail_url)
            yield item
            yield scrapy.Request(url=detail_url, callback=self.parse_info, meta={'item': item})

        self.page += 1
        if self.page <= 2:
            url = self.url % self.page
            yield scrapy.Request(url=url, callback=self.parse)

    def parse_info(self, response):
        # 获取传递过来的item
        item = response.meta['item']
        image_url = response.xpath('//*[@id="Zoom"]//img[1]/@src').extract_first()
        print(image_url)
        pattern = re.compile(r'◎导　　演　(.*?)<br />')
        ret = pattern.findall(response.text)
        print(len(ret))
        director = ret[0]
        pattern = re.compile(r'◎简　　介(.*?)<br /><br />(.*?)<img')
        ret = pattern.findall(response.text)
        info = ret[1]
        item['image_url'] = image_url
        item['director'] = director
        item['info'] = info
        yield item
