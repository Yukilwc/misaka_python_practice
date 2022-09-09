import logging
import os
from tools.use_selenium import ChromeUtils
from selenium.webdriver.common.by import By
from tools.file_tools import save_json_file


class TreeNode(object):
    def __init__(self) -> None:
        self.id = ''
        self.pid =  ''
        self.title = ''
        self.url = '' 
        pass
    def from_title_el(self,el,*,id,pid):
        self.id = id
        self.pid =  pid
        self.title = el.text
        self.url = '' 
        return self
    def from_link_el(self,el,*,id,pid):
        self.id = id
        self.pid =  pid
        self.title = el.text
        self.url = el.get_attribute('href') 
        return self
class VueTurorialDoc2Pdf(object):
    def __init__(self) -> None:
        print('init VueTurorialDoc2Pdf')
        self.menu_tree_folder =os.path.join( os.path.dirname(__file__),'json','menu')
        self.menu_tree_file = 'data.json'
        self.menu_url = 'https://cn.vuejs.org/guide/introduction.html'
        self.chrome_utils = ChromeUtils()
        self.browser = self.chrome_utils.get_browser()
        try:
            self.app_init(domain=self.menu_url)
            # self.menu_tree_2_json()
        except Exception as e:
            logging.exception(e)
        finally:
            self.browser.quit()
    # 开始前设定内容 例如点击，设置cookie等
    def app_init(self,domain):
        self.browser.get(domain)
        # cookie_dict = dict(name='vue-docs-prefer-composition',value=True)
        # self.browser.delete_cookie('vue-docs-prefer-composition')
        # self.browser.add_cookie(cookie_dict)
        # self.browser.refresh()
        window_with = 1920
        window_height= 9000
        self.browser.set_window_size(window_with,window_height)
        check_selector = '.vt-switch.api-switch'
        ChromeUtils.wait_selector(self.browser,check_selector)
        check_btn = self.browser.find_element(By.CSS_SELECTOR,check_selector)
        check_btn.click()
    # 获取目录树json
    def menu_tree_2_json(self):
        menu_selector = 'aside .group'
        self.browser.get(self.menu_url)
        ChromeUtils.wait_selector(self.browser,'aside')
        node_list = []
        id = 0
        group_el_list = self.browser.find_elements(By.CSS_SELECTOR,menu_selector)
        for group_el in group_el_list:
            title_el = group_el.find_element(By.CSS_SELECTOR,'.title')
            link_el_list = group_el.find_elements(By.CSS_SELECTOR,'.link')
            id = id+1
            title_node = TreeNode().from_title_el(title_el,id=id,pid=0)
            node_list.append(title_node)
            for link_el in link_el_list:
                id=id+1
                link_node = TreeNode().from_link_el(link_el,id=id,pid=title_node.id)
                node_list.append(link_node)
        content = [node.__dict__ for node in node_list]
        save_json_file(content,folder_path=self.menu_tree_folder,file_name=self.menu_tree_file)
        pass