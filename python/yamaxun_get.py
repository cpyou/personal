# -*- coding: utf-8 -*-
import requests
import re
import sys

from BeautifulSoup import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


url = 'https://www.amazon.cn/gp/bestsellers'
r = requests.get(url)
soup = BeautifulSoup(r.content)
assert isinstance(soup.find, object)
categories = soup.findAll(attrs={'class': re.compile('zg_homeWidget$')})
for c in categories:
    print c.find('h3').text
    for item in c.findAll(attrs={'class': re.compile('zg_homeWidgetItem$')}):
        print item.find(attrs={'class': re.compile('zg_rank$')}).text
        print item.find('img').get('alt')
        try:
            print item.find(attrs={'class': re.compile('a-icon-row a-spacing-none$')}).find('a').get('title')
        except:
            pass

print '完成'
