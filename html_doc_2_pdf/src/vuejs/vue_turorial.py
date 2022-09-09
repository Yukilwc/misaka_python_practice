import logging
import os
from tools.use_selenium import ChromeUtils
from selenium.webdriver.common.by import By
from tools.file_tools import save_folder_file
class VueTurorialDoc2Pdf(object):
    def __init__(self) -> None:
        print('init VueTurorialDoc2Pdf')
        self.menu_url = 'https://cn.vuejs.org/guide/introduction.html'
        self.chrome_utils = ChromeUtils()
        self.browser = self.chrome_utils.get_browser()
        try:
            self.app_init(domain=self.menu_url)
            self.menu_tree_2_json()
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
    def menu_tree_2_json():
        menu_tree_folder = './json/menu/'
        menu_tree_file = 'data.json'
        content = dict(a=1)
        save_folder_file(content,folder_path=menu_tree_folder,file_name=menu_tree_file)
        pass