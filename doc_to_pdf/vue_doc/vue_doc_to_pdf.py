import sys
import os
# sys.path.append(os.path.join('.','../base_doc_to_pdf.py') )
sys.path.append(r'D:\workspace\libiary\my\misaka_python_practice\doc_to_pdf')

# 直接导入子模块 
# import base_doc_to_pdf.base_tools
# base_doc_to_pdf.base_tools.hello()

# 从主模块中导入子模块 
# from base_doc_to_pdf import base_tools
# base_tools.hello()

# 从子模块导入方法
# from base_doc_to_pdf.base_tools import hello
# hello()

# 错误 子模块不可使用点号运算符调用，方法才可以
# import base_doc_to_pdf
# base_doc_to_pdf.base_tools.hello()

