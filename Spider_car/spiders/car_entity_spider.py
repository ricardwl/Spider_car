import os
import scrapy
import requests
import logging
import re
import pandas as pd
from .. import items

logging.getLogger('scrapy').setLevel(logging.INFO)


def map_num(string):
    # there is a font map in the car type
    # 0 1 2 3 4 5 6 7 8 9
    # 0 2 1 4 3 8 6 7 5 9
    dic = {'1': '2', '2': '1', '3': '4', '4': '3', '5': '8', '8': '5'}
    new = []
    for s in string:
        if s in dic.keys():
            new.append(dic[s])
        else:
            new.append(s)
    return ''.join(new)


class CarEntitySpider(scrapy.Spider):
    # config
    image_path = './image_complete'
    pg_start = 1
    pg_end = 50

    classes = pd.read_csv('class.csv')
    classes = [name[1] for name in classes.values.tolist()]

    name = 'car_entity'
    start_urls = [
        'https://www.renrenche.com/cn/ershouche/p1/?keyword=%s' % i for i in classes
    ]

    start_urls.extend(['https://www.renrenche.com/cn/ershouche/p2/?keyword=%s' % i for i in classes])
    id_list = []
    print(len(start_urls))

    def parse(self, response):
        if not os.path.exists(self.image_path):
            os.makedirs(self.image_path)

        car_ids = response.xpath('//div[@class="favorite-box"]/@data-car-id').extract()
        car_ids = [id_.encode().decode('utf-8') for id_ in car_ids]
        for car_id in car_ids:
            if car_id in self.id_list:
                continue
            self.id_list.append(car_id)
            car_url = "https://www.renrenche.com/car/%s" % car_id
            yield scrapy.Request(car_url, callback=self.parse_entity)

    def parse_entity(self, response):
        img_src = response.xpath('//img[@data-start="1" and @class="main-pic" ]/@data-src').extract()[0]
        img_name_id = response.url.split('/')[-1]
        old_name = response.xpath('//div[@class="title"]/h1/text()').extract()[-1].rstrip()

        img_name = map_num(old_name)+'_'+img_name_id
        url = 'https:' + img_src

        img = requests.get(url, verify=False).content
        with open('%s/%s.jpg' % (self.image_path, img_name), 'wb') as f:
            f.write(img)
        # item yield
        try:
            info = response.xpath('//div[class="title"]/h1/text()').extract().encoder().decoder()
        except Exception:
            return
        # 2012款 index from 0 to -2
        year = re.findall(r"\d{4}款", info)[0][0:-2]
        tmp, version_ = re.split(r"\d{4}款", info)
        try:
            brand, type_ = tmp.split('-', maxsplit=1)
        except Exception:
            brand, type_ = tmp.split(' ', maxsplit=1)
        img_id = response.url.split("/")[-1]
        yield items.EntityItem(id_=img_id, brand=brand, type_=type_, year=year, version_=version_)

