from controllers.collector import save_new_word


def search_word(word):
    # 검색 결과를 찾음

    # 없는 단어일 경우 db에 새로 추가
    save_new_word(word)

    # 있을 경우 json return

    return ''


def search_similar_word(word):
    return ''


def search_mean_word(word):
    return ''
