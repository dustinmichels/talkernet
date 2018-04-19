import scrapy

# Global vars
START_YEAR = 2018
END_YEAR = 2021
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

    name = person.css('h2::text').extract_first() or person.css('h2 a::text').extract_first()
    first_name, last_name = name.split(' ', 1)

    majors = person.css('span.majors span.major::text').extract()
    majors = [m.replace('\u200b', '') for m in majors]  # remove 0-width space

    minors = person.css('span.majors span.minor::text').extract()
    minors = [m.replace('\u200b', '') for m in minors]  # remove 0-width space

    location = (person.css('p.location a::text').extract_first() or
                ', '.join(person.css('p.location::text').extract()))

    # dorm_full = person.css('p.location a::text').extract_first()
    # house_full = person.css('p.location::text').extract()
    #
    # if house_full:
    #     house_full = ', '.join(house_full)
    #
    # location = dorm_full or house_full
    #
    # if dorm_full:
    #     _dorm = dorm_full.split(' ')
    #     dorm_building = ' '.join(_dorm[:-1])
    #     dorm_number = _dorm[-1]
    # else:
    #     dorm_building = None
    #     dorm_number = None

    year = person.css('span.affiliation::text').extract_first()
    img = BASE_URL + person.css('div.image img::attr(src)').extract_first()
    tags = person.css('div.tags a::text').extract()
    email = person.css('div.email a::text').extract_first()
    _id = email.split('@')[0]

    return dict(
        _id=_id, first_name=first_name, last_name=last_name, year=year, img=img,
        majors=majors, minors=minors, location=location, tags=tags, email=email)


def get_urls(start_year=START_YEAR, end_year=END_YEAR):
    """Returns list of urls to use for searching"""
    urls = []
    years = [str(y) for y in range(start_year, end_year + 1)]
    for year in years:
        for letter in LETTERS:
            urls.append('{}/?last_name={}&year={}'.format(DIR_BASE_URL, letter, year))
    return urls
