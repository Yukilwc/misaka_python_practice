"""
There are people sitting in a circular fashion,
print every third member while removing them,
the next counter starts immediately after the member is removed.
Print till all the members are exhausted.
For example:
Input: consider 123456789 members sitting in a circular fashion,
Output: 369485271
"""

def josephus(int_list, skip):
    int_list = list(int_list)
    length = len(int_list)
    skip -= 1
    idx = 0
    while length>0:
        idx = (idx+skip)%length
        print('索引idx:',idx,',',int_list)
        yield int_list.pop(idx)
        length-=1

print(''.join([i for i in josephus('123456789876543210',3)]))