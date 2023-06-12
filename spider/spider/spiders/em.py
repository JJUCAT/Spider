import scrapy
# from spider.items import FlowItem

class EmSpider(scrapy.Spider):
    name = "em"
    allowed_domains = ["data.eastmoney.com"]
    start_urls = ["https://data.eastmoney.com/zjlx/002261.html"]

    def parse(self, response):
        filename = "002261.html"
        open(filename, 'wb+').write(response.body)
        pass