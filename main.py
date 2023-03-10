# DiscordBot_temp.py : 디스코드 봇 명령어 모음 / 봇 네이밍 후 파일명 변경

from datetime import datetime

import discord
import discord.message

from discord.ext import commands
from discord import app_commands

from SearchTools import *
from SearchTools import config

from ExtractTools import *

from EctTools import *

# 봇이 반응하는 접두사 : '/'
# 예시) 디스코드 채널 /ping 입력 -> pong 메시지 반환
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', intents=intents)

# 디스코드 봇 개발 API 코드
DISCORD_TOKEN = config.discord_api

# 봇이 작동되면 온라인으로 상태 전환
@bot.event
async def on_ready():
    print('Done!')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} commands')
        
    except Exception as e:
        print(e)
        
    await bot.change_presence(status=discord.Status.online, 
                              activity=discord.Game(name='명령어 모음은 /help'))

@bot.tree.command(name='정보', description='캐릭터의 다양한 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def char_info(interaction: discord.Interaction, char_name: str) -> None:
    """
    char_name : 캐릭터 이름
    
    return:
    캐릭터 정보 출력 임베드
    """
    # 클라이언트에서 호출한 메소드 및 실행 시간 로그 (메소드 이름과 실행 시간만 출력)
    # 추후 로그 DB 만들어 insert 예정
    print(interaction.command.name, toNowTime())
    
    
    # 캐릭터 검색 객체 호출 -> 개별 캐릭터를 검색하는 메소드 (charInfo)
    search = CharInfoSearch(char_name)
    
    # 캐릭터 정보 / 레벨 정보 / 특성 정보 / 공격력 및 체력 / 썸네일 url
    char_profile, char_lev_info, char_spec_info, attack_hp, tendencies, thumnail = \
                                        search.charInfo()
    
    
    class_name = char_profile['직업']
    # 캐릭터 정보 description
    profile_des = profileDescription(char_profile)
    char_lev_des = profileDescription(char_lev_info)
    attack_hp_des = profileDescription(attack_hp)
    char_spec_des = profileDescription(char_spec_info)
    tendencies_des = profileDescription(tendencies)
    
    embed = discord.Embed(title='')
    embed.set_author(name=f'{char_name}', icon_url=classIcon[class_name])
    
    embed.set_thumbnail(url=thumnail)
    
    embed.add_field(name='캐릭터 정보', value=profile_des, inline=True)
    embed.add_field(name='', value='\t\t', inline=True)
    embed.add_field(name='레벨', value=char_lev_des)
    
    embed.add_field(name='', value='\n\n', inline=False)
    embed.add_field(name='성향', value=tendencies_des, inline=True)
    
    # embed.add_field(name='', value=char_spec_des, inline=False)

    embed.add_field(name='', value='\t\t', inline=True)
    embed.add_field(name='특성', 
                    value=attack_hp_des+'\n'+char_spec_des, 
                    inline=True)
    
    await interaction.response.send_message(embed=embed)
    

@bot.tree.command(name='장비', description='착용한 장비 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def equipment_info(interaction: discord.Interaction, char_name: str):
    """
    char_name : 캐릭터 이름
    
    return:
    캐릭터가 착용하는 장비 상세 사항 임베드 메시지
    """
    print(interaction.command.name, toNowTime())
    
    equipment_search = CharInfoSearch(char_name)
    equipment_info, _, _ = equipment_search.equipmentInfo()
    
    if equipment_info == None:
        await interaction.response.send_message('착용 장비가 없습니다.')
        return
    
    embed = discord.Embed(title='')
    embed.set_author(name=f'착용 장비 - {char_name}', icon_url='https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Shop_icon/Shop_icon_1445.png')
    
    # 제너레이터에서 값 꺼내오기
    for equip_iter in equipmentExtract(equipment_info):
        description = equipmentDescription(**equip_iter)

        embed.add_field(name='', value=description, inline=False)
    
    await interaction.response.send_message(embed=embed)
    
@bot.tree.command(name='악세', description='착용한 악세서리 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def accessory_info(interaction: discord.Interaction, char_name: str):
    """
    char_name : 캐릭터 이름
    
    return:
    캐릭터가 착용하는 장비 상세 사항 임베드 메시지
    """
    
    acc_search = CharInfoSearch(char_name)
    _, acc_info, _ = acc_search.equipmentInfo()

    if acc_info == None:
        await interaction.response.send_message('착용 악세서리가 없습니다.')
        return

    embed = discord.Embed(title='')
    embed.set_author(name=f'착용 악세서리 - {char_name}', icon_url='https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Acc/Acc_212.png')
    
    for acc_iter in accExtract(acc_info):
        description = accDescription(**acc_iter)
        
        embed.add_field(name='', value=description, inline=False)
    
    await interaction.response.send_message(embed=embed)
    

@bot.tree.command(name='각인', description='적용 각인 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def engrav_info(interaction: discord.Interaction, char_name: str):
    """
    return:
    캐릭터가 장착 중인 각인 정보
    """
    print(interaction.command.name, toNowTime())
    
    search = CharInfoSearch(char_name)
    engInfo = search.engravInfo()
    
    if engInfo == None:
        await interaction.response.send_message('존재하지 않는 닉네임 입니다.')
        return

    embed = discord.Embed(title=f'장착 각인 - {char_name}')
    
    _engrav_name = ''
    
    # 장착한 각인 데이터 순회 -> 각인 이름 출력
    for idx in range(len(engInfo)):
        _engrav_name += engInfo[idx]['Name'] + '\n'
    
    embed.add_field(name='', value=_engrav_name, inline=False)
    
    await interaction.response.send_message(embed=embed)

@engrav_info.error
async def engrav_info_error(interaction: discord.Interaction, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await interaction.response.send_message('올바른 닉네임 형식을 입력해주세요.')



@bot.tree.command(name='배럭', description='계정 내 배럭 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def siblings_info(interaction: discord.Interaction, char_name: str):
    """
    return: 
    같은 계정에 생성된 캐릭터를 레벨 순으로 최대 6명까지 출력
    """
    print(interaction.command.name, toNowTime())
    
    search = CharInfoSearch(char_name)
    siblingsInfo = search.siblingsInfo()
    
    # 캐릭터가 존재하지 않을 시 오류 메시지 반환하고 메소드 종료
    if siblingsInfo == None:
        await interaction.response.send_message('존재하지 않는 닉네임 입니다.')
        return
    
    embed = discord.Embed(title=f'배럭 목록 - {char_name}')
    
    embed.add_field(name='캐릭터명', value='', inline=True)
    embed.add_field(name='직업', value='', inline=True)
    embed.add_field(name='아이템 레벨', value='', inline=True)
    
    # 캐릭터 개수가 6개 이하라면 가지고 있는 부캐 개수만큼 출력
    barraks_cnt = min(len(siblingsInfo), 6)
    for idx in range(barraks_cnt):
        _info = siblingsInfo[idx]
        _name = _info['CharacterName']
        _class = _info['CharacterClassName']
        _itemLevel = _info['ItemMaxLevel']

        embed.add_field(name='', value=f'{_name}', inline=True)
        embed.add_field(name='', value=f'{_class}', inline=True)
        embed.add_field(name='', value=f'{_itemLevel}', inline=True)
        
    await interaction.response.send_message(embed=embed)


#### 캐릭터 착용 보석
@bot.tree.command(name='보석', description='장착 보석 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def gems_info(interaction: discord.Interaction, char_name: str):
    """
    return:
    캐릭터가 장착 중인 보석 정보 임베드 메시지
    """
    print(interaction.command.name, toNowTime())
    
    search = CharInfoSearch(char_name)
    gemsInfo = search.gemsInfo()
    
    if gemsInfo == None:
        await interaction.response.send_message('보석 장착 정보가 존재하지 않는 닉네임입니다.')
        return
    
    embed = discord.Embed(title='')
    embed.set_author(name=f'보석 정보 - {char_name}', 
                     icon_url='https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Use/Use_9_55.png')
    
    
    # 코드 블록 형태로 출력
    gem_messages = ''
    skill_messages = ''
    
    # 보석 레벨 순 정렬 위해 리스트에 추가
    gem_info_list = []
    for gem_data in gemsInfo:
        # (7레벨 홍염의 보석, [워로드] 차지 스팅어)
        _gem_info = gemsExtract(gem_data)
        gem_info_list.append(_gem_info)
    
    # 레벨 기준 내림차순 정렬
    gem_info_list.sort(key=lambda x: x[2], reverse=True)
    
    # 코드 블록에 출력 메시지 추가
    for gem_info in gem_info_list:
        gem_color = f':{gem_info[3]}_square: ' # 이모지 형식으로 전환 (예시 - :green_square:)
        gem_messages += gem_color + gem_info[0] + '\n\n'
        skill_messages += gem_info[1] + '\n\n'
    
    # 코드 블록으로 embed 출력
    embed.add_field(name='보석', value=gem_messages, inline=True)
    embed.add_field(name='', value='\t', inline=True)
    embed.add_field(name='스킬', value=skill_messages, inline=True)
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='전각', description='전설 각인서 가격 및 분배금 정보를 알려줍니다.')
@app_commands.describe(item_name = '각인서 이름')
async def auc_book_distrib(interaction: discord.Interaction, item_name: str) -> None:
    """
    item_name : 전설 각인서 이름
    예시) !전각 고독한 기사
    
    return: 
    파티 인원 별 입찰가와 선점입찰가를 embed 형식으로 출력
    """
    
    print(interaction.command.name, toNowTime())
    
    # 아이템 검색 객체 호출
    item_search = ItemInfoSearch(item_name)
    itemInfo = item_search.engravingBookPrice()
    
    # 검색이 안된다면 결과가 없어 IndexError 발생
    try:
        # 정식 아이템 이름 / 경매장 기준 최근 판매값
        official_name = itemInfo["Items"][-1]["Name"]
        recent_price = itemInfo["Items"][-1]["RecentPrice"]
        image_url = itemInfo["Items"][-1]["Icon"]
        
    except IndexError:
        await interaction.response.send_message("존재하지 않는 아이템 입니다.")
    
    # 4인 및 8인 파티 일반 입찰가와 선점 입찰가 (priceExtract 메소드 사용)
    bid_4, preempt_bid_4, bid_8, preempt_bid_8 = \
        priceExtract(recent_price)
    
    # 디스코드 메시지로 출력할 embed 형식
    embed = discord.Embed(title='',
                          description='')
    
    embed.set_author(name='전각 분배금 계산기', icon_url=image_url)
    
    # 아이템 이름 필드
    embed.add_field(name='아이템 이름', value=f'{official_name}', inline=False)
    
    # 최저가 필드
    embed.add_field(name='경매장 최저가',
                    value=f'{recent_price}\n\n\n\n', inline=False)
    
    # 분배금 필드, 소수점 제한하여 출력
    embed.add_field(name='4인 파티',
                    value=f'입찰가 : {bid_4:.0f}\n선점입찰가 : {preempt_bid_4:.0f}\n\n\n\n', inline=False)
    embed.add_field(name='8인 파티',
                    value=f'입찰가 : {bid_8:.0f}\n선점입찰가 : {preempt_bid_8:.0f}')
    
    
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='골드', description='골드 분배금 정보를 알려줍니다.')
@app_commands.describe(gold = '골드')
async def auc_gold_distrib(interaction: discord.Interaction, gold: int):
    """
    gold : 골드 값
    예시) /분배 2030 / /경매 3000
    
    return: 
    파티 인원 별 입찰가와 선점입찰가를 embed 형식으로 출력
    """
    
    print(interaction.command.name, toNowTime())
    
    bid_4, preempt_bid_4, bid_8, preempt_bid_8 = \
        priceExtract(gold)
        
    embed = discord.Embed(title='',
                          description='')
    
    embed.set_author(name='경매 분배금 계산기', icon_url='https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Money/Money_4.png')

    embed.add_field(name='4인 파티',
                    value=f'입찰가 : {bid_4:.0f}\n선점입찰가 : {preempt_bid_4:.0f}\n\n\n\n', inline=False)
    embed.add_field(name='8인 파티',
                    value=f'입찰가 : {bid_8:.0f}\n선점입찰가 : {preempt_bid_8:.0f}')
    
    
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name='사사게', description='인벤 사사게 수록 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def trouble_info(interaction: discord.Interaction, char_name: str):
    """
    char_name : 캐릭터 이름
    
    return:
    최근 1만개 게시글 중 올라온 사건사고 게시글 이름과 하이퍼링크 
    """
    
    print(interaction.command.name, toNowTime())
    
    trouble_search = TroubleSearch(char_name)
    trouble_post, trouble_title = trouble_search.searchTrouble()
        
    embed = discord.Embed(title=f':exclamation: 사사게 검색 결과 - {char_name}', 
                          description='''부캐명이 포함되지 않을 수 있다는 점 참고 부탁드립니다!
                                         최근 1만개의 게시글 내에서 검색합니다.''')

    if len(trouble_post) == 0 and len(trouble_title) == 0:
        embed.add_field(name='', value='**검색 결과가 없습니다!**')
        await interaction.response.send_message(embed=embed)
        return
    
    # 인덱스와 검색 결과 같이 출력
    for idx, (url, title) in enumerate(zip(trouble_post, trouble_title)):
        idx += 1
        embed.add_field(name='', value=f'{idx}. [{title}](<{url}>)', inline=False)
    
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name='카드', description='장착 카드 정보를 알려줍니다.')
@app_commands.describe(char_name = '닉네임')
async def cards_info(interaction: discord.Interaction, char_name: str):
    """
    char_name : 캐릭터 이름
    
    return:
    캐릭터가 장착 중인 카드 세트 이름과 효과 정보
    """
    print(interaction.command.name, toNowTime())
    
    cards_search = CharInfoSearch(char_name)
    cardsInfo = cards_search.cardInfo()
    
    if cardsInfo == None:
        await interaction.response.send_message(f'존재하지 않는 닉네임 입니다.')
        return
    
    embed = discord.Embed(title='', description='')
    embed.set_author(name=f'{char_name} 캐릭터 카드 세트 정보')
    
    # 카드 세트 이름 / 세트 정보 출력
    # 세트 정보는 코드 블록 형식으로 출력함
    for c_set in cardsInfo:
        _name, _description = cardExtract(c_set)
        _description = '```' + _description + '```'
        embed.add_field(name=_name, value=_description, inline=False)
    
    await interaction.response.send_message(embed=embed)



@bot.tree.command(name='주간컨텐츠', description='이번 주 도전 컨텐츠 정보를 알려줍니다.')
async def weeklyContents_info(interaction: discord.Interaction):
    """
    no parameters
    
    return:
    주간 도전 컨텐츠 목록
    """
    print(interaction.command.name, toNowTime())
    
    weekly_contents = weeklyContentsSearch()
    
    embed = discord.Embed(title='주간 도전 컨텐츠 목록')
    
    # 던전 리스트, 이미지 url
    sub_abyss, abyss_img_url = \
        weekly_contents.abyssInfo()
    
    # 가디언 토벌 리스트
    guardian_list, guardian_image_url = weekly_contents.guardianInfo()
            
    # contents_img = imageConcat(total_img)
    
    abyss_description = '```' + '\n'.join(sub_abyss) + '```'
    embed.add_field(name='도전 어비스 던전', value=abyss_description, inline=False)
    
    guardian_descrition = '```' + '\n'.join(guardian_list) + '```'
    embed.add_field(name='도전 가디언 토벌', value=guardian_descrition)
    
    await interaction.response.send_message(embed=embed)
    
    
@bot.tree.command(name='help')
async def help(interaction: discord.Interaction):
    embed = discord.Embed(title='로비스 봇 명령어 모음',
                          description= "제작자 : 문학학사공학석사 @아만" + "\n" + "깃허브 주소 : https://github.com/KimChanw/LoVis_LostarkDiscordBot")

    embed.add_field(name='/정보 [캐릭터 이름]', value='캐릭터의 다양한 정보를 알려줍니다.', inline=False)

    embed.add_field(name='/장비 [캐릭터 이름]', value='캐릭터가 착용 중인 장비를 알려줍니다. (품질 / 등급 / 아이템 이름 / 아이템 레벨 / 엘릭서 부여)', inline=False)
    embed.add_field(name='/악세 [캐릭터 이름]', value='캐릭터가 착용 중인 악세서리를 알려줍니다. (품질 / 등급 / 아이템 이름 / 악세서리 정보)', inline=False)
    
    embed.add_field(name='/각인 [캐릭터 이름]', value='캐릭터가 장착 중인 각인 정보를 알려줍니다.')
    embed.add_field(name='/배럭 [캐릭터 이름]', value='계정 내 배럭 정보를 아이템 레벨 순으로 정렬하여 최대 6개까지 알려줍니다.', inline=False)
    embed.add_field(name='/보석 [캐릭터 이름]', value='캐릭터가 장착 중인 보석 정보를 알려줍니다.')
    embed.add_field(name='/전각 [전설 각인서 이름]', value='전설 각인서의 경매장 최저가를 기준으로 파티 인원 별 경매 분배금을 계산해 줍니다.' + '\n' + 
                                                            '! 반드시 전설 각인서 이름을 입력해 주세요.' + '\n' + 
                                                            '! 예시) /전각 처단자, /전각 고독한 기사, /전각 망치 (분노의 망치 검색됨)', inline=False)
    embed.add_field(name='/골드 [숫자]', value='입력한 골드를 기준으로 파티 인원 별 경매 분배금을 계산해 줍니다.', inline=False)
    embed.add_field(name='/사사게 [캐릭터 이름]', value='로스트아크 인벤 사건사고 게시판에 올라온 게시글을 검색합니다.' + '\n' +
                                                        '최근 게시된 1만개 내에서 검색하므로 과거의 결과는 나오지 않을 수 있습니다.' + '\n' +
                                                        '검색 속도 문제로 배럭 캐릭터의 게시글은 검색하지 않습니다.',
                                                        inline=False)
    embed.add_field(name='/카드 [캐릭터 이름]', value='캐릭터가 장착 중인 카드 세트 정보를 출력합니다.', inline=False)
    embed.add_field(name='/주간컨텐츠', value='이번 주의 도전 가디언 토벌, 도전 어비스 던전 리스트를 알려줍니다.', inline=False)
    
    await interaction.response.send_message(embed=embed)
    
bot.run(DISCORD_TOKEN)

