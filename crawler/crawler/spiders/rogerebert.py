import scrapy
# from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup
import urllib

class Rogerebert(scrapy.Spider):
    name = 'rogerebert'
    allowed_domains = ['www.rogerebert.com']
    start_urls = [
        # 'https://copyblogger.com/blog/',
        'https://www.rogerebert.com/collections/drama-movies',
        'https://www.rogerebert.com/collections/comedy-movies',
    ]

    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self):
        return

    def parse(self, response):
        print('Current page ' + response.url)
        nextpage = response.css('a.pagination-next::attr(href)').get()
        # nextpagetext = response.css('.pagination-next').extract()

        # yield scrapy.Request(nextpage, callback=self.parse)
        yield response.follow(nextpage, callback=self.parse)
        return


    def parse_next_page(self, response):
        print('Fetched next page' + response.url)
        return

