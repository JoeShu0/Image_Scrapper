#Simple multithread downloadtest
import os, shutil,time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

BaseLink = "https://gelbooru.com/index.php"
tagPreString = "?page=post&s=list&tags="
pagePreString = "&pid="
tagstring = ""

downloadInterval = 10 #Avoid being banned

def GetPageSoup(page_link, base_link):
    page = requests.get(base_link + page_link)
    return BeautifulSoup(page.content, features="html.parser")

def GetSearchPostString(tags):
    global tagstring
    tags_list = tags.split(" ") #tags 
    searchPost_string = tagPreString
    for tag in tags_list:
        searchPost_string = searchPost_string + tag + "+"
        tagstring = tagstring + "-" + tag 
    return searchPost_string

def GetAllPageString(searchPageSoup):
    page_ind_list = searchPageSoup.body.find(id="paginator").find_all("a")
    if not page_ind_list:
        return []

    max_ind_num = 0
    max_ind_link = ""
    for page_ind in page_ind_list:
        if page_ind.string == "»":
            max_ind_link = page_ind.get("href")
            break
        elif page_ind.string == "›" or page_ind.string == "‹" or page_ind.string == "«" :
            continue
        page_num = int(page_ind.string)
        if page_num > max_ind_num:
            max_ind_num = page_num
            max_ind_link = page_ind.get("href")
    
    max_page_index = int(max_ind_link.split(pagePreString)[-1])
    page_count = int(max_page_index / 42 + 1) #42 是gelbooru，每页的图片数量
    page_strings = []
    for i in range(page_count):
        page_strings.append(pagePreString + str(i * 42))
        
    return page_strings

def GetAllThumbSoupInPage(page_string, base_link):
    page_soup = GetPageSoup(page_string, base_link)
    image_thumbs = page_soup.body.find("div", {"class": "thumbnail-container"}).find_all("article", {"class": "thumbnail-preview"})
    return image_thumbs

def downloadImage(image_thumb_soup):
    #gather all infos
    image_page_link = image_thumb_soup.a.get("href")
    image_id = image_thumb_soup.a.get("id")
    image_tags = image_thumb_soup.img.get("alt").split("|")[-1]
    print("开始下载图片: " + image_id)
    #get to the image page
    image_page_soup = GetPageSoup(image_page_link,"")
    image_link = image_page_soup.body.find(rel="noopener").get("href")
    #make sure path exist
    global tagstring
    outputfolder = "output"+ tagstring
    os.makedirs(outputfolder, exist_ok=True)
    #download image
    postfix = image_link.split(".")[-1]
    response = requests.get(image_link, stream=True)
    image_file_path = os.path.join(outputfolder, image_id+'.'+postfix)
    with open(image_file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
    #write tags
    tag_file_path = os.path.join(outputfolder, image_id+".txt")
    with open(tag_file_path, "w") as text_file:
        text_file.write(image_tags)


def DownLoadByTags():
    input_tags = input("请输入gelbooru的tag, 用空格隔开: ")
    search_post_string = GetSearchPostString(input_tags)
    #print("Search String is: " + search_post_string)
    search_result_page_soup = GetPageSoup(search_post_string, BaseLink)
    page_strings = GetAllPageString(search_result_page_soup)

    if len(page_strings) == 0:
        print("此tag的图片过少，请检查tag！")
        return 

    print("一共有 " + str(len(page_strings)) + " 页, 全部下载预计将会花费 " + str(len(page_strings)*42 * 5/60) + " 分钟")
    comfirm_downlod = input("你确定要下载所有图片?(y/n):")
    
    if comfirm_downlod == "y" or comfirm_downlod == "Y":
        print("下载开始")
        pool = ThreadPoolExecutor()

        image_thumb_soups = []
        for page_string in page_strings:
            page_thumb_soups = GetAllThumbSoupInPage(search_post_string+page_string, BaseLink)
            results = pool.map(downloadImage, page_thumb_soups)
            time.sleep(downloadInterval)
            #for pts in page_thumb_soups:
                #mage_thumb_soups.append(pts)
            #break

        #print("Total " + str(len(image_thumb_soups)) + " images")
        
        #results = pool.map(downloadImage, image_thumb_soups)
        #future = pool.submit(downloadImage, image_thumb_soups[0])
        #for res in results:
            #print(res) # print results as they become available

        pool.shutdown()
    
    else:
        limited_downlod_num = int(input("你想要下载多少张图片?(int):"))

        if limited_downlod_num == 0:
            return

        print("下载开始")
        pool = ThreadPoolExecutor()
        download_counter = 0
        image_thumb_soups = []
        for page_string in page_strings:
            page_thumb_soups = GetAllThumbSoupInPage(search_post_string+page_string, BaseLink)
            results = pool.map(downloadImage, page_thumb_soups)
            time.sleep(downloadInterval)
            download_counter += len(page_thumb_soups)
            
            if download_counter > limited_downlod_num:
                break

        pool.shutdown()

    print("下载完毕")



if __name__ == "__main__":
    print("这是一个用来爬取gelbooru图片和tag的脚本。频繁使用可能导致IP被BAN，请谨慎使用：）")
    while(True):
        DownLoadByTags()