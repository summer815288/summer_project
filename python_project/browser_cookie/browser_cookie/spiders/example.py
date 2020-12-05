import scrapy
from scrapy import Request

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']
    url = 'https://www.zhihu.com/settings/profile'

    def parse(self, response):
        pass
