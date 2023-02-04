import config
import requests


class CharInfoSearch:
    """
    CharInfoSearch : 로스트아크 공식 API를 통해 캐릭터 정보를 탐색하는 클래스
    
    1. charInfo : 단일 캐릭터 정보 (이름, 레벨, )
    """
    # private 변수
    # 로스트아크 api key
    __LOSTARK_API = config.lostark_api
    BASIC_URL = 'https://developer-lostark.game.onstove.com'
    HEADERS = {
        'accept' : 'application/json',
        'authorization' : f'bearer {__LOSTARK_API}'
    }
    
    # 객체 호출 시 캐릭터 이름을 인자로 받음
    def __init__(self, char_name):
        self.char_name = char_name
    
    # 단일 캐릭터 정보 검색
    def charInfo(self):
        # api 엔드포인트
        url = CharInfoSearch.BASIC_URL + f'/armories/characters/{self.char_name}/profiles'
        # requests 라이브러리로 get
        res = requests.get(url, headers=CharInfoSearch.HEADERS)
        
        # json 포맷으로 변환
        return res.json()


