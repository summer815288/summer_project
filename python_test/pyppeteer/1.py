import asyncio
from pyppeteer import launch

''''
async 声明一个异步操作。
await 声明一个耗时操作。
asyncio.get_event_loop().run_until_complete(main()) 创建异步池并执行main函数。
browser = await launch() 创建浏览器对象，可以传入 字典形式参数
page = await browser.newPage() 创建一个页面对象， 页面操作在该对象上执行
await page.goto('http://example.com') 页面跳转
await page.screenshot({'path': 'example.png'}) 截图保存
await browser.close() 关闭浏览器对象
evaluate()方法执行下面代码都能临时修改浏览器属性中的webdriver属性
'''


async def main():
    browser = await launch({
        # 'timeout': 50000,
        # 'headless': False,
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
            # "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
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
    # 设置浏览器宽高
    await page.setViewport(viewport={'width': 1400, 'height': 900})
    await page.setUserAgent(
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36')
    await page.setJavaScriptEnabled(enabled=True)
    # 以下为插入中间js，将淘宝会为了检测浏览器而调用的js修改其结果。
    await page.evaluate('''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await page.evaluate('''() =>{ window.navigator.chrome = { runtime: {},  }; }''')
    # 设置浏览器语言
    await page.evaluate(
        '''() =>{ Object.defineProperty(navigator, 'languages', { get: () => ['zh-CN', 'zh', 'en-US', 'en'] }); }''')
    # 设置插件
    await page.evaluate(
        '''() =>{ Object.defineProperty(navigator, 'plugins', { get: () => [1, 2, 3, 4, 5,6], }); }''')

    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})
    await browser.close()


asyncio.get_event_loop().run_until_complete(main())
