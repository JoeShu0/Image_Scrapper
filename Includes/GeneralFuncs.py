import os
import json
import shutil
import time
import requests
import sys

#For Faking Header
def downloadImageData(session, imglink, headers):
    retries = 1
    success = False
    while not success and retries < 5:
        try:
            response = session.get(imglink, headers=headers)
            success = True
        except Exception as e:
            wait = retries * 10
            print ('Error! Waiting {} secs and re-trying...'.format(wait))
            time.sleep(wait)
            retries += 1
    return response

def downloadImageToDisk(session, imglink, headers, savepath):
    retries = 1
    success = False
    while not success and retries < 5:
        try:
            response = session.get(imglink, headers=headers)
            success = True
        except Exception as e:
            wait = retries * 10
            print ('Error! Waiting {} secs and re-trying...'.format(wait))
            time.sleep(wait)
            retries += 1
    image_data = response.content
    with open(savepath, 'wb') as f:
        f.write(image_data)
        print("文件保存成功")

def downloadImageToDiskBase(imglink, savepath):
    retries = 1
    success = False
    while not success and retries < 5:
        try:
            response = requests.get(imglink)
            success = True
        except Exception as e:
            wait = retries * 10
            print ('Error! Waiting {} secs and re-trying...'.format(wait))
            time.sleep(wait)
            retries += 1
    image_data = response.content
    with open(savepath, 'wb') as f:
        f.write(image_data)
        print("文件保存成功")

def get_response_size(url):
    total_size = 0
    print(url)
    response = requests.get(url, stream=True, timeout=10)
    total_size = int(response.headers.get('content-length'))
    if total_size < 300:
        print(f'Error for image {url}, the size is {total_size}')
    return total_size, url


def download_image_by_url(file_name, url, path='./images'):
    # TODO 断点续传
    if not os.path.exists(path):
        os.makedirs(path)

    try:
        total_size, url = get_response_size(url)
    except:
        print("Failed to get size for: {file_name}, skipping!")

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