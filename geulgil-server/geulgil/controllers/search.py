from geulgil.controllers.collector import save_new_word
from geulgil.models import *


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
            "mean": get_mean_list(words[0].id),
            "mean_words": get_mean_words_list(words[0].id),
            "similar_words": get_similar_words_list(words[0].id)
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


# 특정 단어의 의미 list 를 반환 해주는 함수
def get_mean_list(word_id):
    means = Mean.query.filter(Mean.word_id == word_id).all()
    return [mean.mean
            for mean in means]


# 특정 단어의 similar word 를 반환 해주는 함수
def get_similar_words_list(word_id):
    similar_keywords = SimilarKeyword.query.filter(SimilarKeyword.word_id == word_id).all()
    return [similar_keyword.similar_keyword
            for similar_keyword in similar_keywords]


# 특정 단어의 mean word 를 반환 해주는 함수
def get_mean_words_list(word_id):
    mean_keywords = MeanKeyword.query.filter(MeanKeyword.word_id == word_id).all()
    return [mean_keyword.mean_keyword
            for mean_keyword in mean_keywords]


# 유사어에 해당 단어가 포함되어 있는 단어들을 리턴해주는 함수
def word_in_similar(word):
    similar_words = SimilarKeyword.query.filter(SimilarKeyword.similar_keyword == word).all()

    result = []
    for similar_word in similar_words:
        word = Word.query.filter(Word.id == similar_word.word_id).all()
        result.append(get_single_word(word.word))

    return result


# 의미 키워드에 포함되어 있는 단어들을 리턴해주는 함수
def word_in_mean(word):
    mean_words = MeanKeyword.query.filter(MeanKeyword.similar_keyword == word).all()

    result = []
    for mean_word in mean_words:
        word = Word.query.filter(Word.id == mean_word.word_id).all()
        result.append(get_single_word(word.word))

    return result

