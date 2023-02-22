# DiscordBot_temp.py : 디스코드 봇 명령어 모음 / 봇 네이밍 후 파일명 변경

from datetime import datetime

import discord
import discord.message

from discord.ext import commands

from SearchTools import *
from SearchTools import config

from ExtractTools import *

from EctTools import *

# 봇이 반응하는 접두사 : '/'
# 예시) 디스코드 채널 /ping 입력 -> pong 메시지 반환
bot = commands.Bot(command_prefix='/')

# 디스코드 봇 개발 API
DISCORD_TOKEN = config.discord_api

# 봇이 작동되면 온라인으로 상태 전환
@bot.event
async def on_ready():
    print('Done!')
    await bot.change_presence(status=discord.Status.online, activity=None)

# 테스트 명령어
@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'pong!')


@bot.command(aliases=['정보','캐릭터','캐릭', '인포'])
async def char_info(ctx, char_name: str) -> None:
    """
    char_name : 캐릭터 이름
    
    return:
    캐릭터 정보 출력 임베드
    """
    # 클라이언트에서 호출한 메소드 및 실행 시간 로그 (메소드 이름과 실행 시간만 출력)
    # 추후 로그 DB 만들어 insert 예정
    print(ctx.command, toNowTime())
    
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
    
    await ctx.send(ctx.author.mention, embed=embed)
    
# info 커맨드에서 캐릭터 이름이 빠질 시 에러 메시지 반환
@char_info.error
async def char_info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('올바른 닉네임 형식을 입력해주세요.')



@bot.command(aliases=['장비'])
async def equipment_info(ctx, char_name):
    """
    char_name : 캐릭터 이름
    
    return:
    캐릭터가 착용하는 장비 상세 사항 임베드 메시지
    """
    print(ctx.command, toNowTime())
    
    equipment_search = CharInfoSearch(char_name)
    equipment_info, acc_info = equipment_search.equipmentInfo()
    
    if equipment_info == None and acc_info == None:
        await ctx.send('착용 장비가 없습니다.')
        return
    
    embed = discord.Embed(title='')
    embed.set_author(name=f'착용 장비 - {char_name}', icon_url='https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Shop_icon/Shop_icon_1445.png')
    
    # 제너레이터에서 값 꺼내오기
    for equip_iter in equipmentExtract(equipment_info):
        description = equipmentDescription(*equip_iter)

        embed.add_field(name='', value=description, inline=False)
    
    await ctx.send(ctx.author.mention, embed=embed)
    
    
    
    
@bot.command(aliases=['각인'])
async def engrav_info(ctx, char_name):
    """
    return:
    캐릭터가 장착 중인 각인 정보
    """
    print(ctx.command, toNowTime())
    
    search = CharInfoSearch(char_name)
    engInfo = search.engravInfo()
    
    if engInfo == None:
        await ctx.send(f'{ctx.author.mention} 존재하지 않는 닉네임 입니다.')
        return

    embed = discord.Embed(title=f'장착 각인 - {char_name}')
    
    _engrav_name = ''
    
    # 장착한 각인 데이터 순회 -> 각인 이름 출력
    for idx in range(len(engInfo)):
        _engrav_name += engInfo[idx]['Name'] + '\n'
    
    embed.add_field(name='', value=_engrav_name, inline=False)
    
    await ctx.send(ctx.author.mention, embed=embed)

@engrav_info.error
async def engrav_info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('올바른 닉네임 형식을 입력해주세요.')



#### 캐릭터 배럭
@bot.command(aliases=['배럭', '부캐'])
async def siblings_info(ctx, char_name):
    """
    return: 
    같은 계정에 생성된 캐릭터를 레벨 순으로 최대 6명까지 출력
    """
    print(ctx.command, toNowTime())
    
    search = CharInfoSearch(char_name)
    siblingsInfo = search.siblingsInfo()
    
    # 캐릭터가 존재하지 않을 시 오류 메시지 반환하고 메소드 종료
    if siblingsInfo == None:
        await ctx.send(f'{ctx.author.mention} 존재하지 않는 닉네임 입니다.')
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
        
    await ctx.send(ctx.author.mention, embed=embed)
    
@siblings_info.error
async def sibilings_info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('올바른 닉네임 형식을 입력해주세요.')



#### 캐릭터 착용 보석
@bot.command(aliases=['보석'])
async def gems_info(ctx, char_name):
    """
    return:
    캐릭터가 장착 중인 보석 정보 임베드 메시지
    """
    print(ctx.command, toNowTime())
    
    search = CharInfoSearch(char_name)
    gemsInfo = search.gemsInfo()
    
    if gemsInfo == None:
        await ctx.send(f'{ctx.author.mention} 존재하지 않는 닉네임 입니다.')
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
    
    await ctx.send(ctx.author.mention, embed=embed)

@gems_info.error
async def gems_info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('올바른 닉네임 형식을 입력해주세요.')




