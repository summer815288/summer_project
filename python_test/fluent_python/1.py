# import collections
# from random import choice
#
# # Python 2.6开始，namedtuple 就加入到 Python 里，用以构建只有少数属性但是没有方法的对象
# Card = collections.namedtuple('Card', ['rank', 'suit'])
#
#
# class FrenchDeck:
#     ranks = [str(n) for n in range(2, 11)] + list('JQKA')
#     suits = 'spades diamonds clubs hearts'.split()
#
#     def __init__(self):
#         self._cards = [
#             Card(rank, suit) for suit in self.suits
#             for rank in self.ranks
#         ]
#
#     def __len__(self):
#         return len(self._cards)
#
#     def __getitem__(self, position):
#         return self._cards[position]
#
#
# beer_card = Card('7', 'diamonds')
# print(beer_card)
# deck = FrenchDeck()
# print(len(deck))
# print(deck[0])
# # 随机抽取
# print(choice(deck))
# # 抽出3张
# deck[:3]
# # 先抽出索引是 12 的那张牌，然后每隔 13 张牌拿 1 张
# deck[12::13]
# # 迭代
# for card in deck:
#     print(card)
# # 反向迭代
# for card in reversed(deck):
#     print(card)
#
# # 排序
# suit_values = dict(spades=3, hearts=2, diamonds=1, clubs=0)
#
#
# def spades_high(card):
#     rank_value = FrenchDeck.ranks.index(card.rank)
#     return rank_value * len(suit_values) + suit_values[card.suit]
#
#
# for card in sorted(deck, key=spades_high):  # doctest: +ELLIPSIS
#     print('11')
#     print(card)
#
# l = list(range(10))
# l[2:5] = [20, 30]
# print(l)
# t = (1, 2, [30, 40])
# t[2] += [50, 60]
# print(t)

# # 在有序序列中用 bisect 查找某个元素的插入位置
# import bisect
# import sys
#
# HAYSTACK = [1, 4, 5, 6, 8, 12, 15, 20, 21, 23, 23, 26, 29, 30]
# NEEDLES = [0, 1, 2, 5, 8, 10, 22, 23, 29, 30, 31]
# ROW_FMT = '{0:2d} @ {1:2d} {2}{0:<2d}'
#
#
# def demo(bisect_fn):
#     for needle in reversed(NEEDLES):
#         # 在 haystack（干草垛）里搜索 needle（针）的位置，该位置满足的条件是，把 needle 插入这个位置之后，haystack 还能保持升序。
#         position = bisect_fn(HAYSTACK, needle)
#         offset = position * ' |'
#         print(ROW_FMT.format(needle, position, offset))
#
#
# if __name__ == '__main__':
#     if sys.argv[-1] == 'left':
#         bisect_fn = bisect.bisect_left
#     else:
#         bisect_fn = bisect.bisect
#     print('DEMO:', bisect_fn.__name__)
#     print('haystack ->', ' '.join('%2d' % n for n in HAYSTACK))
#     demo(bisect_fn)

# DIAL_CODES = [
#     (86, 'China'),
#     (91, 'India'),
#     (1, 'United States'),
#     (62, 'Indonesia'),
#     (55, 'Brazil'),
#     (92, 'Pakistan'),
#     (880, 'Bangladesh'),
#     (234, 'Nigeria'),
#     (7, 'Russia'),
#     (81, 'Japan'),
# ]
# # 循环DIAL_CODES得到值 code, country，然后组合成：键是country，值为code
# country_code = {country: code for code, country in DIAL_CODES}
# print(country_code)


# def factorial(n):
#     '''returns n!'''
#     return 1 if n < 2 else n * factorial(n - 1)
# print(factorial(1))
# # __doc__ 是函数对象众多属性中的一个
# print(factorial.__doc__)
# # factorial 是 function 类的实例
# print(type(factorial))
# # 通过别的名称使用函数，再把函数作为参数传递
# list_data = list(map(factorial, range(11)))
# print(range(11))
# print(list_data)

