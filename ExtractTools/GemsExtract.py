import re
    
def gemsExtract(gems_json):
    """
    gems_json : api로 받은 보석 json 데이터
    
    return : 
    가공 데이터 : 보석 이름 / 보석 등급 별 색 / 스킬명 dict가 저장된 리스트
    """

    # 추출 과정 : RegEx를 이용하여 pattern 정의 -> 문자열에서 matching
    # 보석 이름 추출 -> gems_json 데이터 "Name" 데이터 사용
    name_pattern = re.compile('(?<=<FONT COLOR=\'.{7}\'>).+(?=<\/FONT>)')
    name_search_result = name_pattern.search(gems_json["Name"])
    gem_name = name_search_result.group()
    
    # 스킬 이름 추출 -> gems_json 데이터 "Tooltip" 데이터 사용
    # 클래스 이름 + 스킬 이름
    # 예시) [워로드] + 차지 스팅어
    class_pattern = re.compile('\[.+\] (?=<FONT COLOR=\'#FFD200\'>)')
    class_search_result = class_pattern.search(gems_json["Tooltip"])
    class_name = class_search_result.group()
    
    skill_pattern = re.compile('(?<=<FONT COLOR=\'#FFD200\'>).+(?=<\/FONT>)')
    skill_search_result = skill_pattern.search(gems_json["Tooltip"])
    skill_name = skill_search_result.group()
    
    gem_skill = class_name + skill_name
    
    # 정렬 기준 위해 보석 레벨 정수형으로 추출
    lv_pattern = re.compile('[0-9]+')
    lv_search_result = lv_pattern.search(gem_name)
    lv = int(lv_search_result.group())  # str -> int
    
    return gem_name, gem_skill, lv