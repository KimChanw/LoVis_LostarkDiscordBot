# embed에 들어갈 description 작성 메소드
# dict -> str

def descriptionTool(data: dict):
    description = ''
    
    for key, value in zip(data.keys(), data.values()):
        description += f'**{key}**  :  {value}\n'
    
    return description