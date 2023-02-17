import requests
from bs4 import BeautifulSoup

class TroubleSearch:
    def __init__(self, search_kw):
        self.search_kw = search_kw
        
    def _check_result(self, bs_object):
        # 검색 결과 여부 확인
        # 최근 1만개 이내 검색
        
        no_result = bs_object.find_all(
            'div', {'class' : 'no-result'}
        )
        
        if no_result:
            return False
        
        return True
    
    def searchTrouble(self):
        base_url = f'https://www.inven.co.kr/board/lostark/5355?query=list&p=1&sterm=&name=subject&keyword={self.search_kw}'
        req = requests.get(base_url)
        
        bs = BeautifulSoup(req.text, 'html.parser')
        
        post_url_list = []
        title_list = []
        
        if self._check_result(bs):
            post_result_list = bs.find_all(
                'a', {'class' : "subject-link"}
            )

            # 공지글 제거
            post_result_list = post_result_list[1:]
            
            for result in post_result_list:
                post = result.attrs['href']
                
                # 게시글 이름 재구성
                title = result.text.split()
                title = ' '.join(title)

                post_url_list.append(post)
                title_list.append(title)
                
        return post_url_list, title_list