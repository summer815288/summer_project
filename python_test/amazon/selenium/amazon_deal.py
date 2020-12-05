# -*- coding: utf-8 -*-
'''
deal列表

'''
from lxml import etree
import time
import random
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import json
import redis


class Matchlist(object):

    def __init__(self):
        self.timeout = 15

        self.chrome_options = Options()
        # 不展示页面
        # self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--disable-gpu')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('user-agent=' + self.ua)   自己的ua
        # self.chrome_options.add_argument('--proxy-server=http://%s' % self.proxy)  公司的代理ip
        self.driver = webdriver.Chrome(executable_path=r'chromedriver', chrome_options=self.chrome_options)
        # self.driver.binary_location = r'/usr/bin/google-chrome'

        redis = self.redis.StrictRedis(host=self.settings['REDIS_HOST'], port=6379, decode_responses=True,
                                      password=self.settings['REDIS_PARAMS']['password'])

        def set_tiktok(self, value):
            self.conn.rpush(self.settings['REDIS_KEYS']['tiktok'], value)

        def set_tiktok_video(self, value):
            self.conn.rpush(self.settings['REDIS_KEYS']['tiktok_video'], value)

        def set_url_detail(self, value):
            self.conn.rpush(self.settings['REDIS_KEYS']['url_detail'], value)

    def page_spider(self):
        # 存储操作

        pag = self.driver.page_source
        tree = etree.HTML(pag)
        body = tree.xpath('//div[@class="a-row"]//a[@class="a-link-normal"]/@href')
        print(body)
        if len(body) > 0:
            for href in body:
                if href and '/dp/' in href:
                    str_end = href.find('/ref=')
                    if str_end:
                        href = href[0:str_end]
                    # 把本次请求的href重新放入队列中
                    red.set_url_detail(json.dumps({'url': href}))
                    # 存在文件中
                    with open('1.text', 'a', encoding='utf8')as f:
                        f.write(href.strip() + '\n')

    def startone(self):
        '''入口'''
        try:

            for i in range(1, 10):
                print('第%s页>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>' % i)
                url = f'https://www.amazon.com/b/ref=gbps_ftr_m-9_475e_page_{i}?node=15529609011&pf_rd_r=96J4CJ1CECKQ3JZVTY1N&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:{i},sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:40&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&ie=UTF8'
                self.driver.get(url)
                self.driver.maximize_window()
                time.sleep(random.uniform(1, 1.5))
                self.page_spider()


        except Exception as e:
            pass
        finally:
            print('''完事.....''')
            self.driver.quit()
        return


if __name__ == '__main__':
    mclist = Matchlist()
    mclist.startone()
