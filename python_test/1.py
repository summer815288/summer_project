import socket
import urllib.request
import urllib.error

# try:
#     response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
# except urllib.error.URLError as e:
#     if isinstance(e.reason, socket.timeout):
#         print('TIME OUT')

# request = urllib.request.Request('https://python.org')
# response = urllib.request.urlopen(request)
# print(response.read().decode('utf-8'))


# 看一下 Request 可以通过怎样的参数来构造，
# 通过 个参数构造了一个请求，其中 url 即请求 URL, headers 中指定了 User-Agent Host ，参数 data urlencode （）和 bytes （）方法转成字节流 另外，指定了请求方式为 POST
# from urllib import request, parse
#
# url = 'http://httpbin.org/post'
# headers = {
#     'User-Agent': 'Mozilla/4.0(compatible;MSIE 5.5;Windows NT)',
#     'Host': 'httpbin.org'
# }
# dict = {
#     'name': 'Germey'
# }
# data = bytes(parse.urlencode(dict), encoding='utf8')
# req = request.Request(url=url, data=data, headers=headers, method='POST')
# response = request.urlopen(req)
# print(response.read().decode('utf-8'))

# 验证
# from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
# from urllib.error import URLError
#
# username = 'username'
# password = 'password'
# url = 'http: //localhost:5000/'
#
# p = HTTPPasswordMgrWithDefaultRealm()
# p.add_password(None, url, username, password)
# auth_handler = HTTPBasicAuthHandler(p)
# opener = build_opener(auth_handler)
#
# try:
#     result = opener.open(url)
#     html = result.read().decode('utf-8')
#     print(html)
# except URLError as e:
#     print(e.reason)

# 获取cookie
# import http.cookiejar, urllib.request
#
# cookie = http.cookiejar.CookieJar()
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# for item in cookie:
#     print(item.name + "=" + item.value)

# 将cookie写入文件
import http.cookiejar, urllib.request

# filename = 'cookies.txt'
# # cookie = http.cookiejar.MozillaCookieJar(filename)
# cookie = http.cookiejar.LWPCookieJar(filename)  # 保存成libwww-perl(lwp)格式的cookie文件
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# cookie.save(ignore_discard=True, ignore_expires=True)

# 将cookie文件读取并利用
# cookie = http.cookiejar.LWPCookieJar()
# cookie.load('cookies.txt', ignore_discard=True, ignore_expires=True)
# handler = urllib.request.HTTPCookieProcessor(cookie)
# opener = urllib.request.build_opener(handler)
# response = opener.open('http://www.baidu.com')
# print(response.read().decode('utf-8'))

# 将提取到的图片保存
# import requests
#
# r = requests.get('https://github.com/favicon.ic')
# with open('favicon.ico', 'wb') as f:
#     f.write(r.content)

# 抓取分析
# import requests,re
#
#
# def get_one_page(url):
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3100.0 Safari/537.36'
#     }
#     response = requests.get(url, headers=headers)
#     print(response.status_code)
#     if response.status_code == 200:
#         return response.text
#     return None

# name = input('please input name:')
# print("hell," + name + "!")
try_count = {}
url = "https://www.amazon.com/b/ref=gbps_ftr_m-9_475e_page_1?node=15529609011&pf_rd_r=3MHRMPRZP2TCRX7J9K8S&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:1,sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:48&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&ie=UTF8"
try_count[url] = 3
if url in try_count and try_count[url] > 3:
    print(1)
else:
    if url in try_count:
        try_count[url] += 1
    else:
        try_count[url] = 1

print(try_count)
