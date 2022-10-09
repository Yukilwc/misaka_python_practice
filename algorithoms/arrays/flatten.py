"""
Implement Flatten Arrays.
Given an array that may contain nested arrays,
produce a single resultant array.
"""

# 返回iterator
from collections.abc import Iterable


def flatten_iter(iterable):
    for element in iterable:
        if not isinstance(element,str) and isinstance(element,Iterable):
            yield from flatten_iter(element)
        else:
            yield element

res = flatten_iter([[1,2,3],[[8,9,[10]],[6,7,[]],3],8,[1,2,[4,5]]])
for i in res:
    print('i',i)