import scrapy
import uuid
from datetime import datetime


class Metacritic(scrapy.Spider):
    name = 'metacritic'
    allowed_domains = ['www.metacritic.com']

    start_urls = [
        'https://www.metacritic.com/browse/movies/people/popular',
    ]

    custom_settings = {
        'LOG_LEVEL': 'INFO',
    }

    def __init__(self):
        pass

    def parse(self, response):
        self.logger.info('Index page ' + response.url)

        next_page = response.css('span.flipper.next a::attr(href)').get()

        content_pages = response.css('div.title a::attr(href)').getall()
        for page in content_pages:
            yield response.follow(page, callback=self.parse_page1)

        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        return

    def parse_page1(self, response):
        self.logger.info('Content page ' + response.url)
        uid = uuid.uuid1().hex
        self.logger.info("id " + uid)

        name = response.css('h1.person_title::text').get()
        if not name:
            name = " "
        else:
            name = name.strip()
            if name.lower() == "tbd" or name.lower() == "tba":
                name = " "


        # 所有title, year, role集合
        titles = response.css('table.credits.person_credits td.title.brief_metascore a::text').getall()
        years = response.css('table.credits.person_credits td.year::text').getall()
        roles = response.css('table.credits.person_credits td.role::text').getall()

        # limits to at most 5 movies
        limit = min(5, len(titles))  # if not titles, then for loop will not be executed
        movies = []
        for i in range(limit):
            cur_title = titles[i]
            cur_year = years[i]
            cur_role = roles[i]

            if not cur_title:
                cur_title = " "
            else:
                cur_title = cur_title.strip()
                if cur_title.lower() == "tbd" or cur_title.lower() == "tba":
                    cur_title = " "

            if not cur_year:
                cur_year = -1
            else:
                cur_year = cur_year.strip()
                if cur_year.lower() == "tbd" or cur_year.lower() == "tba":
                    cur_year = -1
                else:
                    try:
                        cur_year = datetime.strptime(cur_year, '%b %d, %Y').year
                    except ValueError:
                        self.logger.info("Date does not match pattern, set to -1")
                        cur_year = -1

            if not cur_role:
                cur_role = " "
            else:
                cur_role = cur_role.strip()
                if cur_role.lower() == "tbd" or cur_role.lower() == "tba":
                    cur_role = " "

            movies.append({"name": cur_title, "year": cur_year, "role": cur_role})

        yield {
            "id": uid,
            "url": response.url,
            "timestamp_crawl": datetime.now(),
            "name": name,
            "movies": movies,
        }

        return
