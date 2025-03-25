from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from arabic_news_scraper.arabic_news_scraper.spiders.aljazeera_spider import AljazeeraSpider
from arabic_news_scraper.spiders.alarbiya_spider import AlarabiyaSpider
from arabic_news_scraper.spiders.bbc_spider import BBCSpider
from arabic_news_scraper.spiders.echorouk_spider import EchoroukSpider

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(AljazeeraSpider) # good
process.crawl(EchoroukSpider)  # good
process.start()