import requests
from SearchTools.InfoBaseLine import InfoBaseLine

class weeklyContentsSearch(InfoBaseLine):
    def __init__(self):
        self.url_abyss = InfoBaseLine.BASIC_URL + '/gamecontents/challenge-abyss-dungeons'
        self.url_guardian = InfoBaseLine.BASIC_URL + '/gamecontents/challenge-guardian-raids'
    
    def abyssInfo(self) -> tuple:
        """
        return:
        어비스 던전명과 하위 던전 리스트 저장된 튜플
        """
        json_res = self._getinfo(self.url_abyss)
        
        
        # 하위 던전
        sub_dungeons = [abyss_info['Name'] for abyss_info in json_res]
        
        return sub_dungeons 
    
    def guardianInfo(self) -> list:
        """
        return:
        주간 레이드 리스트
        """
        json_res = self._getinfo(self.url_guardian)
        
        raids_name = [weekly_raid['Name'] for weekly_raid in json_res['Raids']]
        
        return raids_name