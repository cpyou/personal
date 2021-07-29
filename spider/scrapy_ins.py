"""
运行命令：scrapy runspider scrapy_ins.py
"""
import scrapy
import time


class QdSpider(scrapy.Spider):
    name = 'qd'
    allowed_domains = ['qidian.com']
    start_urls = ['https://www.qidian.com/rank/yuepiao?style=1&page=1']

    def parse(self, response):
        start = time.time()  # 开始计时⏲

        books = response.xpath("//div[@class='book-img-text']/ul/li")

        for book in books:
            imglink = 'https:' + book.xpath("./div[1]/a/@href").extract_first()
            # 其它信息的xpath提取语句，......
            update = book.xpath("./div[2]/p[3]/a/text()").extract_first()
            # print(imglink, title, author, intro, update)
            print(imglink, update)

        end = time.time()  # 结束计时⏲

        print(end - start)

