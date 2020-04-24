'''
타이틀아이디
제목
작가
소개글
별점
키워드 (타입, 장르, 테마)
연령가
요일 (완결작은 null)
완결여부
'''
import requests
from bs4 import BeautifulSoup
import re
import json

type_and_genre = ['episode', 'omnibus', 'story', 'daily', 'comic', 'fantasy', 'action', 'drama', 'pure', 'sensibility', 'thrill', 'historical', 'sports']
days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']

BASE_ONE = 'https://comic.naver.com/webtoon/genre.nhn?genre=' #장르
BASE_TWO = 'https://comic.naver.com/webtoon/weekdayList.nhn?week=' #요일
BASE_THREE = 'https://comic.naver.com/webtoon/theme.nhn' #테마

webtoons = dict()

# 전체 웹툰 정보 수집 및 키워드 삽입
for keyword in type_and_genre:
    url = BASE_ONE+keyword
    res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    item_list = soup.select('div[class=list_area] > ul > li')

    for item in item_list:
        title_id = int(re.findall('\d+', item.find("dl").find("dt").a.get("href"))[0])
        if title_id in webtoons.keys():
            info_obj = webtoons[title_id]
        else:
            info_obj = {
                'title': item.find("dl").find("dt").a.get('title'),
                'author': item.find("dl").find("dd", "desc").text.replace('\n',''),
                'intro': '',
                'star': item.find("dl").find("div", "rating_type").find("strong").text,
                'keyword': [],
                'grade': '',
                'day': [],
                'complete': False
            }
            # 연령가
            if len(item.find("div", "thumb").find_all("span", "mark_adult_thumb"))>0:
                info_obj['grade'] = 'ADULT'
            else:
                info_obj['grade'] = 'NA' #해당없음

            # 완결웹툰
            if len(item.find("div", "thumb").find_all('img')) > 1:
                info_obj['complete'] = True
            
            # 딕셔너리에 추가
            webtoons[title_id] = info_obj
            
        # keyword 추가
        info_obj['keyword'].append(keyword)

# 요일 데이터 추가
for d in days:
    url = BASE_TWO+d
    res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})
    
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    item_list = soup.select('ul[class=img_list] > li')

    for item in item_list:  
        title_id = int(re.findall('\d+', item.find("dl").find("dt").a.get("href"))[0])    
        if title_id in webtoons.keys():
            webtoons[title_id]['day'].append(d)
        else:
            print(title_id)

# 키워드에 테마 추가
url = BASE_THREE
res = requests.get(url, headers={'User-Agent':'Mozilla/5.0'})

html = res.text
soup = BeautifulSoup(html, 'html.parser')
item_list = soup.find_all(attrs={'class': 'theme_list_area'})
eng_name_dict = {'브랜드웹툰':'brandtoon', '리메이크':'remake', '멀티플롯':'multi-plot', '스포츠':'sports'}

for item in item_list:  
    theme_name = eng_name_dict[item.find("h4").find("strong").text[1:-1]]
    toons = item.find("ul").find_all("li")
    for t in toons:
        title_id = int(re.findall('\d+', t.find("div", "thumb").a.get("href"))[0])
        if title_id in webtoons.keys():
            webtoons[title_id]['keyword'].append(theme_name)

# 브랜드웹툰은 장르 구분이 되어 있지 않음 / 추천에 포함시키려면 추가 크롤링 필요

# json 파일로 저장
with open('./data/webtoons.json', 'w', encoding='UTF-8-sig') as file:
     file.write(json.dumps(webtoons, ensure_ascii=False))