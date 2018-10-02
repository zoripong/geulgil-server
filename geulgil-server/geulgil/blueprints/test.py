from flask import Blueprint
from konlpy.tag import Komoran  # Window용
# from konlpy.tag import Twitter #Linux용


bp = Blueprint('test', __name__, url_prefix='/')
konlpy = Komoran()

@bp.route('/')
def index():
    return 'hello world'

@bp.route('/nouns/<string:str>/')
def natural_language(str):
    # jpype.attachThreadToJVM()
    list = konlpy.nouns(str)
    result = ''
    for i in list:
        result += i +':'
    return result

@bp.route('/request/<string:str>/<isMean>/')
def response(str, isMean):
    if(isMean == 'true'):
        return dbformean(str)
    else:
        return dbforsimilar(str)


@bp.route('/request/<string:str>/')
def getSamesound(str):
    return selectFromWord(str)
