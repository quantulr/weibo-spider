# weibo-spider

## 微博相册爬虫
首先分别运行以下命令来安装 PySide2，requests。

```bash
pip3 install requests
pip3 install PySide2
```

切换到 weibo-spider 文件夹中，运行命令`python3 main.py`(在 Windows 则为 `py main.py`)来使用。
使用前需要在浏览器打开网页 [http://photo.weibo.com/1642909335](http://photo.weibo.com/1642909335) ，按提示登录微博，按 F12 或 Ctrl+Shift+C 打开开发者工具，点击网络选项卡，点击 XHR 按钮，然后点击该网络请求，复制 cookie 到 cookie.json 文件中的相应位置。
![图片.png](https://i.loli.net/2019/09/06/6b2qIQNjYDsTWZV.png)
