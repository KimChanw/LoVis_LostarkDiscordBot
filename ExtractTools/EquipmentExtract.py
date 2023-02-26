# -*- coding: utf-8 -*-

import re
import json

# 품질 수치와 표현 색 매핑
quality_map = {
    0 : 'red',
    1 : 'yellow',
    2 : 'yellow',
    3 : 'green',
    4 : 'green',
    5 : 'green',
    6 : 'green',
    7 : 'blue',
    8 : 'blue',
    9 : 'purple',
    10 : 'orange'
}

# 장비 툴팁으로 엘릭서 정보 추출
def _elixirExtract(tooltip):
    # 엘릭서 키워드가 장비 툴팁에 존재하면 엘릭서 부여 장비
    if '엘릭서' not in tooltip:
        return
    
    # 부여 정보 텍스트
    grant_text = ''
    
    
    # 재련 완료 여부 확인 - 재련이 완료된 장비는 툴팁 텍스트 내 '재련' 키워드가 존재하지 않음
    # 완료 여부에 따라 탐색할 key를 조정함
    # 기본 탐색할 key : Element_008
    
    element_key = 'Element_008'
    
    if '재련' not in tooltip:
        element_key = 'Element_007'
        
    # 장비 툴팁 json
    tooltip_json = json.loads(tooltip)
    
    # print(tooltip_json)
    
    elixir_grant_info = tooltip_json[element_key]['value']['Element_000']["contentStr"]
    
    # 최대 2개까지 부여 가능 / 첫 번째 옵션 Element_000부터 저장
    for i in range(len(elixir_grant_info)):
        grant = elixir_grant_info[f'Element_00{i}']["contentStr"]
        
        replace_tags = ["<FONT color='#FFD200'>", "</FONT>"]
         
        # 태그 제거 후 띄어쓰기 2개를 하나로 변환
        for tag in replace_tags:
            grant = grant.replace(tag, ' ').replace('  ', ' ')
            grant = grant.strip()
            
        grant = grant.replace('<BR>', '\n').replace('<br>', '\n')
        
        grant_text += grant + '\n\n'
    
    # 공백 정리
    grant_text = grant_text.strip()
    
    return grant_text
    
def equipmentExtract(equip_json):
    """
    equip_json : api로 받은 착용 장비 json 데이터
    
    return:
    장비 이름, 장비 품질, 장비 등급, 장비 레벨, 엘릭서 부여 정보 generator
    """
    # 품질 수치 뽑기 위한 정규표현식
    quality_pattern = re.compile('(?<=\\"qualityValue\\": )[0-9]+(?=,\\r\\n)')
    equip_lv_pattern = re.compile('(?<=\\"<FONT SIZE=\'14\'>아이템 레벨 )[0-9]+(?=.*<\/FONT>)')
    
    for idx in range(len(equip_json)):
        equip_name = equip_json[idx]['Name']
        equip_grade = equip_json[idx]['Grade']
        equip_type = equip_json[idx]['Type']
        
        # 품질은 툴팁에서 유일하게 존재 -> search 메소드 결과의 0번째 인덱스
        quality = quality_pattern.search(equip_json[idx]['Tooltip'])[0]
        
        # 품질을 10으로 나눈 몫으로 품질 표현 색 추출
        quality_color = quality_map[int(quality) // 10]
        
        # 아이템 레벨도 유일 -> search 메소드 결과 0번째 인덱스
        equip_lv = equip_lv_pattern.search(equip_json[idx]['Tooltip'])[0]
        
        # 엘릭서 부여 정보
        elixir_text = _elixirExtract(equip_json[idx]['Tooltip'])
        
        yield equip_name, equip_grade, quality, quality_color, equip_lv, elixir_text, equip_type
        
        
        
    
def accExtract(acc_json):
    """
    acc_json : api로 받은 착용 악세사리 json 데이터
    
    return:
    악세사리 이름, 악세사리 품질, 악세사리 등급, 악세사리 세부 정보 iterator
    """
    pass
