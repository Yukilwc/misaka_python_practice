import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from PIL import Image
from operator import contains
import os
import time,threading
from typing import final
from tools.list_tools import list_split
from tools.use_selenium import ChromeUtils
from selenium.webdriver.common.by import By
from tools.file_tools import load_json_file, save_json_file



def start():
    type = input('输入要进行的操作(menu,image,check,pdf):')
    if type=='menu':
        Doc2Pdf().menu_tree_2_json().quit()
    elif type=='image':
        # 截取图片
        Doc2Pdf.multi_thread_generate_with_pool()
        pass
    elif type=='check':
        MenuTree().check_images()
        pass
    elif type=='pdf':
        Doc2Pdf.image_list_2_pdf_by_pillow()
        pass
    else:
        logging.exception('未知的类型')


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


# 控制menu文件数据
class MenuTree(object):
    menu_tree_folder =os.path.join( os.path.dirname(__file__),'dist','json')
    menu_tree_file = 'data.json'
    def __init__(self) -> None:
        total_path = os.path.join(self.menu_tree_folder,self.menu_tree_file)
        self.menu_list = []
        if os.path.exists(total_path):
            self.menu_list = load_json_file(os.path.join(MenuTree.menu_tree_folder,MenuTree.menu_tree_file))
        pass
    # 按核心数获取分组
    def get_multi_core_list(self,thread_num,*,start=None,end=None):
        if start is None:
            list = self.menu_list
        else:
            list = self.menu_list[start:end]
        length = len(list)
        if(thread_num is None):
            thread_num = multiprocessing.cpu_count()
        group_len = length//thread_num
        others = length%thread_num
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

    def get_all_image_local_path_list(self):
        all_list = self.menu_list
        image_list = filter(lambda item:item['url']!='',all_list)
        path_list = [ os.path.join(Doc2Pdf.screen_images_folder,TreeNode.get_name(**node)) for node in image_list]
        return path_list

    # 检查图片完备程度
    def check_images(self):
        all_list =  self.menu_list
        # image_list = filter(lambda item:item['url']!='',all_list)
        not_exist_list = []
        for index,node in enumerate(all_list):
            name = TreeNode.get_name(**node)
            folder = Doc2Pdf.screen_images_folder
            path = os.path.join(folder,name)
            if(node['url']!='' and not os.path.exists(path)):
                print('not exists path',path)
                print('not exists index',index)
                not_exist_list.append(node)
        # print('not exists image',node)
        pass




class Doc2Pdf(object):
    screen_images_folder = os.path.join( os.path.dirname(__file__),'dist','images')
    pdf_folder= os.path.join( os.path.dirname(__file__),'dist','pdf')
    pdf_name = 'book.pdf'
    menu_url = 'https://cn.vuejs.org/guide/introduction.html'
    screen_selector = '#app'

    def __init__(self) -> None:
        print('init Doc2Pdf')
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

    # 通用方法:
    def quit(self):
        self.browser.quit()

    # 业务方法: 
    # 开始前设定内容 例如点击，设置cookie等
    def app_init(self,domain):
        window_with = 1920
        window_height= 9000
        self.browser.set_window_size(window_with,window_height)
        pass

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
        save_json_file(content,folder_path=MenuTree.menu_tree_folder,file_name=MenuTree.menu_tree_file)
        return self
    
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
    
    # 截取保存全部图片
    def screen_all_page(self,list):
        print(' screen_all_page:',list)
       # list分为5份
        for node in list:
            if node['url'] != '':
                self.screen_page(node['url'],TreeNode.get_name(**node))
                # time.sleep(1)
        pass

    @staticmethod
    def image_list_2_pdf_by_pillow():
        list = MenuTree().get_all_image_local_path_list()
        if not os.path.exists(Doc2Pdf.pdf_folder):
            os.makedirs(Doc2Pdf.pdf_folder)
        # 构造首个image和剩余image list 
        img_1= Image.open(list[0]).convert('RGB')
        img_others_list = [Image.open(path ).convert('RGB') for path in list[1:]]
        img_1.save(os.path.join(Doc2Pdf.pdf_folder,Doc2Pdf.pdf_name),save_all=True,append_images=img_others_list)

    @staticmethod
    def multi_thread_generate_with_pool():
        """
        多线程爬取全部菜单页面
        """
        tree = MenuTree()
        thread_num = 8
        # split_list = tree.get_multi_core_list(thread_num)
        split_list = tree.get_multi_core_list(thread_num,start=56,end=58)
        def one_thread(list):
            print('one_thread',len(list))
            try:
                instance = Doc2Pdf()
                instance.screen_all_page(list)
            except Exception as e:
                logging.exception(e)
                logging.exception(list)
            finally:
                instance.quit()
        thread_pool = ThreadPoolExecutor(max_workers=8,thread_name_prefix='scrapy_doc_page_')
        thread_pool.map(one_thread,split_list)
        print('before shutdown')
        thread_pool.shutdown(wait=True)
        print('after shoudown')
        pass



# 多线程爬取
# def multi_thread_generate():
#     start_time = time.time()
#     multi_list =  Doc2Pdf.get_multi_core_list(8)
#     # print('multi_list  len',len(multi_list ))
#     t_list = []
#     for index,value in enumerate(multi_list):
#         t = threading.Thread(target=one_thread, args=(multi_list[index],))
#         t_list.append(t)
#         t.start()

#     for t in t_list:
#         t.join()
#     print('线程结束，耗时:',time.time()-start_time)
#     pass

# def one_thread(list):
#     try:
#         instance = Doc2Pdf()
#         instance.screen_all_page(list)
#     except Exception as e:
#         logging.exception(e)
#         logging.exception(list)
#     finally:
#         instance.quit()



