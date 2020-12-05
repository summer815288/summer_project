# 通过得到html页面

from bs4 import BeautifulSoup
import json, random, re, requests
from bs4 import BeautifulSoup

FILE_NAME = 'instagram_cookie.txt'
session = requests.Session()

with open(FILE_NAME) as f:
    # readline()每一次读取一行数据，并指向该行末尾
    cookies = f.readline().rstrip()  # 读取第一行数据（此时已经指向第一行末尾）
    if cookies:
        print(1111)
        cookies = json.loads(cookies)
        # 将字典转为CookieJar：
        cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
        session.cookies = cookies
    else:
        print(2222)
        exit()
        BASE_URL = 'https://www.instagram.com/accounts/login/'
        LOGIN_URL = BASE_URL + 'ajax/'
        headers_list = [
            "Mozilla/5.0 (Windows NT 5.1; rv:41.0) Gecko/20100101" \
            " Firefox/41.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2)" \
            " AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2" \
            " Safari/601.3.9",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0)" \
            " Gecko/20100101 Firefox/15.0.1",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
            " (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36" \
            " Edge/12.246"
        ]

        USERNAME = 'summerzhaos'
        PASSWD = "#PWD_INSTAGRAM_BROWSER:10:1603249892:ARJQAPgGG9MLWyCLJiSQgY2awswO0w8XdGHaF9ZjpqBDTdtQ+b3s+7T8w7d63KL/418aepVuZZhxXEZVxHSqm0gKzNIEr239kp5m2xihGXEpkvVN99OAOa20IGicB9g3usckzxjSz9e12JKt"
        USER_AGENT = headers_list[random.randrange(0, 4)]

        session.headers = {'user-agent': USER_AGENT}
        session.headers.update({'Referer': BASE_URL})
        # 先请求一次得到csrf_token，再请求一次登录成功
        req = session.get(BASE_URL)
        soup = BeautifulSoup(req.content, 'html.parser')
        body = soup.find('body')

        pattern = re.compile('window._sharedData')
        script = body.find("script", text=pattern)

        script = script.get_text().replace('window._sharedData = ', '')[:-1]
        data = json.loads(script)

        csrf = data['config'].get('csrf_token')
        login_data = {'username': USERNAME, 'enc_password': PASSWD}
        session.headers.update({'X-CSRFToken': csrf})
        login = session.post(LOGIN_URL, data=login_data, allow_redirects=True, verify=False)
        # b'{"user": true, "userId": "43999366107", "authenticated": true, "oneTapPrompt": true, "status": "ok"}'

        cookies = requests.utils.dict_from_cookiejar(login.cookies)
        with open(FILE_NAME, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
            f.write(json.dumps(cookies))

DETAIL_URL = 'https://www.instagram.com/9gag'
info = session.get(DETAIL_URL)
soup = BeautifulSoup(info.content)
scripts = soup.find_all('script', type="text/javascript", text=re.compile('window._sharedData'))
stringified_json = scripts[0].get_text().replace('window._sharedData = ', '')[:-1]
influencer_info = json.loads(stringified_json)
# 得到用户信息
user_info = influencer_info['entry_data']['ProfilePage'][0]['graphql']['user']
user_list = {
    'biography': user_info['biography'],
    'business_email': user_info['business_email'],
    'external_url_linkshimmed': user_info['external_url_linkshimmed'],
    'edge_followed_by': user_info['edge_followed_by']['count'],
    'edge_follow': user_info['edge_follow']['count'],
    'full_name': user_info['full_name'],
    'highlight_reel_count': user_info['highlight_reel_count'],
    'id': user_info['id'],
    'business_category_name': user_info['business_category_name'],
    'edge_mutual_followed_by': user_info['edge_mutual_followed_by']['count'],
    'username': user_info['username'],
    'profile_pic_url': user_info['profile_pic_url'],
}
print(user_list)
print(3333)
# 得到帖子信息
video_info = user_info['edge_owner_to_timeline_media']
page_info = video_info['page_info']
count = video_info['count']
edges = video_info['edges']
video_list = []
for nodes in edges:
    node = nodes['node']
    video_list.append({
        'display_url': node['display_url'],
        'is_video': node['is_video'],
        'accessibility_caption': node['accessibility_caption'],
        'edge_media_to_comment': node['edge_media_to_comment']['count'],
        'edge_liked_by': node['edge_liked_by']['count'],
        'edge_media_preview_like': node['edge_media_preview_like']['count'],
        'thumbnail_src': node['thumbnail_src'],
    })
    print(video_list)
    exit()
