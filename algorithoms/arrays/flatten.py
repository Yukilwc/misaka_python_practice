"""
Implement Flatten Arrays.
Given an array that may contain nested arrays,
produce a single resultant array.
"""

# 返回iterator
def flatten_iter(list):
    for i in list:
        

res = flatten_iter([[1,2,3],[[8,9,[10]],[6,7,[]],3],[1,2,[4,5]]])
print(' flatten_iter',res)