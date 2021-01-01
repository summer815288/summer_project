'''
Tombola 是抽象基类，有两个抽象方法和两个具体方法
Tombola 抽象基类有四个方法，
其中两个是抽象方法。
• .load(...)：把元素放入容器。
• .pick()：从容器中随机拿出一个元素，返回选中的元素。
另外两个是具体方法。
• .loaded()：如果容器中至少有一个元素，返回 True。
• .inspect()：返回一个有序元组，由容器中的现有元素构成，不会修改容器的内容（内
部的顺序不保留）。
'''

import abc


class Tombola(abc.ABC):  # ➊ 自己定义的抽象基类要继承 abc.ABC
    @abc.abstractmethod
    def load(self, iterable):  # ➋ 抽象方法使用 @abstractmethod 装饰器标记，而且定义体中通常只有文档字符串。

        """从可迭代对象中添加元素。"""

    @abc.abstractmethod
    def pick(self):  # ➌ 根据文档字符串，如果没有元素可选，应该抛出 LookupError

        """随机删除元素，然后将其返回。
       如果实例为空，这个方法应该抛出`LookupError`。
        """

    def loaded(self):  # ➍ 抽象基类可以包含具体方法。

        """如果至少有一个元素，返回`True`，否则返回`False`。"""

        return bool(self.inspect())  # ➎ 抽象基类中的具体方法只能依赖抽象基类定义的接口（即只能使用抽象基类中的其他具体方法、抽象方法或特性）

    def inspect(self):
        """返回一个有序元组，由当前元素构成。"""
        items = []
        while True:  # ➏ 我们不知道具体子类如何存储元素，不过为了得到 inspect 的结果，我们可以不断调用 .pick() 方法，把 Tombola 清空……
            try:
                items.append(self.pick())
            except LookupError:
                break
        self.load(items)  # ➐ ……然后再使用 .load(...) 把所有元素放回去。
        return tuple(sorted(items))
