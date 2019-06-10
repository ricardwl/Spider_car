# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os


class SpiderCarPipeline(object):
    id_list = []

    def process_item(self, item, spider):
        id_ = item['id_']
        if id_ in self.id_list:
            return item
        self.id_list.append(id_)
        with open('./save.csv', 'a+', newline='') as f:
            file_write = csv.writer(f)
            file_write.writerow((item['id_'], item['brand'], item['type_'], item['version_'], item['year']))
           # file_write.writerow((item['id_'],item['name']))
        return item

