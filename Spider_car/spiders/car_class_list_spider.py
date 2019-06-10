import scrapy
from Spider_car import  items


class Car_list_Spider(scrapy.Spider):
    name = "car_list"
   # allowed_domains = ["https://www.renrenche.com/cn/ershouche/?plog_id=16a41fbccbc725712d103d5ada7fb93b"]]
    start_urls = [
        'https://www.renrenche.com/cn/sitemap_%s' % chr(i + 97) for i in range(26)
    ]

    def parse(self, response):
       tags = response.xpath('//li[@class = "series-special"]/a/text()').extract()
       #提取车型字母开头
       letter = response.url[-1]
       id_base = (ord(letter) - ord('a')) * 1000
       for i in range(len(tags)):

           id_ = id_base + i
           tag = tags[i].encode().decode()
           print(tag)
           yield items.ClassItem(id_=id_, name = tag)
