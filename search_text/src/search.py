
from importlib.resources import path
from tools.file_tools import save_json_file,load_json_file
import re
import os

# 匹配黑名单
folder_black_list = ['node_modules','.git','etransNew']
root_path = r'D:\workspace\work\web\gitee\etranscode\etransNew'

class SearchNode(object):
    def __init__(self) -> None:
        # 匹配到的内容
        self.content = ''
        # 匹配到的行元组
        self.line = (0,0)
        # 匹配到的文件路径
        self.path = ''

def search(filter_list):
    res_list = []
    # 遍历全部文件 构造node数组
    all_node_list = []
    loop_all_files(root_path,all_node_list)
    pass

def is_black(name):
    res = False
    for black_item in folder_black_list:
        if re.match(re.compile(black_item,re.IGNORECASE),name):
            res = True
            break;
    return res
 
def loop_all_files(folder_path,all_node_list):
    dirs = os.listdir(folder_path)
    dirs = [p for p in dirs if not is_black(p)]
    for d in dirs:
        subpath = os.path.join(folder_path,d)
        if(os.path.isfile(subpath)):
            node = SearchNode()
            node.path = subpath
            all_node_list.append(node)
        else:
            loop_all_files(subpath,all_node_list)

def f1():
    pass

def f2():
    pass


filter_list = [
    f1,
    f2
]

res_list = search(filter_list)

# black_res = is_black('node_modules/vue')
# print('black_res ',black_res )