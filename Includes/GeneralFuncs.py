import os
import json
import shutil
import time
import requests
import sys

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