# Spider_car
一个小爬虫，爬取了人人二手车和瓜子二手车的车型数据.  
库：spider
## spider框架
主要修改spider文件，在此文件下设计自己的爬虫，pipeline文件中设计一些处理，setting文件中进行一些设置。  
## 汽车车型类别收集
爬虫名：car_list
`car_class_list_spider.py`是对所有车型类别的收集，搜索所有字母开头的车型并保存。  
## 汽车车型数据收集
爬虫名：car_entity  
`car_entity_spider.py`是对所有车型图像数据的收集，根据之前保存的csv文件读取车型，并搜索车型访问相关数据并保存。  
**人人网有反爬机制，对数字字体进行了映射变换，每天都不一样，需要自己去寻找，在`map_num`函数中进行了处理，修改变换规则即可**
## 运行
在Spider_car目录下运行`scrapy crawl [爬虫名]`爬虫名在爬虫文件中设置 
