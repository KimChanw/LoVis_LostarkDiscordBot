import requests
import SearchTools.config as config

class InfoBaseLine:
    """
    캐릭터 검색, 아이템 검색 등 정보별 검색 클래스에는 API Key, API 주소, 헤더가 필요함
    InfoBaseLine을 부모 클래스로 설정하고 상속을 통해 코드 반복 방지
    """
 
    # private 변수
    # 로스트아크 api key
    __LOSTARK_API = config.lostark_api
    BASIC_URL = 'https://developer-lostark.game.onstove.com'
    HEADERS = {
        'accept' : 'application/json',
        'authorization' : f'bearer {__LOSTARK_API}'
    }
    
    # private 메소드
    # get 메소드로 호출하는 api
    def _getinfo(self, url):
        # requests 라이브러리로 get
        res = requests.get(url, headers=InfoBaseLine.HEADERS)
        # json 포맷으로 변환
        json_res = res.json()
        
        return json_res