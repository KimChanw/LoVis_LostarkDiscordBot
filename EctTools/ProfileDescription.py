# embed에 들어갈 description 작성 함수
# dict -> str

def profileDescription(data: dict):
    description = ''
    
    for key, value in zip(data.keys(), data.values()):
        description += f'**{key}**  :  {value}\n'
    
    return description