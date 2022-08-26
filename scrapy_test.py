import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
main_page = 'https://python3-cookbook.readthedocs.io/zh_CN/latest/index.html'
chrome_path= 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
# browser.maximize_window()
# browser.set_window_size()
def screenMenu():
    try:
        browser.get(main_page)
        browser.implicitly_wait(3)
        titleEl = browser.find_elements(By.CSS_SELECTOR,"#python-cookbook-3rd-edition-documentation")[0]
        # titleEl = browser.find_elements(By.CSS_SELECTOR,"body")[0]
        loc = titleEl.location
        size = titleEl.size
        window_with = 1920
        window_height= loc['y']+size['height']
        browser.set_window_size(window_with,window_height)
        DOWNLOAD_PATH = './images/'
        if not os.path.exists(DOWNLOAD_PATH):
            os.makedirs(DOWNLOAD_PATH)
        # with open(os.path.join(DOWNLOAD_PATH, 'TOC.png'), 'wb') as file:
        #         file.write(browser.get_screenshot_as_png())
        # browser.save_screenshot(os.path.join(DOWNLOAD_PATH, 'TOC.png'))
        titleEl.screenshot(os.path.join(DOWNLOAD_PATH, 'TOC.png'))
    finally:
        print('finally quit')


# screenMenu()

def getTocTree():
    selector_level_1 = '#python-cookbook-3rd-edition-documentation .toctree-wrapper .toctree-l1'
    selector_level_2 = '.toctree-l2'
    browser.get(main_page)
    browser.implicitly_wait(3)
    el_list = browser.find_elements(By.CSS_SELECTOR,selector_level_1)
    id = 0
    node_list = []
    for index,el in enumerate(el_list):
        first_node,link_el = generate_node_from_el(el,'.toctree-l1>a',id+1,0)
        node_list.append(first_node)
        # 构造子级
        second_link_list = link_el.find_elements(By.CSS_SELECTOR,selector_level_2)
        for index,second_el in enumerate(second_link_list):
            second_node,second_link_el = generate_node_from_el(second_el,'.toctree-l2>a',id+1,first_node['id'])
            node_list.append(second_node)
            pass
    json_str = json.dumps(node_list,indent=4,ensure_ascii=False)
    saveFile('./json/','all_menu.json',json_str)


def generate_node_from_el(el,selector,id,pid):
    link_el = el.find_element(By.CSS_SELECTOR,selector)
    if(link_el is not None):
        url = link_el.get_attribute('href')
        title =  link_el.text
        node = dict(id=id,url=url,title=title,pid=pid)
        return node,link_el
    else:
        return None,None
def saveFile(folder,file_name,content):
    if not os.path.exists(folder):
        os.makedirs(folder)
    with open(os.path.join(folder,file_name),'w',encoding="utf8") as f:
        f.write(content)
        pass
    pass

try: 
    getTocTree()
except Exception as e:
    logging.exception(e)
finally: 
    pass
browser.quit()



