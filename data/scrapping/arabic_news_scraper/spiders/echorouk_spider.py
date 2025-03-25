import scrapy
from arabic_news_scraper.items import NewsItem

class EchoroukSpider(scrapy.Spider):
    name = "echorouk_spider" 
    allowed_domains = ["echoroukonline.com"]  
    start_urls = ["https://www.echoroukonline.com/",
                  "https://www.echoroukonline.com/algeria/",
                  "https://www.echoroukonline.com/world/",
                  "https://www.echoroukonline.com/economy/",
                  "https://www.echoroukonline.com/sport/",
                  "https://www.echoroukonline.com/opinion/",
                  "https://www.echoroukonline.com/jawahir/",
                  "https://www.echoroukonline.com/miscellaneous/",
                  "https://www.echoroukonline.com/tag/%d8%a5%d9%86%d9%81%d9%88%d8%ac%d8%b1%d8%a7%d9%81%d9%8a%d9%83"
                  ]  
    
    custom_settings = {
        'FEEDS': {
            'outputs/echorouk.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
            },
        }
    }

    def parse(self, response):
        links = response.css("h3.ech-card__title a::attr(href)").getall()
        for link in links:
            if link:
                # Ensure the link is absolute
                absolute_url = response.urljoin(link)
                yield scrapy.Request(url=absolute_url, callback=self.parse_linked_page)


    def parse_linked_page(self, response):

        item = NewsItem()
        item["title"] = response.css("h1.ech-sgmn__title::text").get()
        item["content"] = " ".join(response.css(".ech-artx p ::text").getall()).strip()
        item["pub_date"] = response.css('time.ech-card__mtil::text').get()
        item["url"] = response.url 

        yield item