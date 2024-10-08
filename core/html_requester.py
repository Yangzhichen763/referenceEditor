import os

import requests
from time import sleep


# User_Agent 可以按照自己浏览器中的表头修改，开发者模式（F12）-> 网络（Network） -> 任意点击一个请求 -> 查看标头（Headers）
# Cookie 很重要，相当于个人喜好，大数据（一个经常看论文的人更容易搜到论文）
request_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
}


def get_page_content(url: str, headers: dict = None, max_retry_times: int = 3):
    """
    获取网页的 html 内容
    """
    if headers is None:
        headers = request_headers
        # 读取 Cookies.txt 文件，设置 headers
        if os.path.exists("Cookie"):
            with open("Cookie", "r") as f:
                cookie = f.read()
                headers["Cookie"] = cookie

    retry_times = 0
    while retry_times <= max_retry_times:
        try:
            response = requests.get(url=url, headers=headers)   # 通过 url 获取网页相应
            response.raise_for_status()                         # 检查相应状态码
            content = response.text                             # 获取网页内容
            if retry_times > 0:
                print(f"\r获取网页 {url} 内容成功！")
            return content
        except requests.exceptions.RequestException as e:
            print(f"\r({retry_times}) 获取网页内容失败：{e}，重试中...", end="")
            sleep(0.5)                                          # 重试间隔
            retry_times += 1

    return None
