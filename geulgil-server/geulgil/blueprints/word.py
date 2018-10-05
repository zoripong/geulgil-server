from urllib.parse import quote

from flask import Blueprint, jsonify

from geulgil.controllers.search import search_word, search_similar_word, search_mean_word

bp = Blueprint('word', __name__, url_prefix='/words')


# [ 검색 할 경우 ]
@bp.route('/<string:word>')
def get_word(word):
    return jsonify(search_word(word))


# [ 유사어를 통해 검색 할 경우 ]
@bp.route('/<string:word>/similar')
def get_similar_word(word):
    return jsonify(search_similar_word(word))


# [ 의미를 통해 검색 할 경우 ]
@bp.route('/<string:word>/mean')
def get_mean_word(word):
    return jsonify(search_mean_word(word))

