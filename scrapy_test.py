import json
from PIL import Image
import logging
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--ignore-certificate-errors') #忽略一些莫名的问题
chrome_options.add_argument('--disable-blink-features=AutomationControlled')  # 谷歌88版以上防止被检测
# 添加试验性参数
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
chrome_options.add_experimental_option('useAutomationExtension', False)
main_page = 'https://python3-cookbook.readthedocs.io/zh_CN/latest/index.html'
chrome_path= 'C:\Program Files\Google\Chrome\Application\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chrome_path,chrome_options=chrome_options)
browser.execute_cdp_cmd(
    'Page.addScriptToEvaluateOnNewDocument',
    {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
)
# browser.maximize_window()
# browser.set_window_size()
# 通过js脚本，给页面添加padding
def add_style(driver,selector,**kw):
    with open('./js_string/add_style.js','r') as f:
        js_string = f.read()
        js_string = js_string.replace('replace_str_selector','"%s"' % selector)
        js_string = js_string.replace('replace_str_style_name','"%s"' % kw['style_name'])
        js_string = js_string.replace('replace_str_style_value','"%s"' % kw['style_value'])
        res = driver.execute_script(js_string)
        print(res)

def remove_el(driver,selector):
    with open('./js_string/remove_el.js','r') as f:
        js_string = f.read()
        js_string = js_string.replace('replace_str_selector','"%s"' % selector)
        res = driver.execute_script(js_string)
        print(res)

def screenMenu():
    try:
        selector = '.wy-nav-content'
        browser.get(main_page)
        # 创建等待对象
        wait_obj = WebDriverWait(browser,10)
        wait_obj.until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR,selector)
            )
        )
        # 隐式等待
        # browser.implicitly_wait(3)
        titleEl = browser.find_elements(By.CSS_SELECTOR,selector)[0]
        remove_el(browser,'.wy-nav-content footer')
        add_style(browser,selector,style_name="paddingTop",style_value='30px')
        add_style(browser,selector,style_name="paddingBottom",style_value='30px')
 
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
        id = id + 1
        first_node,link_el = generate_node_from_el(el,'.toctree-l1>a',id,0)
        node_list.append(first_node)
        # 构造子级
        second_link_list = el.find_elements(By.CSS_SELECTOR,selector_level_2)
        for index,second_el in enumerate(second_link_list):
            id = id + 1
            second_node,second_link_el = generate_node_from_el(second_el,'.toctree-l2>a',id,first_node['id'])
            node_list.append(second_node)
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

# try: 
#     getTocTree()
# except Exception as e:
#     logging.exception(e)
# finally: 
#     pass

 
def screenPage(page,selector):
    browser.get(page['url'])
    # 创建等待对象
    wait_obj = WebDriverWait(browser,10)
    wait_obj.until(
        expected_conditions.presence_of_element_located(
            (By.CSS_SELECTOR,selector)
        )
    )
    # 隐式等待
    # browser.implicitly_wait(3)
    titleEl = browser.find_elements(By.CSS_SELECTOR,selector)[0]
    # 移除页脚
    remove_el(browser,'.wy-nav-content footer')
    add_style(browser,selector,style_name="paddingTop",style_value='30px')
    add_style(browser,selector,style_name="paddingBottom",style_value='30px')
    loc = titleEl.location
    size = titleEl.size
    window_with = 1920
    window_height= loc['y']+size['height']
    browser.set_window_size(window_with,window_height)
    DOWNLOAD_PATH = './images/'
    if not os.path.exists(DOWNLOAD_PATH):
        os.makedirs(DOWNLOAD_PATH)
    # file_name = '%s_%s_%s.png'%(page['pid'],page['id'],page['title'])
    file_name = '%s_%s.png'%(page['pid'],page['id'])
    titleEl.screenshot(os.path.join(DOWNLOAD_PATH, file_name))
 

# try: 
#     page = {
#         "id": 13,
#         "url": "https://python3-cookbook.readthedocs.io/zh_CN/latest/c01/p01_unpack_sequence_into_separate_variables.html",
#         "title": "1.1 将序列分解为单独的变量",
#         "pid": 12
#     }
#     screenPage(page,'.wy-nav-content')
# except Exception as e:
#     logging.exception(e)
# finally: 
#     pass

def loop_tree_save_image():
    jsonStr = ''
    with open("./json/all_menu.json",'r',encoding="utf8") as f:
        jsonStr = f.read()
    all_menu = list(json.loads(jsonStr))
    length = len(all_menu) 

    for  index in range(0,length):
        print(index)
        page = all_menu[index]
        if page is None:
            return
        screenPage(page,'.wy-nav-content')
        time.sleep(1)

# try: 
#     loop_tree_save_image()
# except Exception as e:
#     logging.exception(e)
# finally: 
#     pass

def get_image_list():
    list_str = ''
    with open('./json/all_menu.json','r',encoding='utf8') as f:
        list_str = f.read()
    all_menu = list(json.loads(list_str))
    TOC_image_path = './images/TOC.png'
    res_list = []
    res_list.append(TOC_image_path)
    res_list = res_list + list(map(lambda item:'./images/%s_%s.png'%(item['pid'],item['id']),all_menu))
    return res_list

def image_list_2_pdf_by_pillow(list=[]):
    pdf_dir = './generate_pdf/'
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)
    # 构造首个image和剩余image list 
    img_1= Image.open(list[0]).convert('RGB')
    img_others_list = [Image.open(path ).convert('RGB') for path in list[1:]]
    img_1.save(os.path.join(pdf_dir,"python_cookbook.pdf"),save_all=True,append_images=img_others_list)

try: 
    all_image_list = get_image_list()
    image_list_2_pdf_by_pillow(all_image_list)
except Exception as e:
    logging.exception(e)
finally: 
    pass


browser.quit()



