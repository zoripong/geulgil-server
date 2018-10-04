import urllib
from urllib.parse import quote
from bs4 import BeautifulSoup
from geulgil import db
from geulgil.models import *
from konlpy.tag import Twitter

import requests
import config


# [ 데이터베이스에서 새로운 단어를 추가 저장함 ]
def save_new_word(word):
    saemmul_data = get_saemmul_words(word)
    similar_data = get_similar_words(word, saemmul_data['mean'])
    mean_data = get_word_in_mean(saemmul_data['mean'])

    # Word
    word = Word(word=word, part=0)
    db.session.add(word)

    words = Word.query.filter(Word.word == word).all()
    word_id = words[0].id

    # Mean
    mean = Mean(word_id=word_id, mean=saemmul_data['mean'])
    db.session.add(mean)

    # MeanKeyword
    for mean in mean_data:
        mean_keyword = MeanKeyword(word_id=word_id, mean_keyword=mean)
        db.session.add(mean_keyword)

    # SimilarKeyword
    for similar in similar_data:
        similar_keyword = SimilarKeyword(word_id=word_id, similar_keyword=similar)
        db.session.add(similar_keyword)

    db.session.commit()


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


# [ 의미에서 단어가져오기 ]
def get_word_in_mean(mean):
    return Twitter().nouns(mean)
