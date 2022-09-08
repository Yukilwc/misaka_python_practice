
# 树节点
class TreeNode(object):
    def __init__(self) -> None:
        pass

class BaseDocToPdf(object):
    def __init__(self,**kv):
        print(' BaseDocToPdf init')
        self.menu_url = kv['menu_url']

    # 浏览器初始化
    def init_browser():
        pass
    # 载入菜单，并存储为json文件
    def load_menu_json():
        pass
    # 截屏一个指定页面的指定区域
    def screen_page():
        pass
    # 截屏菜单图片
    def screen_menu():
        pass
    # 截屏前操作js的钩子
    def js_insert_before_screen_page():
        pass
    def loop_tree_save_images():
        pass
    def get_image_list():
        pass
    def image_list_2_pdf_by_pillow():
        pass
    # 基础工具
    def save_file():
        pass
    def set_cookie():
        pass
    def ocr_convert():
        pass
    # js工具
    # js插入
    def js_insert():
        pass
    def add_style():
        pass
    def remove_el():
        pass