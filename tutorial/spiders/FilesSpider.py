import scrapy
from scrapy.loader import ItemLoader
from tutorial.items.FileItem import FileItem
from scrapy.shell import inspect_response

class FilesSpider(scrapy.Spider):
    name = "files"
    allowed_domains = ["google.com"]
    start_urls = ['https://google.com/']
    custom_settings = {

        'CSV_PATH' : 'data/files.csv',

        'FILES_STORE' : 'data/files',
        # 'FILES_URLS_FIELD' : 'file_urls',
        # 'FILES_RESULT_FIELD' : 'files',

        'IMAGES_STORE' : 'data/images',
        # 'IMAGES_URLS_FIELD' : 'image_urls',
        # 'IMAGES_RESULT_FIELD' : 'images',
        
        'ITEM_PIPELINES' : {
            'scrapy.pipelines.files.FilesPipeline': 1,
            'scrapy.pipelines.images.ImagesPipeline': 2,
            'tutorial.pipelines.CsvExporterPipeline.CsvExporterPipeline': 400,
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

    def parse(self, response):
        self.logger.info('Parse function called on {}'.format(response.url))

        # loader = ItemLoader(item=FileItem(), selector=response)
        # loader.add_css('header', 'title::text')
        # loader.add_value('url', response.url)
        # absolute_url = response.urljoin(response.css('#hplogo::attr(src)').get())
        # # file g bisa pakai itemloader, kare url harus berbentuk array
        # loader.add_value('image_urls', [absolute_url])
        # loader.add_value('file_urls', [absolute_url])
        # item = loader.load_item()

        item = FileItem()
        item['header'] = response.css('title::text').get()
        item['url'] = response.url
        item['image_urls'] = [response.urljoin(response.css('#hplogo::attr(src)').get())]
        item['file_urls'] = [response.urljoin(response.css('#hplogo::attr(src)').get()),'https://cdn.vox-cdn.com/thumbor/0KnnXd7iQ88LzmeFKWza0g-ba88=/0x0:2000x1285/920x613/filters:focal(840x483:1160x803):format(webp)/cdn.vox-cdn.com/uploads/chorus_image/image/57495335/google_buddies_top.0.jpg']

        yield item

    
