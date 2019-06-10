import scrapy
import pandas as pd
import requests
import os
import time
import logging
from .. import items
logging.getLogger('scrapy').setLevel(logging.INFO)


class GuaziCarEntitySpider(scrapy.Spider):

    # config
    name = 'guazi_car_entity'
    img_path = './image_complete2'
    num = 0
    # read csv
    classes = pd.read_csv('guazi.csv')
    classes = [name[0] for name in classes.values.tolist()]
    start_urls = [
        'https://www.guazi.com/www/buy/_%s' % name for name in classes
    ]

    def parse(self, response):
        urls = response.xpath('//a[@class="car-a"]/@href').extract()
        for url in urls:
            # yield
            entity_url = 'https://www.guazi.com'+url
            yield scrapy.Request(url=entity_url,callback=self.parse_entity)

    def parse_entity(self, response):
        self.num = self.num + 1
        if self.num == 40:
            self.num = 0
            time.sleep(10)
        name = response.xpath('//div[@class="product-textbox"]/h2/text()').extract()[0].rstrip().lstrip()

        img_url = response.xpath('//li[@class="fr js-bigpic" and @data-index="1"]/img/@src').extract()[0]
        car_id = response.xpath('//a/@data-clue-id').extract()[0]
        img_name = name.replace(' ', '-', 1)+'_'+car_id

        img = requests.get(img_url,verify=False).content
        # save img
        with open('%s/%s.jpg' % (self.img_path, img_name), 'wb') as f:
            f.write(img)
        # yield
        ls = name.split(' ')
        yield items.EntityItem(id_ = car_id, brand=ls[0], type_=ls[1], year=ls[2],version_=name)