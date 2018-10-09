import urllib
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from geulgil import db
from geulgil.models import *
from konlpy.tag import Twitter

import config


# [ 데이터베이스에서 새로운 단어를 추가 저장함 ]
def save_new_word(word):
    saemmul_data = get_saemmul_words(word)

    # Word
    word_item = Word(word=word, part=0)
    db.session.add(word_item)

    words = Word.query.filter(Word.word == word).all()
    word_id = words[0].id

    # Mean
    for mean_sentence in saemmul_data['mean']:
        mean = Mean(word_id=word_id, mean=mean_sentence)
        db.session.add(mean)

        # MeanKeyword
        means = Mean.query.filter(Mean.mean == mean_sentence, Mean.word_id == word_id).all()
        mean_id = means[0].id
        mean_keywords = get_word_in_mean(mean_sentence)
        for keyword in mean_keywords:
            mean_keyword = MeanKeyword(mean_id=mean_id, mean_keyword=keyword)
            db.session.add(mean_keyword)

    # SimilarKeyword
    similar_data = get_similar_words(word, saemmul_data['mean'])
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

    mean_list = []
    # item 검색
    for item in xml.findAll('item'):
        if item.find('word').text != word:
            pass
        sense = item.find('sense')  # 의미를 포함하는 <>
        mean_list.append(sense.find('definition').text)

    xml_dict = {
        'word': word,
        'mean': mean_list
    }

    return xml_dict  # type list of dict


# TODO : 중복제거
# [ 네이버 사전에서 유사어 가져옴]
def get_similar_words(word, means):
    url = config.DICT_URL + quote(word)
    req = requests.get(url)
    html = req.content

    soup = BeautifulSoup(html.decode('utf-8', 'replace'), 'html.parser')
    similar_list = list()
    for mean in means:
        for tag in soup.find_all('span', text=mean):
            for e in tag.parent.parent.parent.findAll('sup'):
                e.extract()
            for similar in tag.parent.parent.parent.findAll('a', 'syno'):
                if similar.text not in similar_list:
                    similar_list.append(similar.text)
    return similar_list


# TODO : 중복제거
# [ 의미에서 단어가져오기 ]
def get_word_in_mean(mean):
    return list(set(Twitter().nouns(mean)))

