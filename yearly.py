'''
연도
제목
타이틀아이디
'''
import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

BASE_URL = 'https://comic.naver.com/webtoon/period.nhn?period='
years = [str(i) for i in range(2005,2021)]

data = []

for year in years:
    url = BASE_URL+year
    res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    item_list = soup.select('ul[class=img_list] > li > dl > dt')

    for item in item_list:
        row = [int(year), item.text, re.findall('\d+', item.a.get('href'))[0]]
        data.append(row)

df = pd.DataFrame(data, columns = ['year', 'title', 'title_id']) 
df.to_csv('./data/yearly.csv',encoding='euc-kr')