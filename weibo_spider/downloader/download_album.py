import json
import os
import subprocess
from math import ceil

import requests


def remove_repeat(pic_dict, album_name):
    """从字典pic_dict中删除已经下载的图片"""
    exist_file_list = os.listdir(album_name)
    for file_name in exist_file_list:
        try:
            del pic_dict[file_name]
        except KeyError:
            pass


def download(pic_name, pic_host):
    url = pic_host+'/large/'+pic_name
    download_process = subprocess.run("aria2c -c "+url, shell=True, check=True,
                                      capture_output=True, text=True, encoding="utf-8")
    if download_process.returncode != 0:
        raise NameError("下载出错！")


def download_album(uid, album_name, album_id, headers):
    pic_dict = {}

    try:
        os.mkdir(album_name)
    except FileExistsError:
        pass

    # 获取总页数
    url = 'http://photo.weibo.com/photos/get_all?uid=' + \
        uid+'&album_id='+album_id+'&count=32&page='
    if album_name == "微博配图":
        resp = requests.get(url+"1&type=3", headers=headers)
    elif album_name == "头像相册":
        resp = requests.get(url+"1&type=1", headers=headers)
    else:
        resp = requests.get(url+"1&type=1", headers=headers)
    total_pages = int(json.loads(
        resp.content.decode('utf-8'))['data']['total'])
    total_pages = ceil(total_pages/32)

    print("\n\n正在获取"+album_name+"中的图片。")
    for num in range(1, total_pages+1):
        if album_name == "微博配图":
            resp = requests.get(url+str(num)+'&type=3', headers=headers)
        elif album_name == "头像相册":
            resp = requests.get(url+str(num)+'&type=18', headers=headers)
        else:
            resp = requests.get(url+str(num)+'&type=1', headers=headers)
        temp = json.loads(resp.content.decode(
            'utf-8'))['data']['photo_list']
        print('第'+str(num)+'/'+str(total_pages)+'页共有'+str(len(temp))+'张照片！')
        for item in temp:
            pic_dict[item['pic_name']] = item['pic_host']

    remove_repeat(pic_dict, album_name)
    total_pics = len(pic_dict)
    remaining = total_pics
    print("共"+str(total_pics)+"项。")

    os.chdir(album_name)

    for pic_name, pic_host in pic_dict.items():
        download(pic_name, pic_host)
        remaining = remaining - 1
        print(pic_name+'			'+"还剩"+str(remaining)+'/'+str(total_pics)+"项。")
        pic_dict = {}
    os.chdir("..")
