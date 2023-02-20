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
    
    # 단일 캐릭터 정보 검색
    def charInfo(self):
        # api 엔드포인트
        url = InfoBaseLine.BASIC_URL + f'/armories/characters/{self.char_name}/profiles'
        json_res = self._getinfo(url)
        
        # 출력 정보 전처리
        char_profile = {
            '서버' : json_res['ServerName'],
            '직업' : json_res['CharacterClassName'],
            '길드' : json_res['GuildName'],
            '칭호' : json_res['Title'],
            'PvP' : json_res['PvpGradeName'],
            '영지' : f"Lv.{json_res['TownLevel']} { json_res['TownName']}",
            '스포' : json_res['TotalSkillPoint']
        }
        
        # 레벨 정보
        char_lev_info = {
            '원정대 레벨' : json_res['ExpeditionLevel'],
            '전투 레벨' : json_res['CharacterLevel'],
            '아이템 레벨' : json_res['ItemAvgLevel']
        }
        
        # 공격력 / 최대 생명력 추가
        attack_hp = {}
        
        attack_hp['공격력'] = json_res['Stats'][7]['Value']
        attack_hp['최대 생명력'] = json_res['Stats'][6]['Value']
        
        # 특성 추가
        char_spec_info = {}
        for idx in range(6):
            stat_name = json_res['Stats'][idx]['Type']
            stat_val = json_res['Stats'][idx]['Value']
            char_spec_info[stat_name] = stat_val
        
        # 성향 포인트
        tendencies = {}
        for idx in range(len(json_res['Tendencies'])):
            name = json_res['Tendencies'][idx]['Type']
            val = json_res['Tendencies'][idx]['Point']
            tendencies[name] = val
        
        
        thumnail = json_res['CharacterImage']
                
        return char_profile, char_lev_info, char_spec_info, attack_hp, tendencies, thumnail
    
    def siblingsInfo(self):
        # api로 호출
        url = InfoBaseLine.BASIC_URL + f'/characters/{self.char_name}/siblings'
        json_res = self._getinfo(url)
        
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
        url = InfoBaseLine.BASIC_URL + f'/armories/characters/{self.char_name}/engravings'
        json_res = self._getinfo(url)
        
        try:
            return json_res['Effects']
        
        except AttributeError:
            return
    
    # 보석 착용 정보
    def gemsInfo(self):
        
        url = InfoBaseLine.BASIC_URL + f'/armories/characters/{self.char_name}/gems'
        json_res = self._getinfo(url)
        
        try:
            return json_res['Gems']
        
        except AttributeError:
            return
    
    def cardInfo(self):
        url = InfoBaseLine.BASIC_URL + f'/armories/characters/{self.char_name}/cards'
        json_res = self._getinfo(url)
        
        try:
            return json_res['Effects'][0]['Items']

        except:
            return

