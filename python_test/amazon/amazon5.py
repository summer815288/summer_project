import requests
from lxml import etree
from requests.exceptions import RequestException
from urllib.parse import urljoin
from multiprocessing import Pool


def get_one_page(url, headers):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(res):
    html = etree.HTML(res)
    title = html.xpath('//*[@id="resultItems"]/li/a/div!/div/h5/span/text()')
    price = html.xpath('//*[@id="resultItems"]/li/a/div/div/div/div!/span[1]/text()')
    for i in range(len(price)): phone = {}
    phone['title'] = title[i]
    phone['price'] = price[i].replace(',', '')
    yield phone


def main(num):
    url = 'https://www.amazon.cn/gp/aw/s/ref=is_pg?rh=i%3Aaps%2Ck%3A%E5%8D%8E%E4%B8%BA%E6%89%8B%E6%9C%BA&page={}'.format(
        num)
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    response = get_one_page(url, headers)
    print(response)
    result = parse_one_page(response)
    result = list(result)
    print(result)


if __name__ == '__main__':
    for i in range(10):
        main(i + 1)
