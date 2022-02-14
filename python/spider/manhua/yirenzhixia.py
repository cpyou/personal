# -*- coding: utf-8 -*-

import re
import requests
import asyncio


async def download(url, dir, file_name):
    print("开始图片下载：" + url + "\r\n")
    try:
        pic = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        print('图片无法下载')

    # 保存图片路径
    file_path = dir + '/' + file_name
    with open(file_path, 'wb') as fp:
        fp.write(pic.content)
        print("完成图片下载：" + url + "\r\n")

async def main():
    url = "https://m.36manga.com/manhua/yirenzhixia/4459693.html" # 开始下载的页面
    homepage = "https://m.36manga.com/manhua/yirenzhixia/" # 待下载漫画的首页
    save_dir = '/Users/chenpuyu/Desktop/yirenzhixia' # 存储文件夹

    has_next = True
    while has_next:
        r = requests.get(url=url, allow_redirects=False)
        assert r.status_code == 200, "请求页面失败"

        html = r.content.decode('utf-8')
        title = re.findall('<title>一人之下(.*?)_免费阅读-36漫画网</title>', html)[0]
        next_page_url = re.findall('<mip-link href="(.*?)">下一页</mip-link>', html)[0]
        next_chapter_url = re.findall('<mip-link href="(.*?)">下一章</mip-link>', html)[0]
        picture_url = re.findall('<mip-img src="(.*?)">', html)[0]

        file_name = "{}_{}.jpg".format(url.lstrip("https://m.36manga.com.com/manhua/yirenzhixia/").rstrip('html'), title)
        print(file_name, ': ', picture_url)
        download(picture_url, save_dir, file_name)
        print(file_name, '2: ', picture_url)

        if next_page_url != homepage:
            url = next_page_url
        elif next_chapter_url != homepage:
            url = next_chapter_url
        else:
            has_next = False

if __name__ == '__main__':
    asyncio.run(main())
