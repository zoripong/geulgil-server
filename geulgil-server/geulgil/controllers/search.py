from controllers.collector import save_new_word
from models import *


def search_word(word):
    # 단어 자체에 대한 정보 (Common Case)
    # 검색 결과를 찾음
    words = Word.query.filter(Word.word == word).all()

    # 없는 단어일 경우 db에 새로 추가
    if len(words) <= 0:
        save_new_word(word)
        words = Word.query.filter(Word.word == word).all()

    # 단어의 유사어에 대한 정보 (Similar Case)
    # search_similar_word 실행
    # search_mean_word 실행

    # json return
    search_result = [{
    } for word in words]
    return ''


def search_similar_word(word):
    return ''


def search_mean_word(word):
    return ''

# TODO : 유사어에 해당 단어가 포함되어 있는 단어들을 리턴해주는 함수
# TODO : 의미 키워드에 포함되어 있는 단어들을 리턴해주는 함수

# filter가 유사어일 경우 --경우의 수 1 //유사어일 경우 이 함수 호출
def dbforsimilar(searchWord):
    conn = pymysql.connect(host='52.78.168.169', port=3306, user='root', passwd='Geulgil123!', db='geulgil',
                           charset='utf8')
    cursor = conn.cursor()

    # searchWord가 DB에 없다면 insert
    insertDB(conn, cursor, searchWord)

    # searchWord의 유사어키워드 배열 생성
    cursor.execute("select similarkeyword from item where word ='" + searchWord + "'")
    sKeyword = []
    for j in range(cursor.rowcount):
        fetch = cursor.fetchone()[0]
        if (fetch != ''):
            sKeyword = fetch.split(",")
            del sKeyword[len(sKeyword) - 1]

    apiItem = {'title': searchWord, 'relatives': []}


    #commonCase:searchWord
    apiItem = commonCase(cursor, apiItem, searchWord)

    # searchWord의 유사어 단어
    apiItem = similarCase(cursor, apiItem, sKeyword)

    # case1:searchWord가 유사어에 포함되어 있는 단어
    apiItem = case1(cursor, apiItem, searchWord)

    # case3:searchWord의 유사어가 유사어에 포함되어 있는 단어
    apiItem = case3(cursor, apiItem, sKeyword)

    jsonString = json.dumps(apiItem, indent=4)

    cursor.close()
    conn.close()

    return jsonString


# filter가 의미일 경우 --경우의 수 2,4//포함어일경우 이 함수 호출
def dbformean(searchWord):
    conn = pymysql.connect(host='52.78.168.169', port=3306, user='root', passwd='Geulgil123!', db='geulgil',
                           charset='utf8')
    cursor = conn.cursor()

    # searchWord가 DB에 없다면 insert
    insertDB(conn, cursor, searchWord)


    apiItem = {'title': searchWord, 'relatives': []}

    # commonCase:searchWord
    apiItem = commonCase(cursor, apiItem, searchWord)

    # case2:searchWord가 의미키워드에 포함되어있는 단어
    apiItem = case2(cursor, apiItem, searchWord)

    jsonString = json.dumps(apiItem, indent=4)

    cursor.close()
    conn.close()

    return jsonString
