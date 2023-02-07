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