#Simple downloader for pinterest
from concurrent.futures import ThreadPoolExecutor

import os
import json
import shutil
import time
import requests
import sys

from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from Includes import SeleniumUtils
from Includes import GeneralFuncs

baselink = "https://www.pinterest.com/"

Mainfolder = "Pinterest\\"

timeout = 2

isLogin = False

def LoginPinterest(driver):
    SeleniumUtils.WaitForElement(driver, By.XPATH, '//div[@data-test-id="unauth-header"]/div//button') 
     # click login
    header_elements = driver.find_elements(by=By.XPATH, value='//div[@data-test-id="unauth-header"]/div//button')
    for element in header_elements:
        if element.text == '登录':
            login_element = element
            login_element.click()
            break
    #check loading
    SeleniumUtils.WaitForElement(driver, By.XPATH, '//input[@type="email"]') 
    # send username and keywords
    username_element = driver.find_elements(by=By.XPATH, value='//input[@type="email"]')[0]
    password_element = driver.find_elements(by=By.XPATH, value='//input[@type="password"]')[0]
    login_button = driver.find_elements(by=By.XPATH,
                                        value='//div[@data-test-id="registerFormSubmitButton"]/button')[0]


    username = input("輸入pinterest的郵箱: ")
    password = input("輸入密碼: ")
    username_element.send_keys(username)
    password_element.send_keys(password)
    """
    savestr = input("是否记住登录信息？（Y/N）: ")
    if(savestr == "Y" or savestr == "y"):
        save"""

    login_button.click()
    #check login
    SeleniumUtils.WaitForElement(driver, By.XPATH, '//input[@name="searchBoxInput"]', 8)

def GetImageLinksfortag(driver, tag, pages):
    #Search
    search_element = driver.find_elements(by=By.XPATH, value='//input[@name="searchBoxInput"]')[0]
    prompts = len(search_element.get_attribute("value")) + 2# Additional BS 
    search_element.send_keys(Keys.BACKSPACE * prompts)
    search_element.send_keys(tag)
    search_element.send_keys(Keys.ENTER)

    #check loading
    SeleniumUtils.WaitForElement(driver, By.XPATH, '//div[@data-test-id="non-story-pin-image"]/div/img')

    ImageLinks = []
    
    for p in range(pages):
        print(f'正在遍历第{p}页图片...')
        time.sleep(4)
        page_elements = driver.find_elements(By.XPATH, '//div[@data-test-id="non-story-pin-image"]/div/img')
        for elem in page_elements:
            #img_url = elem.get_attribute("src")
            #imglink = img_url.replace('236x', 'originals')
            #获取最大尺寸的图片链接
            imglink = elem.get_attribute("srcset").split(" ")[-2]
            name = elem.accessible_name
            name = name.split(":")
            if(len(name)==1):
                imgname = imglink.split("/")[-1].split(".")[0]
            else:
                imgname = name[1].replace("\\", "").replace("/", "").replace("|", "")
                imgname = "".join( x for x in imgname if (x.isalnum() or x in "._- "))
                #postfix = "." + imglink.split(".")[-1]
            if(len(imgname) > 120):
                #当文件名过长时，有可能是推广。
                continue
            ImageLinks.append((imgname,imglink))

        #向下滚动，载入指定位置叶页
        driver.execute_script(f"window.scrollTo({(p+1) * 1000}, "f"{ (p+1) * 1000});")

    ImageLinks = list(dict.fromkeys(ImageLinks))
    return ImageLinks


def DownloadImageLinks(ImageLinks, tag):
    path = "output\\"+ Mainfolder + tag + "\\"
    os.makedirs(path , exist_ok=True)
    for imgname, imglink in ImageLinks:
        print(imgname)
        print(imglink)
        GeneralFuncs.download_image_by_url(imgname, imglink, path)

            

    

if __name__ == "__main__":
    print("这是一个用来爬取Pinterest图片的脚本。需要提供账号和密码。\n频繁使用可能导致IP被BAN，请谨慎使用：")
    print("使用前需要保证你的能够正常的登陆上此网站，且没有账户安全提示阻止登录")
    print("----------------------------------------------")
    driver = SeleniumUtils.GetChromeDriver()
    print("正在载入Pinterest...")
    driver.get(baselink)


    LoginPinterest(driver)

    while(True):
        #input for tag
        tag = input("输入需要搜索的关键字，使用空格隔开: ")
        pages = input("要下载多少页图片？（推荐1~20）: ")
        ImageLinks = GetImageLinksfortag(driver, tag, pages)
        try:
            DownloadImageLinks(ImageLinks, tag)
        except Exception as error:
            print("下载过程中出现报错:", error)
            pass
