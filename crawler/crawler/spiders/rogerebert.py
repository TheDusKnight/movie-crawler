import datetime
import re
import uuid

import scrapy


class Rogerebert(scrapy.Spider):
    name = 'rogerebert'
    allowed_domains = ['www.rogerebert.com']
    start_urls = [
        'https://www.rogerebert.com/collections/drama-movies',
        'https://www.rogerebert.com/collections/comedy-movies',
    ]

    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self):
        pass

    def parse(self, response):
        self.logger.info('Index page ' + response.url)

        next_page = response.css('a.pagination-next::attr(href)').get()

        content_pages = response.css('h5.review-stack--title a::attr(href)').getall()
        for page in content_pages:
            yield response.follow(page, callback=self.parse_page1)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        return

    def parse_page1(self, response):
        self.logger.info('Content page ' + response.url)
        uid = uuid.uuid1().hex
        self.logger.info("id " + uid)

        title_year = response.css('h3.cast-and-crew--movie-title::text').get()
        if not title_year:
            title = " "
            year = " "
        else:
            title_year = re.sub("\n", "", title_year)
            title = re.search(r"^[^\(]+", title_year)[0].strip()
            year = re.search(r"\((\w+)\)", title_year).group(1)

        director = response.css('li[itemprop="director"] span::text').get()
        casts = response.css('p.cast-and-crew--detail span::text').getall()
        running_time = response.css('p.cast-and-crew--running-time::text').get()
        if not director:
            # try to find another director location
            director = response.css('ul.cast-and-crew--detail a::text').get()
            if not director:
                director = " "
        if not casts:
            casts = [" "]
        if not running_time:
            running_time = " "
        else:
            running_time = re.sub("\n", "", running_time)

        yield {
            "id": uid,
            "url": response.url,
            "timestamp_crawl": datetime.datetime.now(),
            "title": title,
            "release_date": year,
            "director": director,
            "cast": casts,
            "running_time": running_time,
        }
        return
