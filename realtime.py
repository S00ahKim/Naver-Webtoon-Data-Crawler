'''
시간대
순위
타이틀아이디
연령대
성별
'''

import requests
import re
import pandas as pd
import json
import time

BASE_URL = 'https://comic.naver.com/recommandWebtoonRank.nhn?m=list&ageGroup='
ages = ['W10', 'W20', 'W30', 'M10', 'M20', 'M30']

now = time.localtime()
now_format = "%04d-%02d-%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

columns = ['timeline', 'rank', 'title_id', 'age', 'gender'] 
data = []

for age in ages:
    url = BASE_URL + age
    res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'}).text
    info = json.loads(res)
    gender = age[0]
    age = int(age[1:])
    for item in info['list']:
        data.append([now_format, item['rank'], item['titleId'], age, gender])

df = pd.DataFrame(data, columns = columns) 
df.to_csv('./data/realtime.csv',encoding='euc-kr')