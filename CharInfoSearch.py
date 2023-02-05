import requests
from InfoBaseLine import InfoBaseLine

class CharInfoSearch(InfoBaseLine):
    """
    CharInfoSearch : 로스트아크 공식 API를 통해 캐릭터 정보를 탐색하는 클래스
    
    1. charInfo : 단일 캐릭터 정보 (이름, 레벨, )
    """
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
    
    def siblingsInfo(self):
        url = CharInfoSearch.BASIC_URL + f'/characters/{self.char_name}/siblings'
        res = requests.get(url, headers=CharInfoSearch.HEADERS)
        json_res = res.json()
        
        # 캐릭터 아이템 레벨 기준 json 정렬
        # 레벨 형식 : 1,470.00 -> 문자열로 저장되어 있으므로 float 전환
        # float 전환 위해 해당 값에서 ','을 제거
        json_res.sort(key=lambda x: float(x['ItemMaxLevel'].replace(',', '')), 
                      reverse=True)
        
        return json_res
        
    def skillInfo(self):
        # 정식 사이트 크롤링으로 채택 스킬 구현 필요
        pass
    


