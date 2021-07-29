import time
from selenium import webdriver

url = 'https://www.qidian.com/rank/yuepiao?style=1&page=1'

start = time.time()  # 开始计时⏲
driver = webdriver.Chrome()
driver.get(url)
books = driver.find_elements_by_xpath("//div[@class='book-img-text']/ul/li")

for book in books:
    imglink = 'https:' + book.find_element_by_xpath("./div[1]/a").get_attribute('href')
    # 其它小说信息的定位提取语句，...
    update = book.find_element_by_xpath("./div[2]/p[3]/a").text
    # print(imglink, title, author, intro, update)
    print(imglink, update)

end = time.time()  # 结束计时⏲

print(end - start)
# 18.564752340316772
