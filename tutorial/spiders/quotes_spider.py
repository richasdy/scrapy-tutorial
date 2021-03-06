import scrapy
from scrapy.loader import ItemLoader
from tutorial.items.QuoteItem import QuoteItem
from scrapy.shell import inspect_response

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']
    # start_urls = ['http://webcache.googleusercontent.com/search?q=cache%3Aquotes.toscrape.com%2F&oq=cache%3Aquotes.toscrape.com%2F&aqs=chrome..69i57j69i58.9678j0j9&sourceid=chrome&ie=UTF-8']
    
    # start_urls = 'http://quotes.toscrape.com/'

    # headers =  {
    #         'Accept': 'application/json,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    #         'Accept-Encoding': 'gzip, deflate, sdch',
    #         'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4',
    #     }

    # polite spider
    custom_settings = {

        # non stucture database
        'JSONLINES_PATH' : 'data/quotes.jl',
        'CSV_PATH' : 'data/quotes.csv',
        'XML_PATH' : 'data/quotes.xml',
        'PICKLE_PATH' : 'data/quotes.pickle',
        'MARSHAL_PATH' : 'data/quotes.marshal',

        'ITEM_PIPELINES' : {
            # 'tutorial.pipelines.SQLiteDuplicatesPipeline.SQLiteDuplicatesPipeline': 100,
            # 'tutorial.pipelines.SQLiteSaveQuotesPipeline.SQLiteSaveQuotesPipeline': 200,
            # 'tutorial.pipelines.PostgreSQLInsertPipeline.PostgreSQLInsertPipeline': 250,
            'tutorial.pipelines.SQLiteInsertPipeline.SQLiteInsertPipeline': 251,
            # 'tutorial.pipelines.JsonLinesExporterPipeline.JsonLinesExporterPipeline': 300,
            # 'tutorial.pipelines.CsvExporterPipeline.CsvExporterPipeline': 400,
            # 'tutorial.pipelines.XmlExporterPipeline.XmlExporterPipeline': 500,
            # 'tutorial.pipelines.PickleExporterPipeline.PickleExporterPipeline': 600,
            # 'tutorial.pipelines.MarshalExporterPipeline.MarshalExporterPipeline': 700,
        },


        #----------------
        # POLITE SPIDER
        #----------------

        'HTTPCACHE_ENABLED': True, # developement only
        # 'ROBOTSTXT_OBEY' : True,
        'RANDOMIZE_DOWNLOAD_DELAY' : True,
        # 'DOWNLOAD_DELAY' : 5,
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
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
        # 'AUTOTHROTTLE_ENABLED' : True,
        # 'AUTOTHROTTLE_DEBUG' : True,

    }

    # def start_requests(self):
    #     yield scrapy.http.Request(self.start_urls, headers=self.headers)


    def parse(self, response):
        # inspect_response(response, self)
        self.logger.info('Parse function called on {}'.format(response.url))
        # quotes = response.xpath("//div[@class='quote']")
        quotes = response.css('div.quote')

        for quote in quotes:
            loader = ItemLoader(item=QuoteItem(), selector=quote)
            # pay attention to the dot .// to use relative xpath
            # loader.add_xpath('quote_content', ".//span[@class='text']/text()")
            loader.add_css('quote_content', '.text::text')
            # loader.add_xpath('author', './/small//text()')
            loader.add_css('tags', '.tag::text')
            quote_item = loader.load_item()
            author_url = quote.css('.author + a::attr(href)').get()
            # go to the author page and pass the current collected quote info
            yield response.follow(author_url, self.parse_author, meta={'quote_item': quote_item})

        # go to Next page
        for a in response.css('li.next a'):
            yield response.follow(a, self.parse)

    def parse_author(self, response):
        quote_item = response.meta['quote_item']
        loader = ItemLoader(item=quote_item, response=response)
        loader.add_css('author_name', '.author-title::text')
        loader.add_css('author_birthday', '.author-born-date::text')
        loader.add_css('author_bornlocation', '.author-born-location::text')
        loader.add_css('author_bio', '.author-description::text')

        # for debugging
        # inspect_response(response, self)

        yield loader.load_item()
