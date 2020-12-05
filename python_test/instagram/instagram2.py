# 通过请求第一页的接口得到用户信息+第一页的视频信息

from bs4 import BeautifulSoup
import json, random, re, requests, math

FILE_NAME = 'instagram_cookie.txt'
session = requests.Session()

with open(FILE_NAME) as f:
    # readline()每一次读取一行数据，并指向该行末尾
    cookies = f.readline().rstrip()  # 读取第一行数据（此时已经指向第一行末尾）
    if cookies == '':
        print(1111)
        cookies = json.loads(cookies)
        # 将字典转为CookieJar：
        cookies = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
        session.cookies = cookies
    else:
        print(2222)
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

    DETAIL_URL = 'https://www.instagram.com/9gag/?__a=1'
    info = session.get(DETAIL_URL)
    print(info.content)
    exit()
    influencer_info = json.loads(str(info.content, 'utf-8'))
    # 得到用户信息
    user_info = influencer_info['graphql']['user']
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
    print('用户信息:' + json.dumps(user_list))
    print(3333)
    # 得到帖子信息-构造分页取得所有视频信息
    video_info = user_info['edge_owner_to_timeline_media']
    page_info = video_info['page_info']
    has_next_page = page_info['has_next_page']
    end_cursor = page_info['end_cursor']
    count = video_info['count']
    first = 50
    query_hash = "56a7068fea504063273cc2120ffd54f3"
    retry = 0
    # 进行分页构造参数
    page_total = math.ceil(count / first)
    print('视频总页数:' + str(count) + '；总页数：' + str(page_total))
    print(4444)
    page = 0
    if page_total > 0:
        while page < page_total:
            video_list = []
            page = page + 1
            print('第' + str(page) + '页')
            if end_cursor:
                variables = {
                    "id": user_info['id'],
                    "first": first,
                    "after": end_cursor
                }

                NEXT_URL = 'https://www.instagram.com/graphql/query/?query_hash=' + query_hash + '&variables=' + json.dumps(
                    variables)
                video_response = session.get(NEXT_URL)
                try:
                    if video_response.content:
                        video_response = json.loads(str(video_response.content, 'utf-8'))
                        edge_owner_to_timeline_media = ''
                        edges = ''
                        if 'data' in video_response:
                            if 'user' in video_response['data']:
                                if 'edge_owner_to_timeline_media' in video_response['data']['user']:
                                    edge_owner_to_timeline_media = video_response['data']['user'][
                                        'edge_owner_to_timeline_media']
                                else:
                                    print(9999)
                                    print(video_response)
                                    print('edge_owner_to_timeline_media not in video_response')
                            else:
                                print(9999)
                                print(video_response)
                                print('user not in video_response')
                        else:
                            print(9999)
                            print(video_response)
                            print('data not in video_response')

                        if edge_owner_to_timeline_media and ('page_info' in edge_owner_to_timeline_media):
                            if 'end_cursor' in edge_owner_to_timeline_media['page_info']:
                                end_cursor = edge_owner_to_timeline_media['page_info']['end_cursor']
                            else:
                                print(9999)
                                print(video_response)
                                print('end_cursor not in video_response')
                        else:
                            print(9999)
                            print(video_response)
                            print('page_info not in video_response')

                        if edge_owner_to_timeline_media and ('edges' in edge_owner_to_timeline_media):
                            edges = edge_owner_to_timeline_media['edges']
                        else:
                            print(9999)
                            print(video_response)
                            print('edges not in video_response')

                        if edges:
                            for nodes in edges:
                                node = nodes['node']
                                video_url = ''
                                video_view_count = ''
                                edge_media_to_caption_text = ''
                                if 'video_url' in node:
                                    video_url = node['video_url']
                                if 'video_view_count' in node:
                                    video_view_count = node['video_view_count']
                                if 'product_type' in node:
                                    product_type = node['product_type']
                                if 'node' in node:
                                    edge_media_to_caption_text = node['edge_media_to_caption']['edges'][0]
                                    if 'text' in edge_media_to_caption_text['node']:
                                        edge_media_to_caption_text = edge_media_to_caption_text['node']['text']

                                video_list.append({
                                    'end_cursor': end_cursor,
                                    'display_url': node['display_url'],
                                    'is_video': node['is_video'],
                                    'video_url': video_url,
                                    'video_view_count': video_view_count,
                                    'edge_media_to_caption_text': edge_media_to_caption_text,
                                    'edge_media_to_comment': node['edge_media_to_comment']['count'],
                                    'edge_media_preview_like': node['edge_media_preview_like']['count'],
                                    'thumbnail_src': node['thumbnail_src'],
                                    'product_type': product_type,
                                })
                                with open('../video_list.txt', 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
                                    f.write(json.dumps(video_list, indent=1))
                    else:
                        print(9999)
                        print(video_response)
                        print('video_response.content is null')
                except IOError as e:
                    print(8888)
                    print(e)
                except ValueError as e:
                    print(e)
# query_hash
# a7068fea504063273cc2120ffd54f3
# d4d88dc1500312af6f937f7b804c68c3
