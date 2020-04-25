'''
시간대
순위
타이틀아이디
회차이름
구분기준 (인기순/업데이트순)
'''

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import time

BASE_URL = 'https://comic.naver.com/index.nhn'
columns = ['timeline', 'rank', 'title_id', 'episode', 'sort_type'] 
data = []

now = time.localtime()
now_format = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

url = BASE_URL
res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
html = res.text
soup = BeautifulSoup(html, 'html.parser')
favorite= soup.select('ol[id=realTimeRankFavorite] > li') #인기순
update= soup.select('ol[id=realTimeRankUpdate] > li') #업데이트순

idx = 1
for f in favorite:
    tmp = f.find("a").get("title").split('-')
    title_id = int(re.findall('\d+', f.find("a").get("href").split('&')[0])[0])
    episode = "".join(tmp[1:])
    data.append([now_format, idx, title_id, episode, 'favorite'])
    idx += 1

idx = 1
for u in update:
    tmp = u.find("a").get("title").split('-')
    title_id = int(re.findall('\d+', f.find("a").get("href").split('&')[0])[0])
    episode = ''.join(tmp[1:])
    data.append([now_format, idx, title_id, episode, 'update'])
    idx += 1

df = pd.DataFrame(data, columns = columns) 
df.to_csv('./data/popular.csv',encoding='euc-kr')