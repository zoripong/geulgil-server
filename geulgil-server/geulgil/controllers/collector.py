import collections
import urllib
from urllib.parse import quote
from bs4 import BeautifulSoup
from geulgil import db
from geulgil.models import *
from konlpy.tag import Twitter #Window용
from konlpy.tag import Komoran

import requests
import config


# TODO
# [ 데이터베이스에서 새로운 단어를 추가 저장함 ]
def save_new_word(word):
    # 만약 있는 단어일 경우 의미만 추가
    # 없는 단어일 경우 word에도 추가 mean에도 추가


    db.session.commit()
    return ''


# [ 샘물 api에서 국어사전 정보 가져옴 ]
def get_saemmul_words(word):
    # api 요청키 및 url
    url = config.SAEMMUL_API['url'] + "?key=" + config.SAEMMUL_API['key'] \
          + "&q=" + quote(word) + "&num=10" + "&advanced=y" \
          + "&target=1" + "&method=exact"

    # header 정보 추가
    headers = {
        'User-Agent': config.HEADER_USER_AGENT
    }

    # url 요청 및 오픈
    req = urllib.request.Request(url, headers=headers)
    data = urllib.request.urlopen(req).read()

    # BeautifulSoup 을 이용하여 파싱하기 위한 객체 생성
    xml = BeautifulSoup(data, "html.parser")
    dict_list = []

    # item 검색
    for item in xml.findAll('item'):
        sense = item.find('sense')  # 의미를 포함하는 <>
        xml_dict = {
            'word': item.find('word').text,
            'mean': sense.find('definition').text,
            'category': '',
            'part': ''
        }
        category = sense.find('cat')  # 카테고리
        if category is not None:
            xml_dict['category'] = category.text
        else:
            xml_dict['category'] = None
        pos = sense.find('pos')  # 품사
        if pos is not None:
            xml_dict['part'] = pos.text
        else:
            xml_dict['part'] = None
        dict_list.append(xml_dict)
    return dict_list  # type list of dict

'''
[OrderedDict([('word', '유리'), ('mean', '‘노을’의 방언'), ('category', None), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '‘우박’의 방언'), ('category', None), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '‘나리꽃’의 방언'), ('category', None), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '조선 시대에, 각 지방 관아의 이방(吏房)에 속하여 인사ㆍ비서(\u7955書) 따위에 관한 일을 맡아보던 구실아치.'), ('category', '역사'), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '이익이 있음.'), ('category', None), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '유리 연산 이외의 관계를 포함하지 않는 일.'), ('category', '수학'), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '‘유리하다’의 어근.'), ('category', None), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '중 국 은나라 때의 감옥. 은나라의 주왕(紂王)이 주나라의 문왕(文王)을 가두었던 곳인데, 전하여 옥사(獄舍)나 뇌옥(牢獄)의 뜻으 로도 쓰인다.'), ('category', '역사'), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '일정한 집과 직업이 없이  이곳저곳으로 떠돌아다님.'), ('category', None), ('part', '')]), OrderedDict([('word', '유리'), ('mean', '석영, 탄산 소다, 석회암을 섞어 높은 온도에서 녹인 다음 급히 냉각하여 만든 물질. 투명하고 단단하며 잘 깨진다.'), ('category', '화학'), ('part', '')])]
'''


# [ 네이버 사전에서 유사어 가져옴]
def get_similar_words(word, mean):
    url = config.DICT_URL + quote(word)
    req = requests.get(url)
    html = req.content

    soup = BeautifulSoup(html.decode('utf-8', 'replace'), 'html.parser')
    similar_list = list()
    for tag in soup.find_all('span', text=mean):
        for e in tag.parent.parent.parent.findAll('sup'):
            e.extract()
        for similar in tag.parent.parent.parent.findAll('a', 'syno'):
            similar_list.append(similar.text)
    return similar_list
'''
['정애', '친애', '하트']
'''


# [ 의미에서 단어가져오기 ]
def get_word_in_mean(mean):
    return Twitter().nouns(mean)
