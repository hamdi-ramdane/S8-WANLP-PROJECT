import scrapy
from arabic_news_scraper.items import NewsItem

class ElkhabarSpider(scrapy.Spider):
    name = "elkhabar_spider" 
    allowed_domains = ["elkhabar.com"]  
    start_urls = ["https://www.elkhabar.com/"]  
    
    custom_settings = {
        'FEEDS': {
            'outputs/elkhabar.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True,
            },
        }
    }

    def parse(self, response):
        links = response.css("a.title-link.main_article.highlighted_article::attr(href)").getall()
        for link in links:
            if link:
                # Ensure the link is absolute
                absolute_url = response.urljoin(link)
                yield scrapy.Request(url=absolute_url, callback=self.parse_linked_page)

    def parse_linked_page(self, response):

        item = NewsItem()
        item["title"] = response.css("h1.title.blue-text::text").get()
        item["content"] =  response.css("#article_body_content p::text").getall() 
        item["pub_date"] = response.css('.time-blog::text').get()

        yield item