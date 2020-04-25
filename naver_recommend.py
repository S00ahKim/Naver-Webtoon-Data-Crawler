'''
키워드(유형/장르)별 추천웹툰 - 네이버 메인에서 제공

키워드
추천타입 (조회순/별점순)
타이틀아이디
'''

import requests
import json
import re
import pandas as pd

BASE_URL = 'https://comic.naver.com/mainGenre.nhn?m=list&genre={keyword}&order={rec_type}'

columns = ['keyword', 'rec_type', 'title_id'] #rec_type은 추천 타입 (조회순/별점순)
data = []

keywords = ['episode', 'omnibus', 'story', 'daily', 'comic', 'fantasy', 'action', 'drama', 'pure', 'sensibility', 'thrill', 'historical', 'sports']
rec_types = ['StarScore', 'ViewCount']

for keyword in keywords:
    for rec_type in rec_types:
        url = BASE_URL.format(keyword=keyword, rec_type=rec_type)
        res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
        info = json.loads(res)
        for i in info['list']:
            tmp = [keyword, rec_type, i['titleId']]
            data.append(tmp)

df = pd.DataFrame(data, columns = columns) 
df.to_csv('./data/naver_recommned.csv',encoding='euc-kr')