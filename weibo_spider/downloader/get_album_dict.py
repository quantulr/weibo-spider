import json
from math import ceil

import requests


def get_album_dict(uid, header):
    """获取该用户相册名称和相册id到字典album_dict."""
    album_dict = {}
    url = 'http://photo.weibo.com/albums/get_all?uid='+uid+'&page=1&count=20'
    resp = requests.get(url, headers=header).content.decode('utf-8')
    total = int(json.loads(resp)['data']['total'])
    total = ceil(total/20)
    for num in range(1, total+1):
        url = 'http://photo.weibo.com/albums/get_all?uid=' + \
            uid+'&page='+str(num)+'&count=20'
        resp = requests.get(url, headers=header).content.decode('utf-8')
        data = json.loads(resp)['data']['album_list']
        for item in data:
            album_dict[item['caption']] = item['album_id']

    #del album_dict["微博配图"]
    return album_dict
