# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
import codecs

class JsonWithEncodingPipeline(object):

    def __init__(self):
        self.file = codecs.open('scraped_data_utf8.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

class ImageCachePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        avatarUrl = item['image']
        yield Request(avatarUrl)

    def item_completed(self, results, item, info):
        image_paths=[x['path'] for ok,x in results if ok]

        if not image_paths:
            print "图片未下载好:%s" % image_paths