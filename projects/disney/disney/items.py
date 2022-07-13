# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DisneyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImagineeringJobPostItem(scrapy.Item):
    cat_id = scrapy.Field()
    job_id = scrapy.Field()
    req_id = scrapy.Field()
    title = scrapy.Field()
    date = scrapy.Field()
    brand = scrapy.Field()
    location = scrapy.Field()
    url = scrapy.Field()
