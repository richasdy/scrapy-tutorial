import scrapy
import csv
from tutorial.items.SpringerBookItem import SpringerBookItem

class SpringerEbookSpider(scrapy.Spider):
    name = "springer"
    allowed_domains = ["springer.com"]

    start_urls = []
    
    with open("data/Springer Ebooks.csv", "r") as f:
        books = csv.reader(f, delimiter=';')
        next(books) # skip header row
        for book in books:
            start_urls.append(book[4])

    start_urls = ['http://link.springer.com/openurl?genre=book&isbn=978-3-030-19128-3']

    # polite spider
    custom_settings = {
        'CSV_PATH' : 'data/quotes.csv',
        'ITEM_PIPELINES' : {
            'tutorial.pipelines.CsvExporterPipeline.CsvExporterPipeline': 400,
        },

        #----------------
        # POLITE SPIDER
        #----------------
        'HTTPCACHE_ENABLED': True, # developement only
        # 'ROBOTSTXT_OBEY' : True,
        'RANDOMIZE_DOWNLOAD_DELAY' : True,
        'DOWNLOAD_DELAY' : 5,
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        },
        # 'USER_AGENT' : 'MyCompany-MyCrawler (bot@mycompany.com)',
        # https://developers.whatismybrowser.com/useragents/explore/
        'USER_AGENTS' : [ # rotate user agent
            ('Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/57.0.2987.110 '
            'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/61.0.3163.79 '
            'Safari/537.36'),  # chrome
            ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) '
            'Gecko/20100101 '
            'Firefox/55.0')  # firefox
        ],
        'COOKIES_ENABLED' : False,
        'CONCURRENT_REQUESTS_PER_IP' : 10,
        # https://free-proxy-list.net
        # python get_proxy.py
        'ROTATING_PROXY_LIST_PATH' : 'get_proxy.txt',
        'DEFAULT_REQUEST_HEADERS' : {
            'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
            'Referer': 'http://www.google.com' 
        },
        'AUTOTHROTTLE_ENABLED' : True,
        # 'AUTOTHROTTLE_DEBUG' : True,

    }

    def parse(self, response):
        
        self.logger.info('Parse function called on {}'.format(response.url))

        # manual load to item
        item = SpringerBookItem()

        item['title'] = response.css('h1::text').extract_first()
        item['first_author_name'] = response.css('.authors__name::text').extract_first()
        item['file_urls'] = [response.urljoin(response.css('.c-button::attr(href)').get())]
        item['doi'] = response.css('#doi-url::text').get()
        item['copyright_info'] = response.css('#copyright-info::text').get()
        item['publisher_name'] = response.css('#publisher-name::text').get()
        item['print_isbn'] = response.css('#print-isbn::text').get()
        item['electronic_isbn'] = response.css('#electronic-isbn::text').get()
        
        print(item)

        return item

        
