def cardExtract(card_json):
    """
    card_json : api로 받은 카드 세트 효과 json 데이터
    
    return:
    카드 세트 이름 / 세트 효과가 저장된 튜플
    """
    
    name = card_json['Name']
    discript = card_json['Description']
    
    return name, discript