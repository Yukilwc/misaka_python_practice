
from codecs import ignore_errors
from importlib.resources import path
from tools.file_tools import save_json_file,load_json_file
import re
import os

# 匹配黑名单
folder_black_list = ['node_modules','.git','etransNew']
root_path = r'D:\workspace\work\web\gitee\etranscode\etransNew'
# flag =re.I|re.M
flag =re.I

class SearchNode(object):
    def __init__(self) -> None:
        self.path = ''
        self.relative_path = ''
        # 匹配到的内容
        self.content = ''
        # 匹配到的行元组
        self.line_list = []
        # 位置元组
        self.span_list = []
        # 匹配到的文件路径

def get_line_with_loc(all_content,loc):

    pass

def search(filter_list):
    res_list = []
    # 遍历全部文件 构造node数组
    all_node_list = []
    loop_all_files(root_path,all_node_list)
    for node in all_node_list:
        with open(node.path,'r',encoding='utf8',errors='ignore') as f:
            file_content = f.read()
            for index,filter_func in enumerate(filter_list):
                if index==0:
                    node.span_list = [(0,len(file_content))]
                filter_func(node,file_content)
    content = [{"relative_path":node.relative_path,'path':node.path,"line_list":node.line_list} for node in all_node_list if len(node.span_list)>0]
    print('search result length:',len(content))
    save_json_file(content,folder_path= os.path.dirname(os.path.realpath(__file__)),file_name='res.json')
    # is_open = input('是否打开全部查询结果%s个文件,1是2否?'%len(content))
    # if(int(is_open)==1):
    #     for node in content:
    #         open_path = node['path']
    #         os.system('code %s'%open_path)

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
            node.relative_path = node.path.replace(root_path,'')
            all_node_list.append(node)
        else:
            loop_all_files(subpath,all_node_list)

def filter_factory(reg_str):
    def f(node,file_content):
        if(len(node.span_list)==0):
            return
        # 新构造的本次查询的span
        find_span_list = []
        find_line_list = []
        for span in node.span_list:
            start = span[0]
            end = span[1]
            target_str = file_content[start:end]
            find_res = re.finditer(reg_str,target_str)
            for match in find_res:
                sub_span = match.span()
                real_start = start+sub_span[0]
                real_end = start+sub_span[1]
                find_span_list.append((real_start,real_end))
                # node.content = match.group()
                find_line_list.append((
                    file_content.count('\n',0,real_start)+1,
                    file_content.count('\n',0,real_end)+1
                    ))
        node.span_list = find_span_list
        node.line_list = find_line_list
    return f





reg_list = [
    r'<div.+?class.+?content.+?>[\s\S\n]*</div>', # 匹配主表格
    r'<el-table-column[\s\S\n]*?>([\s\S\n]*?)</el-table-column>', # 匹配el-table-column
    r'(</i>|<img)' # 匹配包含图标
]


filter_list = [filter_factory(f) for f in reg_list]

res_list = search(filter_list)

# black_res = is_black('node_modules/vue')
# print('black_res ',black_res )

# os.system(r'code D:\\workspace\\work\\web\\gitee\\etranscode\\etransNew\\src\\App.vue')