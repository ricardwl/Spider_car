import scrapy
import pandas as pd
import os
from .. import items
class CarFontSpider(scrapy.Spider):
    #config
    name = 'car_font'

    classes = pd.read_csv('class.csv')
    classes = [name[1] for name in classes.values.tolist()]


    start_urls = [
        'https://www.renrenche.com/cn/ershouche/p1/?keyword=%s' % i for i in classes
    ]

    start_urls.extend(['https://www.renrenche.com/cn/ershouche/p2/?keyword=%s' % i for i in classes])
    id_list = []
    print(len(start_urls))
    font_list = []
    def parse(self, response):

        car_ids = response.xpath('//div[@class="favorite-box"]/@data-car-id').extract()
        car_ids = [id_.encode().decode('utf-8') for id_ in car_ids]
        for car_id in car_ids:
            if car_id in self.id_list:
                continue
            self.id_list.append(car_id)
            car_url = "https://www.renrenche.com/car/%s" % car_id
            yield scrapy.Request(car_url, callback=self.parse_font)

    def parse_font(self, response):

        # find font_name and font_url
        font_name = response.xpath('//div[@class="title"]/h1/@class').extract()[0]
        font_url = 'https://misc.rrcimg.com/ttf/'+font_name+'.ttf'
        if font_name not in self.font_list:
            self.font_list.append(font_name)
            with open('font.txt', 'a+') as f:
                f.write(font_name+'\n\r')
                f.write(response.url+'\n\r')
        #item yield
            yield items.FontItem(name = font_name, url = font_name)


