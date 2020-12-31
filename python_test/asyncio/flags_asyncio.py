'''
下载国旗的 flags_asyncio.py 脚本的完整代码
(1) 首先，在 download_many 函数中获取一个事件循环，处理调用 download_one 函数生成的几个协程对象。
(2) asyncio 事件循环依次激活各个协程。
(3) 客户代码中的协程（如 get_flag）使用 yield from 把职责委托给库里的协程（如aiohttp.request）时，控制权交还事件循环，执行之前排定的协程。
(4) 事件循环通过基于回调的低层 API，在阻塞的操作执行完毕后获得通知。
(5) 获得通知后，主循环把结果发给暂停的协程。
(6) 协程向前执行到下一个 yield from 表达式，例如 get_flag 函数中的 yield from resp.read()。事件循环再次得到控制权，重复第 4~6 步，直到事件循环终止。



asyncio中，基本的流程是一样的：
在一个单线程程序中使用主循环依次激活队列里的协程。各个协程向前执行几步，然后把控制权让给主循环，主循环再激活队列里的下一个协程。
'''
import asyncio
import aiohttp #必须安装 aiohttp 包，它不在标准库中。
from flags import BASE_URL, save_flag, show, main ➋
@asyncio.coroutine ➌
def get_flag(cc):
     url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
     resp = yield from aiohttp.request('GET', url) ➍
     image = yield from resp.read() ➎
    return image
@asyncio.coroutine
def download_one(cc): ➏
     image = yield from get_flag(cc) ➐
     show(cc)
     save_flag(image, cc.lower() + '.gif')
     return cc
def download_many(cc_list):
     loop = asyncio.get_event_loop() ➑
     to_do = [download_one(cc) for cc in sorted(cc_list)] ➒
     wait_coro = asyncio.wait(to_do) ➓
     res, _ = loop.run_until_complete(wait_coro)
     loop.close()
     return len(res)


if __name__ == '__main__':
    main(download_many)