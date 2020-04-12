import requests
from lxml.html import fromstring
from selenium import webdriver

def get_proxies():
    url = 'https://free-proxy-list.net/'
    wd = webdriver.Chrome('./chromedriver')
    wd.get(url)
    response = wd.page_source
    parser = fromstring(response)
    proxies = set()
    array_proxy = wd.execute_script("return $('#proxylisttable').DataTable().rows().data().toArray()")
    return array_proxy
    
def save_file(list,filename):
    with open(filename, 'w') as f:
        for item in list:
            if item[6]=="yes":
                f.write(item[0]+':'+item[1]+'\n')

proxies = get_proxies()
print(proxies)

save_file(proxies, 'get_proxy.txt')
