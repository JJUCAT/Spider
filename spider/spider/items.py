# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FlowItem(scrapy.Item):
    date = scrapy.Field()
    price = scrapy.Field()
    fluctuation = scrapy.Field()
    main_net = scrapy.Field()
    main_proportion = scrapy.Field()
    huge_net = scrapy.Field()
    huge_proportion = scrapy.Field()
    big_net = scrapy.Field()
    big_proportion = scrapy.Field()
    mid_net = scrapy.Field()
    mid_proportion = scrapy.Field()
    small_net = scrapy.Field()
    small_proportion = scrapy.Field()
    pass
