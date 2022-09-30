"""
Given a list lst and a number N, create a new list
that contains each number of the list at most N times without reordering.
For example if N = 2, and the input is [1,2,3,1,2,1,2,3], you take [1,2,3,1,2], 
drop the next [1,2] since this would lead to 1 and 2 being in the result 3 times, and then take 3, 
which leads to [1,2,3,1,2,3]
"""

import collections


success_res = [1,2,3,1,2,3,4,4]

def delete_nth(list,num):
    result = []
    d = collections.defaultdict(int)
    for i in list:
        if d[i]<num:
            d[i]+=1
            result.append(i)
    return result

res = delete_nth([1,2,3,1,2,1,3,2,4,2,4,4,2,1],1)
print('res',res)