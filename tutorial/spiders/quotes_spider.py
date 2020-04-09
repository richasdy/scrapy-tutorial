import scrapy
from scrapy.loader import ItemLoader
from tutorial.items import QuoteItem

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["toscrape.com"]
    start_urls = ['http://quotes.toscrape.com/']

    # polite spider
    custom_settings = {
        'ITEM_PIPELINES' : {
            'tutorial.pipelines.DuplicatesPipeline': 100,
            'tutorial.pipelines.SaveQuotesPipeline': 200,
            'tutorial.pipelines.JsonLinesExporterPipeline': 300,
        },

        # POLITE SPIDER
        # 'HTTPCACHE_ENABLED': True, # developement only
        'ITEM_PIPELINES' : {
            'tutorial.pipelines.DuplicatesPipeline': 100,
            'tutorial.pipelines.SaveQuotesPipeline': 200,
            'tutorial.pipelines.JsonLinesExporterPipeline': 300,
        },
        'ROBOTSTXT_OBEY' : True,
        # 'USER_AGENT' : 'MyCompany-MyCrawler (bot@mycompany.com)',
        'RANDOMIZE_DOWNLOAD_DELAY' : True,
        # 'DOWNLOAD_DELAY' : 20,
        'DOWNLOADER_MIDDLEWARES' : {
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
            'scrapy_useragents.downloadermiddlewares.useragents.UserAgentsMiddleware': 500,
            # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
            # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
        },
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
        'CONCURRENT_REQUESTS_PER_IP' : 5,
        'ROTATING_PROXY_LIST_PATH' : 'get_proxy.txt'

    }


    def parse(self, response):
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
        yield loader.load_item()
