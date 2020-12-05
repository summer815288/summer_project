import requests, json
from lxml import etree


class User():
    def a_request(url):
        head = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
        }
        r = requests.get(url, headers=head)
        content = r.content
        html = etree.HTML(content)
        print(type(content))
        # 得到所有的商品详情页
        body = html.xpath('.//ul/li//div[@class="a-row a-spacing-small"]//a/@href')
        print(body)
        # 得到下一页的URL
        # next_page = html.xpath('.//a[@id="pagnNextLink"]/@href')[0]
        # next_page = 'https://www.amazon.com/-/zh' + next_page
        # requests.get(next_page, headers=head)


url = 'https://www.amazon.com/b?node=17938598011&pd_rd_w=Yrim9&pf_rd_p=330217e1-d8b5-420c-90c6-f934ed719224&pf_rd_r=K4HHRX34QWH9BPHY4341&pd_rd_r=84831b77-c20e-4ef6-874f-e13acc6e641f&pd_rd_wg=YuYNi'

a = User()
a.a_request(url)
