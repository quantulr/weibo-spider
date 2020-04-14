import json
import os
import re
import subprocess
from math import ceil

import requests

# 从文件 "config.json" 中获取 cookie 和 User-Agent 信息，并添加到变量 header 中
with open("config.json", "r") as e:
    header_settings = json.load(e)
    user_agent = header_settings["user_agent"]
    cookie = header_settings["cookie"]
header = {
    "User-Agent": user_agent,
    "Cookie": cookie
}

def download(leftover, key, value):
    url = value+'/large/'+key
    # html = requests.get(url)
    # with open(key, 'wb') as img:
    # 	img.write(html.content)
    subprocess.run("aria2c -c "+url, shell=True)
    print(key+'			'+"还剩"+str(leftover-1)+"项。")

# 从字典pic_dict中删除已经存在的图片
def remove_repeat(pic_dict, fold_name):
    exist_file_list = os.listdir(fold_name)
    for x in exist_file_list:
        try:
            del pic_dict[x]
        except KeyError:
            pass


# 从输入中获取并返回 uid
def get_uid(url):
    uid = re.findall('[0-9]+', url)[0]
    return uid

# 获取并返回用户名


def get_username(uid):
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+uid
    html = requests.get(url, headers=header)
    user_fold_name = json.loads(html.content.decode(
        'utf-8'))['data']['userInfo']['screen_name']
    return user_fold_name

# 获取该用户相册名称和相册id到字典album_dict.


def get_album_dict(uid):
    album_dict = {}
    url = 'http://photo.weibo.com/albums/get_all?uid='+uid+'&page=1&count=20'
    html = requests.get(url, headers=header)
    total = int(json.loads(html.content.decode('utf-8'))['data']['total'])
    total = ceil(total/20)
    for num in range(1, total+1):
        url = 'http://photo.weibo.com/albums/get_all?uid=' + \
            uid+'&page='+str(num)+'&count=20'
        html = requests.get(url, headers=header)
        data = json.loads(html.content.decode('utf-8'))['data']['album_list']
        for x in data:
            album_dict[x['caption']] = x['album_id']

    #del album_dict["微博配图"]
    return album_dict

# 下载微博配图中的图片


def get_one(thread_obj):
    thread_obj.pathSignal.emit(thread_obj.username+'/')
    pic_dict = {}
    url = 'http://photo.weibo.com/photos/get_all?uid='+thread_obj.uid + \
        '&album_id='+thread_obj.album_dict['微博配图']+'&count=32&page='
    html = requests.get(url+'1&type=3', headers=header)
    total = int(json.loads(html.content.decode('utf-8'))['data']['total'])
    total = ceil(total/32)
    for num in range(1, total+1):
        html = requests.get(url+str(num)+'&type=3', headers=header)
        temp = json.loads(html.content.decode('utf-8'))['data']['photo_list']
        print('此页共有'+str(len(temp))+'张照片！')
        thread_obj.statusSignal.emit(
            '第'+str(num)+'/'+str(total)+'页共有'+str(len(temp))+'张照片！')
        for x in temp:
            pic_dict[x['pic_name']] = x['pic_host']
    os.chdir('..')
    remove_repeat(pic_dict, thread_obj.username)
    os.chdir(thread_obj.username)
    leftover = len(pic_dict)
    print("共"+str(leftover)+"项。")
    thread_obj.statusSignal.emit("共"+str(leftover)+"项。")
    pic_total = leftover
    for key, value in pic_dict.items():
        download(leftover, key, value)
        leftover = leftover - 1
        progressMessage = int(((pic_total-leftover)/pic_total)*100)
        thread_obj.statusSignal.emit(
            "还剩"+str(leftover)+"/"+str(pic_total)+"项。")
        thread_obj.progressSignal.emit(progressMessage)
        pic_dict = {}
    os.chdir('..')

# 下载所有相册图片


def get_all_pic(thread_obj):
    pic_dict = {}
    #pic_dic_all = {}
    for key, value in thread_obj.album_dict.items():
        fold_name = key
        try:
            os.mkdir(fold_name)
            # os.chdir(fold_name)
        except FileExistsError:
            # os.chdir(fold_name)
            pass

        url = 'http://photo.weibo.com/photos/get_all?uid=' + \
            thread_obj.uid+'&album_id='+value+'&count=32&page='
        if key == "微博配图":
            html = requests.get(url+"1&type=3", headers=header)
        elif key == "头像相册":
            html = requests.get(url+"1&type=1", headers=header)
        else:
            html = requests.get(url+"1&type=1", headers=header)
        total = int(json.loads(html.content.decode('utf-8'))['data']['total'])
        total = ceil(total/32)
        #piclist = []

        print("\n\n正在获取"+fold_name+"中的图片。")
        pathMessage = thread_obj.username+'/'+fold_name+'/'
        thread_obj.pathSignal.emit(pathMessage)
        for num in range(1, total+1):
            if key == "微博配图":
                html = requests.get(url+str(num)+'&type=3', headers=header)
            elif key == "头像相册":
                html = requests.get(url+str(num)+'&type=18', headers=header)
            else:
                html = requests.get(url+str(num)+'&type=1', headers=header)
            temp = json.loads(html.content.decode(
                'utf-8'))['data']['photo_list']
            print('第'+str(num)+'页共有'+str(len(temp))+'张照片！')
            thread_obj.statusSignal.emit(
                '第'+str(num)+'/'+str(total)+'页共有'+str(len(temp))+'张照片！')
            for x in temp:
                pic_dict[x['pic_name']] = x['pic_host']
        remove_repeat(pic_dict, fold_name)
        leftover = len(pic_dict)
        pic_total = leftover
        print("共"+str(leftover)+"项。")
        thread_obj.statusSignal.emit("共"+str(leftover)+"项。")
        for key, value in pic_dict.items():
            os.chdir(fold_name)
            download(leftover, key, value)
            leftover = leftover - 1
            progressMessage = int(((pic_total-leftover)/pic_total)*100)
            thread_obj.statusSignal.emit(
                "还剩"+str(leftover)+"/"+str(pic_total)+"项。")
            thread_obj.progressSignal.emit(progressMessage)
            pic_dict = {}
            os.chdir("..")
    os.chdir('..')
