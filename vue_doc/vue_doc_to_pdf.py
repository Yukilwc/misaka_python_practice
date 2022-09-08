import sys
import os
# sys.path.append(os.path.join('.','../base_doc_to_pdf.py') )
# real_path = os.path.realpath(__file__)
# dir_name = os.path.dirname(real_path)
# p_path = os.path.join(real_path,'..','..','doc_to_pdf')
# sys.path.append(r'D:\workspace\libiary\my\misaka_python_practice')

# 从子模块导入方法
from doc_to_pdf.base_doc_to_pdf.base import  BaseDocToPdf
options = dict(
    menu_url='http://www.baidu.com'
)
BaseDocToPdf(**options)
