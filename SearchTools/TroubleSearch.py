import requests
from bs4 import BeautifulSoup

class TroubleSearch:
    def __init__(self, char_name):
        self.char_name = char_name
        
    def searchTrouble(self):
        # 페이로드로 검색 대상 닉네임 전송
        url = 'https://api.sasagefind.ga/sasagefind'
        payload = {
            'charname' : self.char_name,
            'type' : 'titlecontent'
        }
        site_html = requests.post(url, data=payload)

        result_json = site_html.json()
        
        # 이터레이터 생성, 순회
        trouble_text_iter = self._extract_idx_title(result_json)
        
        # yield할 게시글 주소와 제목
        for idx, title in trouble_text_iter:
            trouble_url = f'https://www.inven.co.kr/board/lostark/5355/{idx}'
            
            yield trouble_url, title
    
    # 게시글 번호와 제목 이터레이터
    def _extract_idx_title(self, result_json):
        for trouble_result in result_json:
            _idx = trouble_result['idx']
            _title = trouble_result['title']
            
            yield _idx, _title
