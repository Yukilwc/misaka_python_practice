from lib2to3.pgen2 import driver
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
    browser.quit()





