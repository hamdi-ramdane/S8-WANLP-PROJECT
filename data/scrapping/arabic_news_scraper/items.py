import scrapy


class NewsItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    pub_date = scrapy.Field()
    url = scrapy.Field()