# -*- coding: utf-8 -*-
'''
比赛列表

'''
from lxml import etree
import time
import random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import re


class Matchlist(object):

    def __init__(self):
        self.timeout = 15

        self.chrome_options = Options()
        # 不展示页面
        self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('user-agent=' + self.ua)
        # self.chrome_options.add_argument('--proxy-server=http://%s' % self.proxy)
        self.driver = webdriver.Chrome(executable_path=r'chromedriver', chrome_options=self.chrome_options)
        # self.driver.binary_location = r'/usr/bin/google-chrome'

    def startone(self):
        '''入口'''
        print('开始>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        video_info = {}
        try:
            url = 'https://www.amazon.com/HSI-Professional-Tourmaline-Straightener-Straightens/dp/B001MA0QY2'
            self.driver.get(url + '?currency=USD&language=en_US')
            time.sleep(random.uniform(1, 2))
            pag = self.driver.page_source
            tree = etree.HTML(pag)
            title = tree.xpath('.//span[@id="productTitle"]/text()')
            store_name = tree.xpath('.//a[@id="bylineInfo"]/text()')[0]
            print(11)
            categorys = tree.xpath(
                './/div[@id="wayfinding-breadcrumbs_feature_div"]//span[@class="a-list-item"]/a/text()')
            if categorys:
                categorys = [str(i.strip()) for i in categorys]
                categorys = ','.join(
                    categorys)  # Beauty & Personal Care,Hair Care,Styling Tools & Appliances,Irons,Straighteners
            print(categorys)
            print(2)
            print(store_name)
            print(3)
            print(re.findall(r'Visit the (.*?) Store', store_name))
            print(4)
            if store_name:
                store_name = re.findall(r'Visit the (.*?) Store', store_name)[0]
            print(5)
            print(store_name)
            price1 = tree.xpath('.//span[@id="priceblock_ourprice"]/text()')  # 没有原价的-现价
            # 有原价
            price2 = tree.xpath('.//span[@id="priceblock_dealprice"]/text()')  # 有原价-现价
            origin_price = tree.xpath('.//span[@class="priceBlockStrikePriceString a-text-strike"]/text()')  # 原价
            if price1:
                now_price = price1
                origin_price = price1
            elif price2:
                now_price = price2
            else:
                now_price = 0
                origin_price = 0

            print(6)
            print(now_price)
            print(7)
            print(origin_price)
            print(8)
            #scripts = tree.findall('script', type="text/javascript", text=re.compile('ImageBlockATF'))
            scripts = tree.findall('ImageBlockATF')
            print(scripts)
            scripts = scripts[0].get_text()
            print(scripts)
            str_begin = scripts.find('initial')
            print(str_begin)
            str_end = scripts.find('colorToAsin')
            print(str_end)
            end_str = scripts[str_begin:str_end]
            print(end_str)

            # end_str = (end_str.replace('var dcsServerResponse = ', '')).strip()[:-1]
            # json_info = json.loads(end_str)
            # selectedDealsCount = json_info['selectedDealsCount']
            # sortedDealIDs = json_info['sortedDealIDs']

            # video_info = {
            #     'url': url,  # 干净链接
            #     'asin': url[(url.find('/dp/') + 4):],  # ASIN(product_id)
            #     'currency': 'USD',  # 货币符号
            #     'title': title.strip(),  # 商品标题
            #     'store_name': store_name,  # 店铺名称
            #     'categorys': categorys,
            #     # 品类  Beauty & Personal Care,Hair Care,Styling Tools & Appliances,Irons,Straighteners
            #     'now_price': now_price,  # 现价
            #     'origin_price': origin_price,  # 原价
            #     'images': url,  # 封面图+描述图-5张(第一张就是封面图)
            # }

        except Exception as e:
            print(e)

        finally:
            print('''完事.....''')
        self.driver.quit()
        return


if __name__ == '__main__':
    mclist = Matchlist()
    mclist.startone()
