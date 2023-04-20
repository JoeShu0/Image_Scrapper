#Simple downloader for pixiv
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


baselink = "https://www.pixiv.net/"

savefolder = "Ranking\\"

timeout = 2

isLogin = False

def LoginPixiv():
    print("正在载入Pixiv...")
    #driver = webdriver.Chrome()
    coptions = webdriver.ChromeOptions()
    coptions.add_argument('--ignore-certificate-errors')
    coptions.add_argument('--ignore-ssl-errors')
    # 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
    #coptions.add_experimental_option('excludeSwitches', ['enable-automation'])
    # 忽略 DevTools listening on ws://127.0.0.1... 提示
    coptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    coptions.page_load_strategy = 'eager'
    driver = webdriver.Chrome(options=coptions)

    driver.get(baselink)

    loginlink = driver.find_element(By.PARTIAL_LINK_TEXT, '登录')
    loginlink.send_keys(Keys.ENTER)
    print("登录能够下载一些敏感的图片，不登录只能下载缩略图")
    username = input("輸入Pixiv的用戶名或者郵箱: ")
    password = input("輸入密碼: ")
    print("正在登录Pixiv...")

    usernameinput_elems = driver.find_elements(By.TAG_NAME, "input")
    usernameinput_elems[0].get_property("type")
    namebox = ""
    pwbox = ""
    for elem in usernameinput_elems:
        type = elem.get_property("type")
        if type == "text":
            namebox = elem
        elif type == "password":
            pwbox = elem

    namebox.send_keys(username)
    pwbox.send_keys(password)

    if username != "" and password != "":
        print("正在登录...")
        submit_elems = driver.find_elements(By.TAG_NAME, "button")
        submit_elem = ""
        for elem in submit_elems:
            #print(elem.get_property("type"))
            #print(elem.get_attribute("class"))
            #print(elem.accessible_name)
            if elem.accessible_name == "登录":
                submit_elem = elem
        submit_elem.send_keys(Keys.ENTER)
        #判断是否登陆成功
        time.sleep(1)
        try:
            notchangepw_elem = driver.find_element(By.PARTIAL_LINK_TEXT, '暂时不更改')
            if(notchangepw_elem):
                notchangepw_elem.send_keys(Keys.ENTER)
        except:
            print("No need to change password")
    else:
        print("用户名或密码为空，在不登陆的情况下尝试下载。")

    return driver

def downloadImage(imglink, imgname, imagepagelink):
    print("正在下载: " + imglink)
    postfix = "." + imglink.split(".")[-1]
    savepath = "output\\"+ savefolder + imgname + postfix
    # 如果文件存在则跳過
    if(os.path.exists(savepath)):
        print("文件已存在，跳过")
        return
    #下载图片
    headers = {"Referer": imagepagelink}
    session = requests.Session()
    response = session.get(imglink, headers=headers)
    image_data = response.content
    #文件保存路径
    os.makedirs("output\\"+ savefolder , exist_ok=True)
    with open(savepath, 'wb') as f:
        f.write(image_data)
        print("文件保存成功")

def downloadMangaPages(imglinks, imgname, imagepagelink):
    #下载图片
    headers = {"Referer": imagepagelink}
    
    session = requests.Session()
    for imglink in imglinks:
        print("正在下载: " + imglink)
        #文件保存路径
        postfix = "." + imglink.split(".")[-1]
        pageNum = " "+imglink.split("_")[-2]
        os.makedirs("output\\"+ savefolder , exist_ok=True)
        savepath = "output\\"+ savefolder + imgname + pageNum + postfix
        # 如果文件存在则跳過
        if(os.path.exists(savepath)):
            print("文件已存在，跳过")
            continue
        #下载图片
        response = session.get(imglink, headers=headers)    
        image_data = response.content
        with open(savepath, 'wb') as f:
            f.write(image_data)
            print("文件保存成功")

