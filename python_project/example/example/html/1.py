from scrapy.http import HtmlResponse

html1 = open('../html/example1.html').read()
html2 = open('../html/example2.html').read()
response1 = HtmlResponse(url='http://example1.com', body=html1, encoding='utf8')
response2 = HtmlResponse(url='http://example2.com', body=html2, encoding='utf8')
print(response1)
print(11111)
print(response2)

from scrapy.linkextractors import LinkExtractor

le = LinkExtractor()
links = le.extract_links(response2)
print(links)

import re


def process(value):
    # m = re.search("javascript:goToPage('(.*?))'", value)
    m = re.search("javascript:goToPage\('(.*?)'", value)
    if m:
        value = m.group(1)
        return value


le = LinkExtractor(process_value=process)
links = le.extract_links(response2)
print(22222)
print(links)
