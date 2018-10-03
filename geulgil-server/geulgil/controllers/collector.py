import collections
from urllib import request
from urllib.parse import quote
from bs4 import BeautifulSoup
from geulgil import db
from models import *

import config


# [ 데이터베이스에서 새로운 단어를 추가 저장함 ]


def save_new_word(word):

    db.session.commit()
    return ''


# [ 샘물 api에서 국어사전 정보 가져옴 ]
def get_mean_words(word):
    # api 요청키 및 url
    url = config.SAEMMUL_API['url'] + "?key=" + config.SAEMMUL_API['key'] \
          + "&q=" + quote(word) + "&num=10" + "&advanced=y" \
          + "&target=1" + "&method=exact"

    # header 정보 추가
    headers = {
        'User-Agent': config.HEADER_USER_AGENT
    }

    # url 요청 및 오픈
    req = request.Request(url, headers=headers)
    data = request.urlopen(req).read()

    # BeautifulSoup 을 이용하여 파싱하기 위한 객체 생성
    xml = BeautifulSoup(data, "html.parser")
    dict_list = list()

    # item 검색
    for item in xml.findAll('item'):
        # print type(item)
        xml_dict = collections.OrderedDict()
        xml_dict['word'] = item.find('word').text  # 단어
        sense = item.find('sense')  # 의미를 포함하는 <>
        xml_dict['mean'] = sense.find('definition').text  # 의미
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
    req = request.get(url)
    html = req.content

    soup = BeautifulSoup(html.decode('utf-8', 'replace'), 'html.parser')
    similar_list = list()
    for tag in soup.find_all('span', text=mean):
        for e in tag.parent.parent.parent.findAll('sup'):
            e.extract()
        for similar in tag.parent.parent.parent.findAll('a', 'syno'):
            similar_list.append(similar.text)
    return similar_list
