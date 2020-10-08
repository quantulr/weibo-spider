import json
import os


def parse_config():
    """read config"""
    if os.path.exists(os.path.expandvars('$HOME') + '/.config/weibo-spider/config.json'):
        with open(os.path.expandvars('$HOME') + '/.config/weibo-spider/config.json', "r") as conf:
            header_settings = json.load(conf)
            user_agent = header_settings["user_agent"]
            cookie = header_settings["cookie"]
        header = {
            "User-Agent": user_agent,
            "Cookie": cookie
        }
    else:
        os.mkdir(os.path.expandvars('$HOME') +
                 '/.config/weibo-spider')
        with open(os.path.expandvars('$HOME') + '/.config/weibo-spider/config.json', 'w') as conf:
            conf.write("{}")
        print("No configuration found")
        exit
    return header
