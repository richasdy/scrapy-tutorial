import requests
from lxml.html import fromstring
def get_proxies():
    url = 'https://free-proxy-list.net/'
    response = requests.get(url)
    parser = fromstring(response.text)
    proxies = set()
    # for i in parser.xpath('//tbody/tr')[:10]:
    for i in parser.xpath('//tbody/tr'):
        if i.xpath('.//td[7][contains(text(),"yes")]'):
            #Grabbing IP and corresponding PORT
            proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
            proxies.add(proxy)
    return proxies

def save_file(list,filename):
    with open(filename, 'w') as f:
        for item in list:
            f.write("%s\n" % item)

proxies = get_proxies()
print(proxies)

save_file(proxies, 'get_proxy.txt')
