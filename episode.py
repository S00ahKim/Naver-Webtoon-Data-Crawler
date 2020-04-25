'''
타이틀아이디
회차번호
회차제목
등록일
별점
'''

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

LIST_URL = 'https://comic.naver.com/webtoon/list.nhn?titleId={title_id}&page={page_num}'
columns = ['title_id', 'episode_num', 'episode_title', 'updated_at', 'rating']
data = []

title_ids=['651673'] #유미의 세포들

def episode_crawler(title_id):
    idx = 1
    done = False
    while not done:
        url = LIST_URL.format(title_id=title_id, page_num=str(idx))
        res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
        html = res.text
        soup = BeautifulSoup(html, 'html.parser')
        item_list = soup.select('table[class=viewList] > tr')[2:]
        
        for item in item_list:
            info_obj = item.find("td").a.get('href').split('&')
            title_id = int(re.findall('\d+', info_obj[0])[0])
            episode_num = int(re.findall('\d+', info_obj[1])[0])
            episode_title = item.select('td[class=title]')[0].text.strip()
            updated_at = item.select('td[class=num]')[0].text
            rating = item.select('div[class=rating_type] > strong')[0].text
            tmp = [title_id, episode_num, episode_title, updated_at, rating]
            if tmp in data:
                done = True
            else:
                data.append(tmp)
        idx+=1
    df = pd.DataFrame(data, columns = columns) 
    df.to_csv('./data/episodes_{}.csv'.format(title_id),encoding='euc-kr')

for title_id in title_ids:
    episode_crawler(title_id)