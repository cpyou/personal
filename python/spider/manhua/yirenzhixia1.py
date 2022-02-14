# -*- coding: utf-8 -*-

import re
import requests
import os


def download(url, dir, file_name):
    print("开始下载图片：" + url + "\r\n")
    try:
        pic = requests.get(url, timeout=10)
        # 保存图片路径
        file_path = dir + '/' + file_name
        fp = open(file_path, 'wb')
        fp.write(pic.content)
        fp.close()
    except requests.exceptions.ConnectionError:
        print('图片无法下载')


if __name__ == '__main__':

    url = "https://m.36manga.com/manhua/yirenzhixia/4459693.html"  # 开始下载的页面
    homepage = "https://m.36mh.com/manhua/yirenzhixia/"  # 待下载漫画的首页
    save_dir = '/Users/chenpuyu/Desktop/yirenzhixia2'  # 存储文件夹
    os.system(f'mkdir -p {save_dir}')

    has_next = True
    while has_next:
        r = requests.get(url=url, allow_redirects=False)
        # assert r.status_code != 200, "请求页面失败"

        html = r.content.decode('utf-8')
        chapter = re.findall('一人之下</a>&gt;(.*?)</span>', html)[0]
        next_chapter_url = re.findall('<mip-link href="(.*?)">下一章</mip-link>', html)[0]
        picture_urls = re.findall('<mip-img src="(.*?)">', html)

        for i, picture_url in enumerate(picture_urls):
            picture_url = picture_url.replace('res.img.overseas-mall.com', 'res.img.spt1311.com')
            file_name = f'{chapter}-{i}.jpg'
            print(file_name, ': ', picture_url)

            download(picture_url, save_dir, file_name)

        if next_chapter_url != homepage:
            url = next_chapter_url
        else:
            has_next = False
