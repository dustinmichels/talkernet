import scrapy

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
BASE_URL = 'http://apps.carleton.edu'
DIR_BASE_URL = BASE_URL + '/campus/directory'


class StalkerSpider(scrapy.Spider):
    name = "stalker"

    def start_requests(self):
        urls = get_urls()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for person in response.css('li.person'):
            yield scrape_person(person)


def scrape_person(person):
    """Returns dict of scraped data for given person"""

    name = (person.css('h2::text').extract_first() or
            person.css('h2 a::text').extract_first())

    majors = person.css('span.majors span.major::text').extract()
    majors = [m.replace('\u200b', '') for m in majors]  # 0-width space

    minors = person.css('span.majors span.minor::text').extract()
    minors = [m.replace('\u200b', '') for m in minors]  # 0-width space

    year = person.css('span.affiliation::text').extract_first()
    img = BASE_URL + person.css('div.image img::attr(src)').extract_first()
    house = person.css('p.location a::text').extract_first()
    tags = person.css('div.tags a::text').extract()
    email = person.css('div.email a::text').extract_first()

    return dict(
        name=name, year=year, img=img, majors=majors,
        minors=minors, house=house, tags=tags, email=email)


def get_urls(start_year=2018, end_year=2021):
    """Returns list of urls to use for searching"""
    urls = []
    years = [str(y) for y in range(start_year, end_year + 1)]
    for year in years:
        for letter in LETTERS:
            urls.append('{}/?last_name={}&year={}'.format(DIR_BASE_URL, letter, year))
    return urls
