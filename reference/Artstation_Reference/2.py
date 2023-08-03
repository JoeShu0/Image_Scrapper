from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
# 创建浏览器实例
def get_url(key):
    browser = webdriver.Chrome()
    # 打开页面
    url = f"https://www.artstation.com/projects/{key}.json"  # 替换为你想要访问的地址
    browser.get(url)

    # 等待页面加载完成
    wait = WebDriverWait(browser, 2)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # 获取页面信息
    page_source = browser.page_source
    browser.quit()

    return re.findall('"image_url":"(.*?)"',page_source)[-1]
get_url('21G6y')