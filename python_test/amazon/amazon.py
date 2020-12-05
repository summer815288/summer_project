import requests
import json

# FILE_NAME = 'amazon_cookie.txt'
# url = 'https://www.amazon.com/b/ref=AIS_GW_deals?node=15529609011&pf_rd_r=K4HHRX34QWH9BPHY4341&pf_rd_p=9eb86184-7f77-4a13-b12a-ea49571a635d'
#
# head = {
#     'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# }

# with open(FILE_NAME) as f:
#     # readline()每一次读取一行数据，并指向该行末尾
#     cookies = f.readline().rstrip()  # 读取第一行数据（此时已经指向第一行末尾）
#     if cookies != '':
#         print(1111)
#         cookies = json.loads(cookies)
#     else:
#         r = requests.get(url, headers=head)
#         cookies = requests.utils.dict_from_cookiejar(r.cookies)
#         with open(FILE_NAME, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
#             f.write(json.dumps(cookies))
#
import requests, json, re, time
from lxml import etree
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


def get_one_page(url, a, current_page):
    print(111)
    print('第' + str(current_page) + '页')
    head = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    try:
        r = requests.get(url, headers=head)
        content = r.content
        # html = etree.HTML(content)
        # body = html.xpath('.//div[@id="widgetContent"]//a[@id="dealImage"]/@href')
        # print(content)
        # exit()
        soup = BeautifulSoup(content, 'lxml')
        scripts = soup.find_all('script', type="text/javascript", text=re.compile('var dcsServerResponse = '))
        scripts = scripts[0].get_text()
        str_begin = scripts.find('var dcsServerResponse = ')
        str_end = scripts.find('widgetToRegister.dcsServerResponse')
        end_str = scripts[str_begin:str_end]
        end_str = (end_str.replace('var dcsServerResponse = ', '')).strip()[:-1]
        json_info = json.loads(end_str)
        selectedDealsCount = json_info['selectedDealsCount']
        sortedDealIDs = json_info['sortedDealIDs']
        # dealDetails = json_info['dealDetails']
        # if json_info and json_info['dealDetails']:
        #     with open('detail.json', 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        #         f.write(json.dumps(dealDetails))
        if sortedDealIDs:
            a = set(a).union(set(sortedDealIDs))
            with open('ids.json', 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                f.write(json.dumps(list(a)))

        if current_page <= 21:
            print(2222)
            next_url = 'https://www.amazon.com/b/ref=gbps_ftr_m-9_475e_page_' + str(
                current_page) + '?node=15529609011&pf_rd_r=HRG890RDX86TEM0G13NA&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:' + str(
                current_page) + ',sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:32&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&ie=UTF8#next'
            if next_url:
                current_page += 1
                time.sleep(15)
                get_one_page(next_url, a, current_page)
    except ZeroDivisionError:
        print("You can't divide by zero!")
    except RequestException:
        print("RequestException")
    except IOError:
        print("IOError")


url = 'https://www.amazon.com/b/ref=AIS_GW_deals?node=15529609011&pf_rd_r=K4HHRX34QWH9BPHY4341&pf_rd_p=9eb86184-7f77-4a13-b12a-ea49571a635d'

get_one_page(url, {}, 1)
