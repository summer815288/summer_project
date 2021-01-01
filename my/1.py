from numpy.random import randn
import numpy as np

np.random.seed(123)
import os
import matplotlib.pyplot as plt
import pandas as pd

plt.rc('figure', figsize=(10, 6))
np.set_printoptions(precision=4)
pd.options.display.max_rows = 20

import json

path = 'datasets/bitly_usagov/example.txt'
records = [json.loads(line) for line in open(path)]
time_zones = [rec['tz'] for rec in records if 'tz' in rec]


# 第一种计算
def get_counts(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


# 第二种计算
from collections import defaultdict


def get_counts2(sequence):
    counts = defaultdict(int)  # values will initialize to 0
    for x in sequence:
        counts[x] += 1
    return counts


# 得到前十位的市区及其计算方式
def top_counts(count_dict, n=10):
    value_key_pairs = [(count, tz) for tz, count in count_dict.items()]
    value_key_pairs.sort()
    return value_key_pairs[-n:]


counts = get_counts(time_zones)
print(counts)
print(len(time_zones))

print(counts)
print('....d>>>>>>>>>>>>')
print(top_counts(counts))


import os
from collections import Counter
counts = Counter(time_zones)
print('sdasdada>>>>>>')
print(counts)
print(counts.most_common(10))
