import os
import sys

from . import downloader

# import downloader

def test():
    uid = '2330621952'
    header = downloader.parse_config()
    print(header, uid)
    print(downloader.get_album_dict(uid, header))

def main():
    header = downloader.parse_config()
    url = sys.argv[1]
    path = sys.argv[2]
    uid = downloader.get_uid(url)
    user_name = downloader.get_username(uid, header)
    album_dict = downloader.get_album_dict(uid, header)
    try:
        os.mkdir(os.path.expandvars('$HOME')+'/'+path+'/'+user_name)
        os.chdir(os.path.expandvars('$HOME')+'/'+path+'/'+user_name)
    except FileExistsError:
        os.chdir(os.path.expandvars('$HOME')+'/'+path+'/'+user_name)
    for album_name, album_id in album_dict.items():
        downloader.download_album(uid, album_name, album_id, header)

if __name__ == "__main__":
    main()
