import re
import scrapy

from bs4 import BeautifulSoup


class ImagineeringSpider(scrapy.Spider):
    name = 'ImagineeringSpider'
    allowed_domains = ['jobs.disneycareers.com']

    template = 'http://jobs.disneycareers.com/search-jobs?p={}&ascf=[%7B%22key%22:%22custom_fields.IndustryCustomField%22,%22value%22:%22Walt+Disney+Imagineering%22%7D]'

    start_urls = [
        template.format(1),
    ]

    def parse(self, response):
        bs = BeautifulSoup(
            response.text,
            features='html.parser'
        )

        rows = bs.select('#search-results-list tr')
        if len(rows) > 0:
            for row in rows:
                cols = row.select('td')
                if len(cols) < 3:
                    continue

                link = cols[0].select('a')[0].attrs['href']
                cat_id = re.search(r'(?<=\/)(\d+)(?=\/\d+$)', link)
                job_id = re.search(r'(?<=\/)(\d+)$', link)

                yield {
                    'cat_id': cat_id.group(0),
                    'job_id': job_id.group(0),
                    'title': re.sub('\s+', ' ', cols[0].text).strip(),
                    'date': re.sub('\s+', ' ', cols[1].text).strip(),
                    'brand': re.sub('\s+', ' ', cols[2].text).strip(),
                    'location': re.sub('\s+', ' ', cols[3].text).strip(),
                    'req_id': '',
                    'url': f'https://jobs.disneycareers.com{link}',
                }

            next = bs.select('.pagination-paging .next:not(.disabled)')
            if len(next) > 0:
                ## push the next button...
                p = int(re.sub(r'/search-jobs&p=', '', next[0].attrs['href']))
                yield response.follow(self.template.format(p), callback=self.parse)
