import requests
from SearchTools.InfoBaseLine import InfoBaseLine

class CharInfoSearch(InfoBaseLine):
    """
    CharInfoSearch : 로스트아크 공식 API를 통해 캐릭터 정보를 탐색하는 클래스
    
    1. charInfo : 단일 캐릭터 정보 (이름, 레벨, )
    2. SiblingsInfo : 부캐릭터 목록 정보
    3. engravInfo : 단일 캐릭터가 장착 중인 각인 정보
    """

    # 객체 호출 시 캐릭터 이름을 인자로 받음
    def __init__(self, char_name):
        self.char_name = char_name
    
    # private 메소드
    # get 메소드로 호출하는 api
    def __getinfo(self, url):
        # requests 라이브러리로 get
        res = requests.get(url, headers=CharInfoSearch.HEADERS)
        # json 포맷으로 변환
        json_res = res.json()
        
        return json_res
    
    # 단일 캐릭터 정보 검색
    def charInfo(self):
        # api 엔드포인트
        url = CharInfoSearch.BASIC_URL + f'/armories/characters/{self.char_name}/profiles'
        json_res = self.__getinfo(url)
        
        return json_res
    
    def siblingsInfo(self):
        # api로 호출
        url = CharInfoSearch.BASIC_URL + f'/characters/{self.char_name}/siblings'
        json_res = self.__getinfo(url)
        
        # 캐릭터 아이템 레벨 기준 json 정렬
        # 레벨 형식 : 1,470.00 -> 문자열로 저장되어 있으므로 float 전환
        # float 전환 위해 해당 값에서 ','을 제거
        try:
            json_res.sort(key=lambda x: float(x['ItemMaxLevel'].replace(',', '')), 
                        reverse=True)
            
            return json_res
        
        # 캐릭터 정보가 존재하지 않으면 Nonetype 반환하여 sort 메소드가 없음
        except AttributeError:
            return
    
    # 착용 각인 정보
    def engravInfo(self):
        url = CharInfoSearch.BASIC_URL + f'/armories/characters/{self.char_name}/engravings'
        json_res = self.__getinfo(url)
        
        try:
            return json_res['Effects']
        
        except AttributeError:
            return
    
    # 보석 착용 정보
    def gemsInfo(self):
        
        url = CharInfoSearch.BASIC_URL + f'/armories/characters/{self.char_name}/gems'
        json_res = self.__getinfo(url)
        
        try:
            return json_res['Gems']
        
        except AttributeError:
            return
    
    def cardInfo(self):
        url = CharInfoSearch.BASIC_URL + f'/armories/characters/{self.char_name}/cards'
        json_res = self.__getinfo(url)
        
        try:
            return json_res['Effects'][0]['Items']

        except:
            return

