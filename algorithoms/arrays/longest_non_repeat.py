"""
Given a string, find the length of the longest substring
without repeating characters.

Examples:
Given "abcabcbb", the answer is "abc", which the length is 3.
Given "bbbbb", the answer is "b", with the length of 1.
Given "pwwkew", the answer is "wke", with the length of 3.
Note that the answer must be a substring,
"pwke" is a subsequence and not a substring.
"""

# 思路：
# 核心思路是找非重复子串，发现重复后，末尾前进一个字符，进入新子串，再继续前进
# 首先维护三个状态
# 1.需要返回的最大长度 2.一个dict，其暂存遍历过程中的字符为key，此字符最新出现的下一个位置的索引
# 3是错的理解
# 3.由于遍历中，总是能获得最新的前方的索引,而要获得最大长度，还需要一个后方的索引，总是指向此非重复串的末尾，也就是上一个重复字符的位置，维护
# 为no_repeat_str_first_index
# 之后是操作
# 循环参数的字符串，逐个获取索引
# 如果索引对应的字符，已经存在于dict中了，则证明重复，则更新no_repeat_str_first_index
# no_repeat_str_first_index的更新如下:
# 先从dict中获取该字符的value，此value为该 重复字符 上一次出现的位置的下一个位置的索引
def longest_non_repeat_v1(string):
    """
    Find the length of the longest substring
    without repeating characters.
    """
    max_length = 0
    no_repeat_str_first_index = 0
    d = {}
    for i in range(len(string)):
        pass
    

def longest_non_repeat_v2(string):
    """
    Find the length of the longest substring
    without repeating characters.
    Uses alternative algorithm.
    """
    

# get functions of above, returning the max_len and substring
def get_longest_non_repeat_v1(string):
    """
    Find the length of the longest substring
    without repeating characters.
    Return max_len and the substring as a tuple
    """
    

def get_longest_non_repeat_v2(string):
    """
    Find the length of the longest substring
    without repeating characters.
    Uses alternative algorithm.
    Return max_len and the substring as a tuple
    """