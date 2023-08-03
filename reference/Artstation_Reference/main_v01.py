# -*- coding: utf-8 -*- 

import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
def get_url(key):
    browser = webdriver.Chrome()
    #打开页面
    url = "https://www.artstation.com/projects/{KEY}.json".format(KEY = key) #替换为你想要访问的地址
    browser.get(url)

    # 等待页面加载完成 
    wait = WebDriverWait(browser, 2)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # 获取页面信息
    page_source = browser.page_source
    browser.quit()

    return re.findall('"image_url":"(.*?)"',page_source)[-1]

def get_urls(key):
    browser = webdriver.Chrome()
    #打开页面
    url = "https://www.artstation.com/projects/{KEY}.json".format(KEY = key) #替换为你想要访问的地址
    browser.get(url)

    # 等待页面加载完成 
    wait = WebDriverWait(browser, 2)
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

    # 获取页面信息
    page_source = browser.page_source
    browser.quit()

    return re.findall('"image_url":"(.*?)"',page_source)

headers = {
    'public-csrf-token': 'iWil5nYPd7yQW8T9CzhgAW7bHomoEN31JdW3XRc0bZrtfWSr2Zm7JDR006opO9bzS7xTSp2xMUEbfe3J+LsMrA==',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36',
    'cookie': '__stripe_mid=01bf723f-ae7b-409f-895d-e484e37e48540ff168; visitor-uuid=ed425b76-d521-4569-bbc7-f3bf4c6f5e6f; __cf_bm=OtyoUq3RnM2V1vT87MrDspqOCA01MfVVKYKxr3CLWSQ-1688311217-0-AdEbRsiqoiYXK8/G596N2/hJy9tvfJrNz1lgldiXF837EmKya8AXl23BGWWtNPNwTFG4cPxbbgExMECt66ghUHumCcAkVUib2+5Av4SQniL0twqPZZq7+VzYFiMIGZEMYw==; PRIVATE-CSRF-TOKEN=ZBXBTa%2BWzJikLxdXIgO28iVnTcM1oey0PqhalO%2BPYTY%3D; __stripe_sid=8a993040-139a-440d-8577-85e2cb72da63f57c07',
}
s=input('输入的关键词')
page=int(input('输要爬的页数'))
num=input('1.放入一个文件夹2.一个文件夹一张照片')
for x in range(1,page+1):
    json_data = {
        'query': s,
        'page': x,
        'per_page': 50,
        'sorting': 'relevance',
        'pro_first': '1',
        'filters': [],
        'additional_fields': [],
    }

    response = requests.post(
        'https://www.artstation.com/api/v2/search/projects.json',
        headers=headers,
        json=json_data,
    ).json()['data']
    for i in response:
        a1=i['id']
        urls=get_url(i['hash_id'])
        for index in range(a2s.count):
            with open("output/Artstation/{ID}_{INDEX}.jpg".format(ID=a1, INDEX=index),'wb')as a:
                a.write(requests.get(url=urls[index],headers=headers).content)
        """
        if num=='1':
            with open("output/Artstation/{a1}.jpg".format(a1=a1),'wb')as a:
                a.write(requests.get(url=a2,headers=headers).content)
        else:
            with open("output/Artstation/{a1}/{a1}.jpg".format(a1=a1),'wb')as a:
                a.write(requests.get(url=a2,headers=headers).content)
        """
