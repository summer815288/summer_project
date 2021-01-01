from collections import namedtuple

Result = namedtuple('Result', 'count average')


# 子生成器
def averager():  # ➊与示例 16-13 中的 averager 协程一样。这里作为子生成器使用
    total = 0.0
    count = 0
    average = None
    while True:
        term = yield  # ➋main 函数中的客户代码发送的各个值绑定到这里的 term 变量上
        if term is None:  # ➌至关重要的终止条件。如果不这么做，使用 yield from 调用这个协程的生成器会永远阻塞。
            break
    total += term
    count += 1
    average = total / count
    return Result(count, average)  # ➍返回的 Result 会成为 grouper 函数中 yield from 表达式的值


# 委派生成器
def grouper(results, key):  # ➎grouper 是委派生成器
    while True:  # ➏ 这个循环每次迭代时会新建一个 averager 实例；每个实例都是作为协程使用的生成器对象
        '''
        ➐
        grouper 发送的每个值都会经由 yield from 处 理， 通 过 管 道 传 给 averager 实 例。
        grouper 会在 yield from 表达式处暂停，等待 averager 实例处理客户端发来的值。
        averager 实例运行完毕后，返回的值绑定到 results[key] 上。while 循环会不断创建
        averager 实例，处理更多的值
        '''
        results[key] = yield from averager()

        # 客户端代码，即调用方


# 调用方
def main(data):
    results = {}
    for key, values in data.items():
        group = grouper(results,
                        key)  # group 是调用 grouper 函数得到的生成器对象，传给 grouper 函数的第一个参数是results，用于收集结果；第二个参数是某个键。group 作为协程使用
        next(group)  # 预激 group 协程
        for value in values:
            group.send(value)
        group.send(None)  # 重要！
    print(results)  # 如果要调试，去掉注释
    report(results)


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit))


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}
if __name__ == '__main__':
    main(data)

'''
外层for循环每次迭代会新建一个grouper实例，赋值给group变量；group是委派生成器。
• 调用 next(group)，预激委派生成器 grouper，此时进入 while True 循环，调用子生成
器 averager 后，在 yield from 表达式处暂停。
• 内层 for 循环调用 group.send(value)，直接把值传给子生成器 averager。同时，当前
的 grouper 实例（group）在 yield from 表达式处暂停。
• 内层循环结束后，group 实例依旧在 yield from 表达式处暂停，因此，grouper 函数定
义体中为 results[key] 赋值的语句还没有执行。
• 如果外层 for 循环的末尾没有 group.send(None)，那么 averager 子生成器永远不会终止，
委派生成器 group 永远不会再次激活，因此永远不会为 results[key] 赋值。
• 外层 for 循环重新迭代时会新建一个 grouper 实例，然后绑定到 group 变量上。前一个
grouper 实例（以及它创建的尚未终止的 averager 子生成器实例）被垃圾回收程序回收。

这个试验想表明的关键一点是，如果子生成器不终止，委派生成器会在 yield 
from 表达式处永远暂停。如果是这样，程序不会向前执行，因为 yield from
（与 yield 一样）把控制权转交给客户代码（即，委派生成器的调用方）了。
显然，肯定有任务无法完成。
'''
