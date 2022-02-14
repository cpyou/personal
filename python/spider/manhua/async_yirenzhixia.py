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

class ManhuaSpider():

    def __init__(self):
        self.homepage = "https://m.36mh.com/manhua/yirenzhixia/"
        self.save_dir = '/Users/chenpuyu/Desktop/yirenzhixia'
    
    @staticmethod
    def trans_http_to_https(url):
        if 'https' not in url:
            url = url.replace('http', 'https')
        return url

    def get_all_chapter_urls(self):
        homepage = self.homepage
        r = requests.get(url=homepage, allow_redirects=False)
        re_str = '</li>\n\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t<li>\n                                                                            <a href="(.*?)"\n'
        return re.findall(re_str, r.content.decode('utf-8'))

    async def get_chapter_page_urls(self, url):
        url = self.trans_http_to_https(url)
        homepage = self.homepage
        print(f'章节url：{url}')
        chapter_no = re.findall(f'{homepage}(.*?).html', url)[0]
        r = requests.get(url=url, allow_redirects=False)
        html = r.content.decode('utf-8')
        title = re.findall('一人之下</a>&gt;(.*?)</span>', html)[0]
        k_page = re.findall('<span id="k_page" class="curPage">(.*?)</span>', html)[0]
        k_total = re.findall('<span id="k_total" class="curPage">(.*?)</span>', html)[0]

        first_picture_url = re.findall('<mip-img src="(.*?)">', html)[0]
        await download(first_picture_url, self.save_dir, file_name=f'{title}-1.jpg')

        for i in range(2, int(k_total) + 1):
            page_url = f'{homepage}{chapter_no}-{i}.html'
            print(f'页面url：{page_url}')
            file_name = f'{title}-{i}.jpg'
            await self.save_chapter_page_image(page_url, file_name)
        return True

    async def save_chapter_page_image(self, page_url, file_name):
        r = requests.get(url=page_url, allow_redirects=False)
        html = r.content.decode('utf-8')
        picture_url = re.findall('<mip-img src="(.*?)">', html)[0]
        await download(picture_url, self.save_dir, file_name)

    async def run(self):
        all_chapter_urls = self.get_all_chapter_urls()
        tasks = []
        for chapter_url in all_chapter_urls:
            tasks.append(asyncio.create_task(self.get_chapter_page_urls(chapter_url)))
        for task in tasks:
            await task

    def produce_run(self, c):
        all_chapter_urls = self.get_all_chapter_urls()
        c.send(None)
        for chapter_url in all_chapter_urls:
            r = c.send(chapter_url)
        c.close()

def consumer():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print(f'参数{n}')
        asyncio.run(ManhuaSpider().get_chapter_page_urls(n))
        r = '200 OK'

def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()

if __name__ == '__main__':
    asyncio.run(ManhuaSpider().run())
    # c = consumer()
    # ManhuaSpider().produce_run(c)

