# 글길 검색 api [![Build Status](https://travis-ci.org/zoripong/geulgil-server.svg?branch=master)](https://travis-ci.org/zoripong/geulgil-server)

일상생활 중 단어가 떠오르지 않는 불편함들을 해결하기 위한 역발상 단어사전 '글길'의 api 서버입니다.
어플리케이션의 자세한 설명은 글길 android 앱 레포지토리의 [README.md]()를 확인해주세요.

## Getting Started
### Preparation
* [python 3.5.2](https://www.python.org/downloads/release/python-352/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/#)
* [KoLNPy](https://konlpy-ko.readthedocs.io/ko/v0.4.3/)

### Installing
> requirements 설치
```
pip install -r requirements.txt
```

### Running the Flask App
- config.py를 필요로 합니다. 
```
python run.py
```


## Information of API
- 글길의 검색을 위한 API로 유사어 또는 의미를 중심으로 검색할 수 있도록 구분하였습니다.
- 글길의 데이터베이스에 없는 단어를 요청할 경우 새로이 단어에 관련된 정보를 수집하기 때문에 국어사전에 존재하는 단어라면 모두 검색이 가능합니다.
### Request Example
> 통합 검색
```
[GET] /words/<검색 단어>
```
> 유사어 중점 검색
```
[GET] /words/<검색 단어>/similar
```
> 의미 중점 검색
```
[GET] /words/<검색 단어>/mean
```
### Response Example
'마음'이라는 단어를 통한 검색에 대한 예입니다.
> Key Explanation

| KEY           	| MEAN                                    	|
|:---------------:	|-----------------------------------------	|
|     status    	| 상태를 나타냄, (성공: OK, 실패: Failed) 	|
| result        	| 검색 결과에 대한 정보를 포함            	|
| word_id       	| 단어 고유 번호                          	|
| word          	| 단어                                    	|
| part          	| 단어 품사 정보                          	|
| length        	| 결과 사이즈                             	|
| search_result 	| 검색 결과에 대한 집합                   	|
| mean          	| 단어의 의미                             	|
| mean_words    	| 의미에 포함되는 단어들의 집합           	|
| similar_words 	| 유사어에 포함되는 단어들의 집합         	|

> Json Structure
```json
{
  "status": "ok",
  "result": {
    "word_id": 13,
    "word": "사랑",
    "part": 0,
    "length": 1,
    "search_result": [
      {
        "word_id": 13,
        "word": "사랑",
        "part": 0,
        "mean": [
            "어떤 사람이나 존재를 몹시 아끼고 귀중히 여기는 마음. 또는 그런 일.",
            "어떤 사물이나 대상을 아끼고 소중히 여기거나 즐기는 마음. 또는 그런 일.",
            "남을 이해하고 돕는 마음. 또는 그런 일."
        ],
        "mean_keywords":[
            [
                "사람",
                "일",
                "마음",
                "몹시",
                "존재"
            ],
            [
                "일",
                "마음",
                "사물",
                "대상"
            ],
            [
                "일",
                "마음",
                "이해",
                "남"
            ]
        ],
        "similar_keywords":[
            "정애",
            "친애",
            "하트"
        ]
      }
    ]
  }
}
```

    
## Contents of Searching
> 검색

아래의 케이스들을 모두 포함하여 검색합니다.


> 의미 중점 검색

아래와 같은 단어 정보들을 포함합니다.
- 검색 단어에 대한 정보
- 검색 단어가 의미에 포함된 단어들의 정보

> 유사어 중점 검색

아래와 같은 단어 정보들을 포함합니다.
- 검색 단어에 대한 정보
- 검색 단어의 유사어에 대한 정보
- 검색 단어가 유사어에 포함 되어있는 단어들의 정보
- 검색 단어의 유사어가 유사어에 포함되되는 단어들의 정보

