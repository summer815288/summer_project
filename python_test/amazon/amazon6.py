import asyncio
import time
from pyppeteer import launch


async def main():
    browser = await launch({
        # 'timeout': 50000,
        'headless': False,
        # 是否为每个选项卡自动打开DevTools面板。如果是此选项True，headless则将设置该选项 False
        # "devtools": False,
        # 忽略证书错误
        'ignoreHTTPSErrors': True,
        # dumpio的作用：把无头浏览器进程的 sztderr 核 stdout pip 到主程序，也就是设置为 True 的话，chromium console 的输出就会在主程序中被打印出来
        'dumpio': True,  # 是否将浏览器进程stdout和stderr传递到process.stdout和中process.stderr,默认为False, 防止浏览器卡主
        # 脚本完成后自动关闭浏览器进程, 默认为True
        # "autoClose": False,
        # 用户数据保存目录 这个最好也自己指定一个目录 如果不指定的话，chrome会自动新建一个临时目录使用，在浏览器退出的时候会自动删除临时目录 在删除的时候可能会删除失败（不知道为什么会出现权限问题，我用的windows） 导致浏览器退出失败 然后chrome进程就会一直没有退出 CPU就会狂飙到99%
        # 注意：同一个用户目录（userDataDir）不能被两个chrome进程使用，如果你要多开，记得分别指定用户目录。否则会报编码错误
        # "userDataDir": "./user_data_dir",
        'args': [
            # 禁用GPU硬件加速
            "--disable-gpu",
            # 不要执行同源策略
            "--disable-web-security",
            # 关闭 XSS Auditor
            "--disable-xss-auditor",
            # 允许不安全内容，比如https中包含http的链接
            "--allow-running-insecure-content",
            # 禁用信息栏 比如 chrome正在受到自动测试软件的控制 ...
            '--disable-infobars',  # 不显示信息栏
            # '--window-size=1920,1080',
            # f'--window-size={width},{height}',
            # 沙盒
            '--no-sandbox', '--disable-setuid-sandbox',
            # log等级设置 在某些不是那么完整的系统里 如果使用默认的日志等级 可能会出现一大堆的warning信息
            '--log-level=3',
            # 窗口最大号
            # '--start-maximized',
            # 设置浏览器代理
            # "--proxy-server=socks5://127.0.0.1:10808",
            # 设置ua
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
            # 禁用webgl
            "--disable-webgl",
            # 禁用扩展
            '--disable-extensions',
            # 隐藏滚动条
            '--hide-scrollbars',
            # 禁用flash
            '--disable-bundled-ppapi-flash',
            # 设备静音
            '--mute-audio',
            '--disable-blink-features=AutomationControlled',
        ]
    })
    page = await browser.newPage()
    # await page.goto('https://www.amazon.com/b/ref=gbps_ftr_m-9_475e_page_1?node=15529609011&pf_rd_r=3MHRMPRZP2TCRX7J9K8S&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:1,sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:48&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&ie=UTF8')
    # await page.goto(
    #     'https://www.amazon.com/b/ref=gbps_ftr_m-9_475e_page_2?node=15529609011&pf_rd_r=9XVDBNK9ZVGATJ36CYK7&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,page:2,sortOrder:BY_SCORE,MARKETING_ID:ship_export,dealsPerPage:48&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&ie=UTF8'
    # )
    await page.goto(
        'https://www.amazon.com/b/ref=gbps_ftr_m-9_475e_page_1?node=15529609011&pf_rd_r=96J4CJ1CECKQ3JZVTY1N&pf_rd_p=5d86def2-ec10-4364-9008-8fbccf30475e&gb_f_deals1=dealStates:AVAILABLE%252CWAITLIST%252CWAITLISTFULL%252CEXPIRED%252CSOLDOUT%252CUPCOMING,sortOrder:BY_SCORE,MARKETING_ID:ship_export&pf_rd_s=merchandised-search-9&pf_rd_t=101&pf_rd_i=15529609011&pf_rd_m=ATVPDKIKX0DER&ie=UTF8'
    )

    time.sleep(10)
    print(await page.content())
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
