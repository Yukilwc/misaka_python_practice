import os


def rename_all_file_ext(dir_path,old_ext,new_ext):
    files = os.listdir(dir_path)
    for filename in files:
        print('filename',filename)
        ext_name = os.path.splitext(filename)[1]
        if(ext_name==old_ext):
            new_name = os.path.splitext(filename)[0]+new_ext
            new_path_name = os.path.join(dir_path,new_name)
            old_path_name = os.path.join(dir_path,filename)
            os.rename(old_path_name,new_path_name)
    pass

old_ext = input('输入要替换的旧ext:')
new_ext = input('输入要替换的新ext:')
dir_path= 'D:\\workspace\\work\\web\\sanco\\sanco-web-ssr\\images\\about\\huodongZhongxin\\'
rename_all_file_ext(dir_path,old_ext,new_ext)