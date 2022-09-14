import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

# 添加试验性参数


class ChromeUtils():
# chrome_driver_path='C:\Program Files\Google\Chrome\Application\chromedriver.exe'
    def __init__(self) -> None:
        # self.chrome_driver_path = chrome_driver_path
        self.arg_list = [
            '--headless',
            '--disable-gpu',
            '--no-sandbox',
            '--ignore-certificate-errors'
            ,'--disable-blink-features=AutomationControlled'
        ]
        # self.arg_list.append('--proxy-server=http://localhost:10080')
        self.chrome_options = Options()
        self.set_options()

    def set_options(self):
        list = self.arg_list
        for item in list:
            self.chrome_options.add_argument(item)
        self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
    def get_browser(self):
        # browser = webdriver.Chrome(executable_path=self.chrome_driver_path,chrome_options=self.chrome_options)
        browser = webdriver.Chrome(chrome_options=self.chrome_options)
        browser.execute_cdp_cmd(
            'Page.addScriptToEvaluateOnNewDocument',
            {'source': 'Object.defineProperty(navigator, "webdriver", {get: () => undefined})'}
        )
        return browser

    @staticmethod
    def wait_selector(browser,selector):
        # 创建等待对象
        wait_obj = WebDriverWait(browser,10)
        wait_obj.until(
            expected_conditions.presence_of_element_located(
                (By.CSS_SELECTOR,selector)
            )
        )
    @staticmethod
    def screenshot_body(browser):
        body_el = browser.find_element(By.CSS_SELECTOR,'body')
        body_el.screenshot('body.png')

    @staticmethod
    def set_localstorage(browser,key,value):
        pass

    @staticmethod
    def remove_el(browser,selector):
        js_path =os.path.join( os.getcwd(),'html_doc_2_pdf','lib','javascript','remove_el.js')
        with open(js_path,'r') as f:
            js_string = f.read()
            js_string = js_string.replace('replace_str_selector','"%s"' % selector)
            res =browser.execute_script(js_string)
            print(res)

    @staticmethod
    def add_style(browser,selector,*,style_name,style_value):
        js_path =os.path.join( os.getcwd(),'html_doc_2_pdf','lib','javascript','add_style.js')
        with open(js_path,'r') as f:
            js_string = f.read()
            js_string = js_string.replace('replace_str_selector','"%s"' % selector)
            js_string = js_string.replace('replace_str_style_name','"%s"' % style_name)
            js_string = js_string.replace('replace_str_style_value','"%s"' % style_value)
            res = browser.execute_script(js_string)
            print(res)

    # 获取指定选择器元素宽高
    @staticmethod
    def get_window_size(browser,selector):
        ChromeUtils.wait_selector(browser,selector)
        el = browser.find_element(By.CSS_SELECTOR,selector)
        loc = el.location
        size = el.size
        return dict(width=size['width'],height=loc['y']+size['height'])
