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




class PinterestWebSpider:
    def __init__(self, **config):
        '''

        :param config: a dict must contain the following keys:url, username, password
        '''
        self.config = config
        self.max_pages = 20 if config.get("max_pages", None) is None else config.get("max_pages")
        self.orginal_urls = set() # use set to avoid duplicate urls
        self.session_config = config.get("session_config", None)

        self.driver = self.intialize_chrome_driver()

    def intialize_chrome_driver(self):
        '''
        open the web page and login
        :return: web page handler --driver
        '''
        if not self.session_config:
            options = ChromeOptions()
            config_options = self.config.get("options", None)
            if config_options is not None:
                for option in config_options:
                    options.add_argument(option)
            driver = webdriver.Chrome('chromedriver.exe', options=options)
            driver = self.get_web(driver, self.config.get("url"))
            driver = self.login(driver, self.config.get("username"), self.config.get("password"))

            remote_execute_url = driver.command_executor._url
            session_id = driver.session_id
            self.session_config = {"remote_execute_url": remote_execute_url, "session_id": session_id}

            self.config["session_config"] = self.session_config
            with open("./config.json", "w") as f:
                json.dump(self.config, f)


        else:
            driver = webdriver.Chrome()
            driver = webdriver.Remote(command_executor=self.session_config.get("remote_execute_url"), desired_capabilities={})
            driver.session_id = self.session_config.get("session_id")

        return driver

    def get_web(self, driver, url):
        driver.get(url)
        time.sleep(3)
        return driver

    def login(self, driver, username, password):
        # click login
        header_elements = driver.find_elements(by=By.XPATH, value='//div[@data-test-id="unauth-header"]/div//button')
        for element in header_elements:
            if element.text == '登录':
                login_element = element
                login_element.click()
                break

        # time sleep for loading login dialog opening
        time.sleep(5)

        # send username and keywords
        username_element = driver.find_elements(by=By.XPATH, value='//input[@type="email"]')[0]
        password_element = driver.find_elements(by=By.XPATH, value='//input[@type="password"]')[0]
        login_button = driver.find_elements(by=By.XPATH,
                                            value='//div[@data-test-id="registerFormSubmitButton"]/button')[0]

        username_element.send_keys(username)
        password_element.send_keys(password)
        login_button.click()

        # must sleep to wait for the login dialog closing
        time.sleep(5)

        return driver

    def get_query_urls(self, query, deviation=2):
        search_element = self.driver.find_elements(by=By.XPATH, value='//input[@name="searchBoxInput"]')[0]
        prompts = len(search_element.get_attribute("value")) + deviation
        search_element.send_keys(Keys.BACKSPACE * prompts)
        search_element.send_keys(query)
        search_element.send_keys(Keys.ENTER)

        time.sleep(5) # must sleep to wait for the search results loading

        orignal_urls = set() # use set to avoid duplicate urls
        # get all searching results within the max_pages
        retry_times = self.config.get("retry_times", 3)
        urls_length = len(orignal_urls) # to check if the urls length is changed

        for page_idx in range(1, self.max_pages):
            try:
                page_elements = self.driver.find_elements(By.XPATH, '//div[@data-test-id="non-story-pin-image"]/div/img')
                for img_element in page_elements:
                    img_url = img_element.get_attribute("src")
                    original_url = img_url.replace('236x', 'originals')
                    orignal_urls.add(original_url)

            except Exception as e:
                if retry_times > 0:
                    print(f'Error for page {page_idx}: {e}, maybe sleep time is not enough, increase the sleep time and try again')
                    time.sleep(5)
                    retry_times -= 1
                    continue
                else:
                    print(f'Error for page {page_idx}: {e}, retry times is 0, stop the searching, please check the error')
                    break

            if urls_length == len(orignal_urls):
                print(f'No more images for query {query} until page {page_idx}, stop the searching')
                return orignal_urls

            urls_length = len(orignal_urls)

            # logging, TODO: import the logging module to record the log
            print('-*-' * 20)
            print(f'page {page_idx} has {urls_length} images')
            print('-*-' * 20)

            # scroll to next page
            #self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # TODO : need to be validated
            self.driver.execute_script(f"window.scrollTo({page_idx * self.config.get('page_scroll_length')}, "
                                       f"{ page_idx * self.config.get('page_scroll_length')});")

            time.sleep(10) # must sleep to wait for the next page loading

        return orignal_urls

    def save_urls(self, urls, file_name, path='./urls'):
        if not os.path.exists(path):
            os.makedirs(path)

        with open(os.path.join(path, file_name), 'a+') as f:
            f.write('\n'.join(urls))

    def download_image_by_url(self, url, file_name, path='./images'):
        # TODO 断点续传
        if not os.path.exists(path):
            os.makedirs(path)


        total_size, url = self.get_response_size(url)

        file_name = file_name + '.' + url.split('.')[-1]

        temp_size = os.path.getsize(os.path.join(path, file_name)) if os.path.exists(os.path.join(path, file_name)) else 0
        if temp_size == total_size:
            print(f'image {file_name} already exists, skip')
            return
        elif temp_size > 0:
            print(f'resume the image {file_name} downloading, total size is {total_size} bytes, current size is {temp_size} bytes')

        else:
            print(f'start to download the image {file_name}, total size is {total_size} bytes')


        headers = {'Range': f'bytes={temp_size}-{total_size}',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.95 Safari/537.36',
                   }
        resume_response = requests.get(url, stream=True, timeout=10, headers=headers)

        with open(os.path.join(path, file_name), 'ab') as f:
            for chunk in resume_response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    temp_size += len(chunk)

        return url


    def get_response_size(self, url):

        total_size = 0
        for idx, extend_format in enumerate(self.config['image_formats']):
            if idx > 0:
                url = url.replace(self.config['image_formats'][idx - 1], extend_format)

            try:
                response = requests.get(url, stream=True, timeout=10)
                total_size = int(response.headers.get('content-length'))
            except Exception as e:
                print(f'Error for image {url} with Exception: {e}, try to download other format')
                continue

            if total_size < 300:
                print(f'Error for image {url}, the size is {total_size}, try to download other format')
                continue
            else:
                return total_size, url

        return total_size, url



    def download_images(self, queries):
        for query in queries:
            urls = self.get_query_urls(query)

            print('---' * 20)
            print(f'Found {len(urls)} images for query {query}')
            print('---' * 20)

            if self.config.get("images_path", None) != None:
                urls = list(urls)
                for idx, url in enumerate(urls):
                    right_url = self.download_image_by_url(url, f'{query}_{idx}', self.config.get("images_path"))
                    if right_url != url:
                        urls[idx] = right_url

            if self.config.get("urls_path", None) != None:
                self.save_urls(urls, f'{query}.txt', self.config.get("urls_path"))











if __name__ == '__main__':
    config = {
        "url": "https://www.pinterest.com/",
        "username": "yanxiangly@gmail.com",
        "password": "xy545733",
        "max_pages": 10,
        "retry_times": 3,
        "page_scroll_length": 1000,
        "urls_path": "./驯龙高手_1/urls",
        "images_path": "./驯龙高手_1/images",
        "image_formats": ["jpg", "png", "gif", "jpeg"],
        "options": ["--start-maximized"]
    }
    # sys.argv[1] = './config.json'

    queries = ['Hiccup', 'Astrid', 'Valka', 'Fishlegs']
    # config = json.load(open(sys.argv[1] if len(sys.argv) > 1 else './config.json', 'r'))
    pinterest = PinterestWebSpider(**config)
    pinterest.download_images(queries)