# tag 函数用于生成 HTML 标签；使用名为 cls 的关键字参数传入“class”属性，这是一种变通方法，因为“class”是 Python 的关键字
# def tag(name, *content, cls=None, **attrs):
#     """生成一个或多个HTML标签"""
#     if cls is not None:
#         attrs['class'] = cls
#     if attrs:
#         attr_str = ''.join(' %s="%s"' % (attr, value)
#                            for attr, value
#                            in sorted(attrs.items()))
#     else:
#         attr_str = ''
#     if content:
#         return '\n'.join('<%s%s>%s</%s>' %
#                          (name, attr_str, c, name) for c in content)
#     else:
#         return '<%s%s />' % (name, attr_str)


# # 把 tag 函数（见示例 5-10）的签名绑定到一个参数字典上
# import inspect
#
# sig = inspect.signature(tag)
# my_tag = {
#     'name': 'img',
#     'title': 'Sunset Boulevard',
#     'src': 'sunset.jpg',
#     'cls': 'framed'
# }
# bound_args = sig.bind(**my_tag)
# print(bound_args)

# class HauntedBus:
#     """备受幽灵乘客折磨的校车"""
#
#     # 对象引用、可变性和垃圾回收 ｜ 191
#     def __init__(self, passengers=[]):  # ➊如果没传入 passengers 参数，使用默认绑定的列表对象，一开始是空列表。
#
#         '''
#          ➋这个赋值语句把 self.passengers 变成 passengers 的别名，而没有传入 passengers 参
# 数时，后者又是默认列表的别名。
#  self.passengers 上调用 .remove() 和 .append() 方法时，修改的其实是默认列表，
# 它是函数对象的一个属性。
#         '''
#         self.passengers = passengers
#
#         # ➌ self.passengers 上调用 .remove() 和 .append() 方法时，修改的其实是默认列表，
#
#     # 它是函数对象的一个属性。
#     def pick(self, name):
#         self.passengers.append(name)
#
#     def drop(self, name):
#         self.passengers.remove(name)
#
#
# bus1 = HauntedBus(['Alice', 'Bill'])
# print(bus1.passengers)
# print("\n")
# bus1.pick('Charlie')
# bus1.drop('Alice')
# print(bus1.passengers)
# print("\n")
# bus2 = HauntedBus()
# bus2.pick('Carrie')
# print(bus2.passengers)
# print("\n")
#
# bus3 = HauntedBus()
# print(bus3.passengers)
# print("\n")

# # 不要使用可变类型作为参数的默认值
# bus3.pick('Dave')
# print(bus2.passengers)
# print("\n")
# print(bus2.passengers is bus3.passengers)
# print("\n")
# print(bus1.passengers)
#
# print(dir(HauntedBus.__init__))
# print(HauntedBus.__init__.__defaults__)
# print(HauntedBus.__init__.__defaults__[0] is bus2.passengers)

# #有问题-del不删除对象，而是删除对象的引用
# import weakref
#
# s1 = {1, 2, 3}
# s2 = s1  # ➊s1 和 s2 是别名，指向同一个集合，{1, 2, 3}
#
#
# def bye():  # ➋这个函数一定不能是要销毁的对象的绑定方法，否则会有一个指向对象的引用。
#     print('Gone with the wind...')
#
#
# ender = weakref.finalize(s1, bye)  # ➌ s1 引用的对象上注册 bye 回调
# print(ender.alive)  # ➍ 调用 finalize 对象之前，.alive 属性的值为 True
#
# print(s1)
# print(s2)
# del s1  # ➎如前所述，del 不删除对象，而是删除对象的引用。
# print(ender.alive)
# # print(s1)
# print(s2)
# s2 = 'spam'  # ➏重新绑定最后一个引用 s2，让 {1, 2, 3} 无法获取。对象被销毁了，调用了 bye 回调，ender.alive 的值变成了 False。
# print(ender.alive)

from diamond import *