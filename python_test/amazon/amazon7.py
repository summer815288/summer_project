import requests
import json

FILE_NAME = 'amazon_cookie.txt'
url = 'https://www.amazon.com/b/ref=AIS_GW_deals?node=15529609011&pf_rd_r=K4HHRX34QWH9BPHY4341&pf_rd_p=9eb86184-7f77-4a13-b12a-ea49571a635d'

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
# 得到cookie
with open(FILE_NAME) as f:
    # readline()每一次读取一行数据，并指向该行末尾
    cookies = f.readline().rstrip()  # 读取第一行数据（此时已经指向第一行末尾）
    if cookies != '':
        print(1111)
        cookies = json.loads(cookies)
    else:
        r = requests.get(url, headers=head)
        cookies = requests.utils.dict_from_cookiejar(r.cookies)
        with open(FILE_NAME, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            f.write(json.dumps(cookies))

with open('ids.json') as f:
    ids = f.readline().rstrip()  # 读取第一行数据（此时已经指向第一行末尾）
    ids = json.loads(ids)
