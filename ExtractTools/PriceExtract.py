def priceExtract(gold: int):
    """
    gold : 아이템의 골드 가격
    
    return:
    파티 별 입찰가와 선점입찰가 저장 튜플 
    """
    bid_4 = gold * 0.95 * 3/4
    preempt_bid_4 = gold * 0.95 * 10/11 * 3/4
    
    bid_8 = gold * 0.95 * 7/8
    preempt_bid_8 = gold * 0.95 * 10/11 * 7/8
    
    return bid_4, preempt_bid_4, bid_8, preempt_bid_8