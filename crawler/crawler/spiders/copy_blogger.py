import scrapy
# from scrapy.spiders import CrawlSpider
from bs4 import BeautifulSoup
import urllib

class Crawler(scrapy.Spider):
    name = 'copyblogger'
    allowed_domains = ['copyblogger.com']
    start_urls = [
        'https://copyblogger.com/blog/',
    ]

    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self):
        return

    def parse(self, response):
        print('Current page ' + response.url)
        # nextpage = response.css('.pagination-next a::attr(href)').extract()
        nextpage = response.css('.pagination-next a::attr(href)').getall()
        # nextpagetext = response.css('.pagination-next').extract()

        content_page = response.css('a.entry-title-link::attr(href)').getall()
        for page in content_page:
            yield scrapy.Request(page, callback=self.parse_next_page)

        yield scrapy.Request(nextpage[0], callback=self.parse)


        return

    def parse_next_page(self, response):
        print('Fetched next page ' + response.url)
        return

