import json
import os
# 存储文件夹路径和文件，覆盖文件，路径不存在则新建路径
def save_json_file(content,*,folder_path,file_name):
    json_str = json.dumps(content,indent=4,ensure_ascii=False)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    with open(os.path.join(folder_path,file_name),'w',encoding='utf8') as f:
        f.write(json_str)

def load_json_file(file_path):
    json_str = ''
    with open(file_path,'r',encoding='utf8') as f:
        json_str = f.read()
    return json.loads(json_str)



