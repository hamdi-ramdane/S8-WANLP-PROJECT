import scrapy
from arabic_news_scraper.items import NewsItem

class AljazeeraSpider(scrapy.Spider):
    name = "aljazeera_spider" 
    allowed_domains = ["aljazeera.net"]  
    start_urls = [  "https://www.aljazeera.net/news/",
                    "https://www.aljazeera.net/africa/",
                    "https://www.aljazeera.net/sport/",
                    "https://www.aljazeera.net/opinion/",
                    "https://www.aljazeera.net/travel/",
                    "https://www.aljazeera.net/culture/",
                    "https://www.aljazeera.net/ebusiness/",
                    "https://www.aljazeera.net/tech/",
                    "https://www.aljazeera.net/politics/",
                    "https://www.aljazeera.net/blogs/",
                    "https://www.aljazeera.net/encyclopedia/",
                    "https://www.aljazeera.net/arts/",
                    "https://www.aljazeera.net/turath/",
                    "https://www.aljazeera.net/science/",
                    "https://www.aljazeera.net/lifestyle/",
                    "https://www.aljazeera.net/tag/indepth/",
                    "https://www.aljazeera.net/family/",
                    "https://www.aljazeera.net/where/alquds/",
                    "https://www.aljazeera.net/misc/",
                    "https://www.aljazeera.net/tag/humanrights/"
                  ]  
    custom_settings = {
        'FEEDS': {
            'outputs/aljazeera.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
            },
        }
    }

    def parse(self, response):
        articles = response.css(".gc__content")
        for article in articles:
            item = NewsItem()
            item["title"] = article.css("h3.gc__title a span::text").get()
            item["content"] =  article.css(".gc__excerpt p::text").get() 
            item["pub_date"] = article.css('.gc__date__date .date-simple span[aria-hidden="true"]::text').get()
            yield item