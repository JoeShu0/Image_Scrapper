import requests
import re

# 定义登录页面的url
login_url = "https://accounts.pixiv.net/login"

# 定义请求头，模拟浏览器的行为
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
}

# 定义pixiv账号和密码，替换为你自己的
username = "your_username"
password = "your_password"

# 发送get请求，获取登录页面的html
response = requests.get(login_url, headers=headers)
html = response.text

# 使用正则表达式，从html中提取postkey
pattern = re.compile(r'name="post_key" value="(.*?)"')
postkey = pattern.search(html).group(1)

# 定义登录数据，包括账号、密码和postkey
data = {
    "pixiv_id": username,
    "password": password,
    "post_key": postkey
}

# 发送post请求，向登录接口发送登录数据
response = requests.post(login_url, data=data, headers=headers)

# 获取响应的cookies，用于保持登录状态
cookies = response.cookies

# 打印cookies，验证是否登录成功
print(cookies)


def logintopixiv():
        print("开始登录pixiv")
        global session
        session = requests.Session()
        login_url = "https://accounts.pixiv.net/login?lang=zh&source=pc&view_type=page&ref=wwwtop_accounts_index"
        login_page = session.get(login_url)
        login_page_soup = BeautifulSoup(login_page.text, "html.parser")
        post_key = login_page_soup.find("input", {"name": "post_key"}).get("value")
        login_data = {
            "pixiv_id": "your pixiv id",
            "password": "your pixiv password",
            "captcha": "",
            "g_recaptcha_response": "",
            "post_key": post_key,
            "source": "pc",
            "ref": "wwwtop_accounts_index",
            "return_to": "https://www.pixiv.net/"
        }
        session.post(login_url, data=login_data)
        print("登录成功")

def downloadImageFromPixiv(image_id):
    global session
    image_page_url = "https://www.pixiv.net/member_illust.php?mode=medium&illust_id=" + str(image_id)
    image_page = session.get(image_page_url)
    image_page_soup = BeautifulSoup(image_page.text, "html.parser")
    image_link = image_page_soup.find("img", {"class": "original-image"}).get("data-src")
    print("开始下载图片: " + str(image_id))
    #make sure path exist
    global tagstring
    outputfolder = "output\\"+ tagstring
    os.makedirs(outputfolder, exist_ok=True)
    #download image
    postfix = image_link.split(".")[-1]
    response = requests.get(image_link, stream=True)
    image_file_path = os.path.join(outputfolder, str(image_id)+'.'+postfix)
    with open(image_file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response

def logintopinterest():
    print("开始登录pinterest")
    global session
    session = requests.Session()
    login_url = "https://www.pinterest.com/login/"
    login_page = session.get(login_url)
    login_page_soup = BeautifulSoup(login_page.text, "html.parser")
    post_key = login_page_soup.find("input", {"name": "data"}).get("value")
    login_data = {
        "data": post_key,
        "options": '{"username_or_email":"your pinterest username","password":"your pinterest password"}'
    }
    session.post(login_url, data=login_data)
    print("登录成功")

def downloadImageFromPinterest(image_id):
    global session
    image_page_url = "https://www.pinterest.com/pin/" + str(image_id)
    image_page = session.get(image_page_url)
    image_page_soup = BeautifulSoup(image_page.text, "html.parser")
    image_link = image_page_soup.find("img", {"class": "GrowthUnauthPinImage__Image"}).get("src")
    print("开始下载图片: " + str(image_id))
    #make sure path exist
    global tagstring
    outputfolder = "output\\"+ tagstring
    os.makedirs(outputfolder, exist_ok=True)
    #download image
    postfix = image_link.split(".")[-1]
    response = requests.get(image_link, stream=True)
    image_file_path = os.path.join(outputfolder, str(image_id)+'.'+postfix)
    with open(image_file_path, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
