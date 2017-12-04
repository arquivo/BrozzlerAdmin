from urlparse import urlsplit  # python 2

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ProspectionSpider(CrawlSpider):
    name = 'Arquivo-web-crawler'
    start_urls = ''
    allowed_domains = ['24.sapo.pt']

    custom_settings = {
        'BOT_NAME': 'Arquivo-web-crawler',
        'DOWNLOAD_DELAY': 0.25,
        'CONCURRENT_REQUESTS_PER_IP': 1,
        'DEPTH_LIMIT': 3
    }

    rules = (Rule(LinkExtractor(), follow=True, callback='parse_obj'),)

    # TODO Accept multiple URLs
    def __init__(self, url='', *args, **kwargs):
        super(ProspectionSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]

        parsed_url = urlsplit(url)
        self.allowed_domains = [parsed_url.netloc]

    def parse_obj(self, response):
        with open('{}_outlinks.txt'.format(urlsplit(response.url).netloc), 'a') as f:
            for link in LinkExtractor(allow=(), tags=('source', 'style', 'script', 'a', 'img', 'link', 'meta'),
                                      attrs=('href', 'srcset', 'data-src'),
                                      deny=self.allowed_domains).extract_links(response):
                f.write('Outlink: {}\n'.format(link.url))
