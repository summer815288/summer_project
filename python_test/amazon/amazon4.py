import requests

url = 'https://www.amazon.com/NanoSteamer-3-Humidifier-Blackheads-Stainless/dp/B01BPKUCRE'

head = {
    'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
r = requests.get(url, headers=head)

content = r.content

print(content)