def downLoadImageInPages(ranklinks, driver):
    for i in range(len(ranklinks)):
        print("加载排名页面: " + ranklinks[i])
        driver.get(ranklinks[i])
        #等待页面加载完毕，加载完毕的标志是图片展示出现
        global isLogin
        if isLogin:
            try:
                element_present = EC.presence_of_element_located((By.XPATH, "//*[@target ='_blank'][@rel='noopener']"))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                print("已登录，网页加载超时, 检查网络")
                continue
        else:
            try:
                elementNonlogin_present = EC.presence_of_element_located((By.XPATH, "//div[@role='presentation']/div/img"))
                WebDriverWait(driver, timeout).until(elementNonlogin_present)
            except TimeoutException:

                if driver.find_elements(By.XPATH, "//*[text() ='请登录pixiv账号以继续。']"):
                    print("敏感内容，未登录账号无法下载")
                else:
                    print("未登录，网页加载超时, 检查网络")
                continue
        
        #检查预览栏是否存在
        viewAllButton = driver.find_elements(By.XPATH, "//*[text() ='查看全部']")
        readWork = driver.find_elements(By.XPATH, "//*[text() ='阅读作品']")
        if(viewAllButton):
            print("此项为图集,只下载缩略图")
            #获取图片数量
            #pagesNum = int(previewlabel[0].find_element(By.TAG_NAME, "div").find_element(By.TAG_NAME, "span").get_attribute('innerHTML').split("/")[1])
            #viewAll_elem = driver.find_element(By.XPATH, "//*[text() ='查看全部']")
            #获得图片链接 非原始图片
            if isLogin:
                presentation = driver.find_element(By.XPATH, "//*[@target ='_blank'][@rel='noopener']")
            else:
                presentation = driver.find_element(By.XPATH, "//*[text() ='查看全部']")
            ActionChains(driver)\
                .click(presentation)\
                .perform()
            time.sleep(1)
            #向下滚动，载入所有页面
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if isLogin:
                manga_pages = driver.find_elements(By.XPATH, "//*[@target ='_blank'][@rel='noopener']/img")
            else:
                manga_pages = driver.find_elements(By.XPATH, "//div[@role='presentation']/div/img")
            imgname = manga_pages[0].accessible_name
            imgname = "".join( x for x in imgname if (x.isalnum() or x in "._- "))
            imglinks = []
            for page in manga_pages:
                imglinks.append(page.get_attribute("src"))
            
            print("图集有" + str(len(imglinks))+ "页，开始下载...")
            downloadMangaPages(imglinks, imgname, ranklinks[i])
        elif(readWork):
            print("此项为漫画作品")
            
            #获得图片链接 非原始图片
            if isLogin:
                presentation = driver.find_element(By.XPATH, "//*[@target ='_blank'][@rel='noopener']")
            else:
                presentation = driver.find_element(By.XPATH, "//*[text() ='阅读作品']")
            ActionChains(driver)\
                .click(presentation)\
                .perform()
            time.sleep(1)
            #向下滚动，载入所有页面
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
            if isLogin:
                manga_pages = driver.find_elements(By.XPATH, "//*[@target ='_blank'][@rel='noopener']/img")
            else:
                manga_pages = driver.find_elements(By.XPATH, "//div[@class = 'gtm-expand-full-size-illust']/img")
            imgname = manga_pages[0].accessible_name
            imgname = "".join( x for x in imgname if (x.isalnum() or x in "._- "))
            imglinks = []
            for page in manga_pages:
                imglinks.append(page.get_attribute("src"))
            
            print("图集有" + str(len(imglinks))+ "页，开始下载...")
            downloadMangaPages(imglinks, imgname, ranklinks[i])
            
        else:
            print("此项为单图")
            #若登录成功，则下载原图，未登录则下载预览图
            if isLogin:
                presentation = driver.find_element(By.XPATH, "//*[@target ='_blank'][@rel='noopener']")
                ActionChains(driver)\
                    .click(presentation)\
                    .perform()
                O_image = driver.find_element(By.XPATH, "//div[@role='presentation']/div/div/div/img")
            else:
                O_image = driver.find_element(By.XPATH, "//div[@role='presentation']/div/img")
            imglink = O_image.get_attribute("src")
            imgname = O_image.accessible_name
            imgname = "".join( x for x in imgname if (x.isalnum() or x in "._- "))
            print("开始下载...")
            downloadImage(imglink, imgname, ranklinks[i])


#driver = LoginPixiv()
def downloadRank100(driver):
    driver.get("https://www.pixiv.net/ranking.php")
    time.sleep(1)
    #向下滚动
    for i in range(1):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

    notification = driver.find_elements(By.XPATH, "//button[@title='通知']")
    global isLogin
    if notification:
        isLogin = True
        print("检测到登录正常")
    else:
        isLogin = False
        print("未检测到登录，以未登录模式下载")

    sections = driver.find_elements(By.TAG_NAME, "section")
    ranks = []
    for sect in sections:
        if sect.get_attribute("class") == "ranking-item":
            ranks.append(sect)
    print(len(ranks))

    #store the image links
    ranklinks = []
    for i in range(len(ranks)):
        id = ranks[i].get_attribute("data-id")
        imagepagelink = baselink + "artworks/" +str(id)
        ranklinks.append(imagepagelink)

    downLoadImageInPages(ranklinks, driver)

if __name__ == "__main__":
    print("这是一个用来爬取Pixiv图片的脚本。需要提供Pixiv账号和密码。\n频繁使用可能导致IP被BAN，请谨慎使用：")
    print("----------------------------------------------")
    driver = LoginPixiv()
    while True:
        print("----------------------------------------------")
        choice = input("选择下载内容：\n     1,下载今天排行榜前100图片\n     2,下载指定画师的图片（TBD）\n   选项:")
        if choice == "1":
            print("开始下载今天排行榜前100图片")
            downloadRank100(driver)
        elif choice == "2":
            print("此功能暂未开发")
            #print("开始下载指定画师的图片")
        else:
            print("输入错误，退出")
            time.sleep(5)
            exit()
