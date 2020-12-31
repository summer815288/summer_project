# -*- coding: utf-8 -*-
'''
来研究线程池的行为。
这个程序会创建一个包含 3 个职程的线程池，运行 5 个可调用的对象，输出带有时间戳的消息
'''

from time import sleep, strftime
from concurrent import futures


def display(*args):  # ➊这个函数的作用很简单，把传入的参数打印出来，并在前面加上 [HH:MM:SS] 格式的时间戳。
    print(strftime('[%H:%M:%S]'), end='')
    print(*args)


def loiter(n):  # ➋loiter 函数什么也没做，只是在开始时显示一个消息，然后休眠 n 秒，最后在结束时再显示一个消息；消息使用制表符缩进，缩进的量由 n 的值确定

    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    return n * 10  # ➌loiter 函数返回 n * 10，以便让我们了解收集结果的方式。


def main():
    display('Script starting.')
    executor = futures.ThreadPoolExecutor(max_workers=3)  # ➍创建 ThreadPoolExecutor 实例，有 3 个线程
    # ➎把五个任务提交给 executor（因为只有 3 个线程，所以只有 3 个任务会立即开始：loiter(0)、loiter(1) 和 loiter(2)）；这是非阻塞调用。
    results = executor.map(loiter, range(5))
    display('results:', results)  # ➏立即显示调用 executor.map 方法的结果：一个生成器
    display('Waiting for individual results:')
    '''
    ➐for 循环中的 enumerate 函数会隐式调用 next(results)，
    这个函数又会在（内部）表示第一个任务（loiter(0)）的 _f 期物上调用 _f.result() 方法。
    result 方法会阻塞，直到期物运行结束，因此这个循环每次迭代时都要等待下一个结果做好准备
    '''
    for i, result in enumerate(results):
        display('result {}: {}'.format(i, result))


main()
