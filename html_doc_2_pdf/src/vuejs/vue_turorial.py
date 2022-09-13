import logging
import multiprocessing
from operator import contains
import os
import time,threading
from typing import final
from tools.list_tools import list_split
from tools.use_selenium import ChromeUtils
from selenium.webdriver.common.by import By
from tools.file_tools import load_json_file, save_json_file


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

    @staticmethod
    def get_name(**kw):
        return '%s_%s.png' % (kw['pid'],kw['id'])
class VueTurorialDoc2Pdf(object):
    menu_tree_folder =os.path.join( os.path.dirname(__file__),'dist','json')
    screen_images_folder = os.path.join( os.path.dirname(__file__),'dist','images')
    menu_url = 'https://cn.vuejs.org/guide/introduction.html'
    menu_tree_file = 'data.json'
    screen_selector = '#app'
    def __init__(self) -> None:
        print('init VueTurorialDoc2Pdf')
        self.chrome_utils = ChromeUtils()
        self.browser = self.chrome_utils.get_browser()
        try:
            self.app_init(domain=self.menu_url)
            # self.menu_tree_2_json()
            # self.screen_all_page()
        except Exception as e:
            logging.exception(e)
            self.browser.quit()
        finally:
            pass
    def quit(self):
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
    
    # 截取页面
    def screen_page(self,url,name):
        self.browser.get(url)
        self.on_before_screen()
        # ChromeUtils.screenshot_body(self.browser)
        el = self.browser.find_element(By.CSS_SELECTOR,self.screen_selector)
        if not os.path.exists(self.screen_images_folder):
            os.makedirs(self.screen_images_folder)
        el.screenshot(os.path.join(self.screen_images_folder,name))
        pass

    # 截屏前钩子
    def on_before_screen(self):
        window_with = 1920
        window_height= 1080
        self.browser.set_window_size(window_with,window_height)
        # 去除多余元素
        ChromeUtils.remove_el(self.browser,'.banner')
        ChromeUtils.remove_el(self.browser,'.nav-bar')
        ChromeUtils.remove_el(self.browser,'.aside-container >div:not(.VPContentDocOutline)')
        ChromeUtils.remove_el(self.browser,'.vuejobs-wrapper')
        # 修正样式
        ChromeUtils.add_style(self.browser,'.VPSidebar',style_name="top",style_value='0px')
        ChromeUtils.add_style(self.browser,'.VPApp',style_name="paddingTop",style_value='0px')
        ChromeUtils.add_style(self.browser,'.VPContent',style_name="paddingTop",style_value='0px')
        # 设置尺寸
        size = ChromeUtils.get_window_size(self.browser,self.screen_selector)
        self.browser.set_window_size(size['width'],size['height'])
        print('on_before_screen finished')
        pass
    
    def test_multi(self):
        print(' test_multi',self.screen_images_folder)
    # 截取保存全部图片
    def screen_all_page(self,list):
        print(' screen_all_page:',list)
       # list分为5份
        for node in list:
            if node['url'] != '':
                self.screen_page(node['url'],TreeNode.get_name(**node))
                # time.sleep(1)
        pass
    # 按核心数获取分组
    @staticmethod
    def get_multi_core_list(thread_num):
        list = VueTurorialDoc2Pdf.get_all_list()
        # FIXME:
        # list = list[46-1:46+1-1]
        length = len(list)
        if(thread_num is None):
            thread_num = multiprocessing.cpu_count()
        group_len = length//thread_num
        others = length%thread_num
        # if length%thread_num>0:
            # group_len+=1
        if len(list)<=thread_num:
            split_list = list_split(list,1)
        else:
            split_list = list_split(list[0:length-others],group_len)
            others_list = list[length-2:length]
            final_item = split_list.pop()
            if final_item==None:
                final_item = []
            final_item = final_item+others_list
            split_list.append(final_item)
        return split_list

    @staticmethod
    def get_all_list():
        list = load_json_file(os.path.join(VueTurorialDoc2Pdf.menu_tree_folder,VueTurorialDoc2Pdf.menu_tree_file))
        return list

    def test_multi(self,args):
        print('multi core',self.screen_images_folder,args)

# 多线程爬取
def multi_thread_generate():
    start_time = time.time()
    multi_list =  VueTurorialDoc2Pdf.get_multi_core_list(8)
    # print('multi_list  len',len(multi_list ))
    t_list = []
    for index,value in enumerate(multi_list):
        t = threading.Thread(target=one_thread, args=(multi_list[index],))
        t_list.append(t)
        t.start()

    for t in t_list:
        t.join()
    print('线程结束，耗时:',time.time()-start_time)
    pass

def one_thread(list):
    try:
        instance = VueTurorialDoc2Pdf()
        instance.screen_all_page(list)
    except Exception as e:
        logging.exception(e)
        logging.exception(list)
    finally:
        instance.quit()


def multi_thread_generate_with_pool():
    pass

# 多进程爬取
def multi_process_generate():
    instance = VueTurorialDoc2Pdf()
    p = multiprocessing.Process(target=instance.test_multi, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
 
    pass
# 检查图片完备程度
def check_images():
    all_list =  VueTurorialDoc2Pdf.get_all_list()
    image_list = filter(lambda item:item['url']!='',all_list)
    not_exist_list = []
    for node in image_list:
        name = TreeNode.get_name(**node)
        folder = VueTurorialDoc2Pdf.screen_images_folder
        path = os.path.join(folder,name)
        if(not os.path.exists(path)):
            print('not exists path',path)
            not_exist_list.append(node)
    # print('not exists image',node)
    pass