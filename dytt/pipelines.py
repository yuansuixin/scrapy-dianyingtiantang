# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class DyttPipeline(object):
    def open_spider(self,spider):
        print('*******************')
        self.fp = open('movie.txt','w',encoding='utf-8')

    def process_item(self, item, spider):
        obj = dict(item)
        string = json.dumps(obj,ensure_ascii=False)
        print('67890876')
        print(string)
        self.fp.write(string+'\n')
        print('&&&&&&&&&&&&&&&&&&&&&')
        return item

    def close_spider(self,spider):
        self.fp.close()