@bot.command(aliases=['전각'])
async def auc_book_distrib(ctx, item_name: str) -> None:
    """
    item_name : 전설 각인서 이름
    예시) !전각 고독한 기사
    
    return: 
    파티 인원 별 입찰가와 선점입찰가를 embed 형식으로 출력
    """
    
    print(ctx.command, toNowTime())
    
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
        await ctx.send("존재하지 않는 아이템 입니다.")
    
    # 4인 및 8인 파티 일반 입찰가와 선점 입찰가 (priceExtract 메소드 사용)
    bid_4, preempt_bid_4, bid_8, preempt_bid_8 = \
        priceExtract(recent_price)
    
    # 디스코드 메시지로 출력할 embed 형식
    embed = discord.Embed(title='',
                          description='',
                          color=0XFFD700)
    
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
    
    
    
    await ctx.send(ctx.author.mention, embed=embed)


# 아이템 이름이 누락될 시 오류
@auc_book_distrib.error
async def auc_book_distrib_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f' {ctx.author.mention} 올바른 아이템 이름 형식을 입력해주세요.')



@bot.command(aliases=['골드', '분배', '배분', '경매'])
async def auc_gold_distrib(ctx, gold: int):
    """
    gold : 골드 값
    예시) !분배 2030 / !경매 3000
    
    return: 
    파티 인원 별 입찰가와 선점입찰가를 embed 형식으로 출력
    """
    
    print(ctx.command, toNowTime())
    
    bid_4, preempt_bid_4, bid_8, preempt_bid_8 = \
        priceExtract(gold)
        
    embed = discord.Embed(title='',
                          description='')
    
    embed.set_author(name='경매 분배금 계산기', icon_url='https://cdn-lostark.game.onstove.com/EFUI_IconAtlas/Money/Money_4.png')

    embed.add_field(name='4인 파티',
                    value=f'입찰가 : {bid_4:.0f}\n선점입찰가 : {preempt_bid_4:.0f}\n\n\n\n', inline=False)
    embed.add_field(name='8인 파티',
                    value=f'입찰가 : {bid_8:.0f}\n선점입찰가 : {preempt_bid_8:.0f}')
    
    
    await ctx.send(ctx.author.mention, embed=embed)




@bot.command(aliases=['사사게', '사고', '사건'])
async def trouble_info(ctx, char_name):
    """
    char_name : 캐릭터 이름
    
    return:
    최근 1만개 게시글 중 올라온 사건사고 게시글 이름과 하이퍼링크 
    """
    
    print(ctx.command, toNowTime())
    
    trouble_search = TroubleSearch(char_name)
    trouble_post, trouble_title = trouble_search.searchTrouble()
        
    embed = discord.Embed(title=f':exclamation: 사사게 검색 결과 - {char_name}', 
                          description='''부캐명이 포함되지 않을 수 있다는 점 참고 부탁드립니다!
                                         최근 1만개의 게시글 내에서 검색합니다.''')

    if len(trouble_post) == 0 and len(trouble_title) == 0:
        embed.add_field(name='', value='**검색 결과가 없습니다!**')
        await ctx.send(ctx.author.mention, embed=embed)
        return
    
    # 인덱스와 검색 결과 같이 출력
    for idx, (url, title) in enumerate(zip(trouble_post, trouble_title)):
        idx += 1
        embed.add_field(name='', value=f'{idx}. [{title}](<{url}>)', inline=False)
    
    await ctx.send(ctx.author.mention, embed=embed)




@bot.command(aliases=['카드'])
async def cards_info(ctx, char_name):
    """
    char_name : 캐릭터 이름
    
    return:
    캐릭터가 장착 중인 카드 세트 이름과 효과 정보
    """
    print(ctx.command, toNowTime())
    
    cards_search = CharInfoSearch(char_name)
    cardsInfo = cards_search.cardInfo()
    
    if cardsInfo == None:
        await ctx.send(f'{ctx.author.mention} 존재하지 않는 닉네임 입니다.')
        return
    
    embed = discord.Embed(title='', description='')
    embed.set_author(name=f'{char_name} 캐릭터 카드 세트 정보')
    
    # 카드 세트 이름 / 세트 정보 출력
    # 세트 정보는 코드 블록 형식으로 출력함
    for c_set in cardsInfo:
        _name, _description = cardExtract(c_set)
        _description = '```' + _description + '```'
        embed.add_field(name=_name, value=_description, inline=False)
    
    print(ctx.command, toNowTime())
    
    await ctx.send(ctx.author.mention, embed=embed)



@bot.command(aliases=['주간컨텐츠', '도가토', '도비스'])
async def weeklyContents_info(ctx):
    """
    no parameters
    
    return:
    주간 도전 컨텐츠 목록
    """
    print(ctx.command, toNowTime())
    
    weekly_contents = weeklyContentsSearch()
    
    embed = discord.Embed(title='주간 도전 컨텐츠 목록')
    
    # 던전 리스트, 이미지 url
    sub_abyss, abyss_img_url = \
        weekly_contents.abyssInfo()
    
    # 가디언 토벌 리스트
    guardian_list, guardian_image_url = weekly_contents.guardianInfo()
            
    # contents_img = imageConcat(total_img)
    
    abyss_description = '\n'.join(sub_abyss)
    embed.add_field(name='도전 어비스 던전', value=abyss_description, inline=False)
    
    guardian_descrition = '\n'.join(guardian_list)
    embed.add_field(name='도전 가디언 토벌', value=guardian_descrition)
    
    await ctx.send(ctx.author.mention, embed=embed)
    
bot.run(DISCORD_TOKEN)

