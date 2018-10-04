from controllers.collector import save_new_word
from models import *


# 검색 했을 때 ( 유사어 + 포함어 )
def search_word(word):
    word_info = get_single_word(word)

    # failed
    if "status" in word_info:
        return word_info
    else:
        return ''


# 검색 했을 때 ( 유사어 )
def search_similar_word(word):
    word_info = get_single_word(word)

    # failed
    if "status" in word_info:
        return word_info
    else:
        # 검색 단어에 대한 정보
        search_result = [word_info]

        similar_words = word_info['similar_words']

        # 검색 단어의 유사어에 대한 정보
        search_result += get_multiple_word(similar_words)

        # 검색 단어가 유사어에 포함 되어있는 단어들의 정보
        search_result += word_in_similar([word])

        # 검색 단어의 유사어가 유사어에 포함되어 있는 단어들의 정보
        search_result += word_in_similar(similar_words)

        result = {
            "status": "ok",
            "result": {
                "word_id": word_info['word_id'],
                "word": word_info['word'],
                "part": word_info['part'],
                "length": len(search_result),
                "search_result": search_result
            }
        }

        return result


# 검색 했을 때 ( 포함어 )
def search_mean_word(word):
    word_info = get_single_word(word)

    # failed
    if "status" in word_info:
        return word_info
    else:
        # 검색 단어에 대한 정보
        search_result = [word_info]
        # 검색 단어가 의미에 포함된 단어들의 정보 추가
        search_result += word_in_mean(word)

        result = {
            "status": "ok",
            "result": {
                "word_id": word_info['word_id'],
                "word": word_info['word'],
                "part": word_info['part'],
                "length": len(search_result),
                "search_result": search_result
            }
        }
        return result


# 단어 하나의 정보
def get_single_word(word):
    result = {
        "status": "failed",
    }

    words = Word.query.filter(Word.word == word).all()

    if len(words) <= 0:
        save_new_word(word)
        words = Word.query.filter(Word.word == word).all()
        if len(words) <= 0:
            return result
    else:
        return {
            "word_id": words[0].id,
            "word": words[0].word,
            "part": words[0].part,
            "mean": get_mean_list(word),
            "mean_words": get_mean_words_list(word),
            "similar_words": get_similar_words_list(word)
        }


# 단어 여러개의 정보
def get_multiple_word(words):
    words = []
    for word in words:
        word = get_single_word(word)
        if "status" in word:        # 아마 없을 듯 ==> 국어사전에서 얻어온 정보를 통해 검색하는 것이기 때문
            return word
        words.append(word)

    return words


# TODO
# 특정 단어의 의미 list 를 반환 해주는 함수
def get_mean_list(word):
    return []


# TODO
# 특정 단어의 similar word 를 반환 해주는 함수
def get_similar_words_list(word):
    return []


# TODO
# 특정 단어의 mean word 를 반환 해주는 함수
def get_mean_words_list(word):
    return []


# TODO :
# 유사어에 해당 단어가 포함되어 있는 단어들을 리턴해주는 함수
def word_in_similar(word):
    return [{}]


# TODO :
# 의미 키워드에 포함되어 있는 단어들을 리턴해주는 함수
def word_in_mean(word):

    return [{}]

