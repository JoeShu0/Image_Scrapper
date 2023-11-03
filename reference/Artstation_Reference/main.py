import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re
import os

MainFolder = "Artstation"

def validateTitle(title):
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title
def get_url(key):
    coptions = webdriver.ChromeOptions()
    #coptions.add_argument("--headless")
    coptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=coptions)

    # 打开页面
    url = "https://www.artstation.com/projects/{KEY}.json".format(KEY = key)  # 替换为你想要访问的地址
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
s=input('输入的关键词: ')
ssd=int(input('输要爬的个数: '))
page=int(ssd//50)
ssd=int(ssd%50)
if page>0:
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
        for u,i in enumerate(response):
            if x==page:
                if u <= ssd:
                    a1=i['title']+'-'+i['hash_id']
                    a2=get_url(i['hash_id'])
                    a3=i['hash_id']
                    for x,r in enumerate (a2):
                        path=validateTitle(a1)
                        try:
                            os.makedirs(f'Output\\Artstation\\{path}')
                        except:
                            path=validateTitle(a3)
                            os.makedirs(f'Output\\Artstation\\{path}')
                        if x==1:
                            pass
                        else:
                            name=str(r).split('/')[-1].split('?')[0]
                            with open(f'Output\\Artstation\\{path}\{name}','wb')as a:
                                a.write(requests.get(r).content)
                            print(f'{path}-{name}写入完成')
            else:
                a1=i['title']+'-'+i['hash_id']
                a2=get_url(i['hash_id'])
                a3=i['hash_id']
                
                for x,r in enumerate (a2):
                    path=str(validateTitle(a1)).replace(' ','')[:127]
                    try:
                        os.makedirs(f'Output\\Artstation\\{path}')
                    except:
                        pass
                    if x==1:
                        pass
                    else:
                        name=str(r).split('/')[-1].split('?')[0]
                        with open(f'Output\\Artstation\\{path}\{name}','wb')as a:
                            a.write(requests.get(r).content)
                        print(f'{path}-{name}写入完成')

else:
    for x in range(1,2):
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
        for u,i in enumerate(response):
                if u <= ssd:
                    a1=i['title']+'-'+i['hash_id']
                    a2=get_url(i['hash_id'])
                    a3=i['hash_id']
                    print(a2)
                    for x,r in enumerate (a2):
                        path=str(validateTitle(a1)).replace(' ','')[:127]
                        try:
                            os.makedirs(f'Output\\Artstation\\{path}')
                        except:
                            pass
                        if x==1:
                            pass
                        else:
                            name=str(r).split('/')[-1].split('?')[0]
                            with open(f'Output\\Artstation\\{path}\{name}','wb')as a:
                                a.write(requests.get(r).content)
                            print(f'{path}-{name}写入完成')


