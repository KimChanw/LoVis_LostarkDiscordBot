import requests
from InfoBaseLine import InfoBaseLine

class ItemInfoSearch(InfoBaseLine):
    """
    CharInfoSearch : 로스트아크 공식 API를 통해 캐릭터 정보를 탐색하는 클래스
    주의사항) 검색 아이템은 반드시 광기 / 비기 / 고독한 기사 등 정식 이름으로 검색할 것
    예시) 고기(고독한 기사) 등으로 검색 불가
    
    1. engravingBookPrice : 각인서 가격 정보 (이름, 레벨, )
    """
    
    def __init__(self, item_name):
        self.item_name = item_name
    
    def engravingBookPrice(self):
        url = ItemInfoSearch.BASIC_URL + '/markets/items'
        
        # post method 위한 전송 데이터
        params = {
                "Sort": "",
                "CategoryCode": 40000,
                "CharacterClass": "",
                "ItemTier": 0,
                "ItemGrade": "",
                "ItemName": f"{self.item_name}",    # 검색 대상 아이템
                "PageNo": 0,
                "SortCondition": "ASC"
                }
        
        res = requests.post(url, data=params, headers=ItemInfoSearch.HEADERS)
        
        return res.json()
        