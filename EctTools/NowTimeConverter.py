from datetime import datetime

def toNowTime():
    now = datetime.now()
    
    # 마이크로초 빼고 변환
    now_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    return now_time