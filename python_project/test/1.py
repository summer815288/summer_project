# import requests
# from pyquery import PyQuery as pq
#
# url = 'http://quotes.toscrape.com/js/'
# response = requests.get(url)
# doc = pq(response.text)
# print('Quotes:', doc('.quote').length)

# Pyppeteer 整个流程就完成了浏览器的开启、新建页面、页面加载等操作。
# 另外 Pyppeteer 里面进行了异步操作，所以需要配合 async/await 关键词来实现。
import asyncio
from pyppeteer import launch
from pyquery import PyQuery as pq

# 例子一：抓取http://quotes.toscrape.com/js/中的数据

# async def main():
#     # 首先， launch 方法会新建一个 Browser 对象，然后赋值给 browser
#     browser = await launch()
#     # 然后调用 newPage 方法相当于浏览器中新建了一个选项卡，同时新建了一个 Page对象
#     page = await browser.newPage()
#     # 然后 Page 对象调用了 goto 方法就相当于在浏览器中输入了这个URL，
#     await page.goto('http://quotes.toscrape.com/js/')
#     # 浏览器跳转到了对应的页面进行加载，加载完成之后再调用 content 方法，返回当前浏览器页面的源代码,
#     # 然后进一步地，我们用pyquery进行同样地解析，就可以得到JavaScript渲染的结果了。
#     doc = pq(await page.content())
#     print('Quotes:', doc('.quote').length)
#     await browser.close()
#
#
# asyncio.get_event_loop().run_until_complete(main())


# 例子二：完成了网页截图保存、网页导出 PDF 保存、执行 JavaScript 并返回对应数据
# import asyncio
# from pyppeteer import launch
#
#
# async def main():
#     browser = await launch()
#     page = await browser.newPage()
#     await page.goto('http://quotes.toscrape.com/js/')
#     # 首先 screenshot 方法可以传入保存的图片路径，另外还可以指定保存格式 type、清晰度 quality、是否全屏 fullPage、裁切 clip 等各个参数实现截图。
#     await page.screenshot(path='example.png')
#     # 保存为pdf
#     await page.pdf(path='example.pdf')
#     # 最后我们又调用了 evaluate 方法执行了一些 JavaScript，JavaScript 传入的是一个函数，使用 return 方法返回了网页的宽高、像素大小比率三个值，最后得到的是一个 JSON 格式的对象
#     dimensions = await page.evaluate('''() => {
#         return {
#             width: document.documentElement.clientWidth,
#             height: document.documentElement.clientHeight,
#             deviceScaleFactor: window.devicePixelRatio,
#         }
#     }''')
#
#     print(dimensions)
#     # >>> {'width': 800, 'height': 600, 'deviceScaleFactor': 1}
#     await browser.close()
#
#
# asyncio.get_event_loop().run_until_complete(main())


# 例子三：
import asyncio
from pyppeteer import launch

width, height = 1366, 768


async def main():
    # browser = await launch(headless=False)
    # 就是在 launch 方法中，args 参数通过 list 形式传入即可，这里使用的是 --disable-infobars 的参数。
    browser = await launch(devtools=False,
                           headless=False,
                           userDataDir='./userdata',
                           args=[f'--window-size={width},{height}'])
    page = await browser.newPage()
    await page.setViewport({'width': width, 'height': height})
    await page.goto('https://www.taobao.com')

    await page.evaluate(
        '''() =>{ Object.defineProperties(navigator,{ webdriver:{ get: () => false } }) }''')
    await asyncio.sleep(100)


asyncio.get_event_loop().run_until_complete(main())
