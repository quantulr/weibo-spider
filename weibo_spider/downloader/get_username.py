import json

import requests


def get_username(uid, header):
    """获取并返回用户名"""
    url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value='+uid
    resp = requests.get(url, headers=header).content.decode('utf-8')
    user_fold_name = json.loads(resp)['data']['userInfo']['screen_name']
    return user_fold_name
