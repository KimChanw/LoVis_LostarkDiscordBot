# DiscordBot_temp.py : 디스코드 봇 명령어 모음 / 봇 네이밍 후 파일명 변경

import config as config
import discord
import discord.message
from CharInfoSearch import CharInfoSearch
from ItemInfoSearch import ItemInfoSearch
from discord.ext import commands

# 서버 메시지 인텐트 설정
discord.Intents.message_content = True

# 봇이 반응하는 접두사 : '/'
# 예시) 디스코드 채널 /ping 입력 -> pong 메시지 반환
bot = commands.Bot(command_prefix='/')

# 디스코드 봇 개발 API
DISCORD_TOKEN = config.discord_api

@bot.event
async def on_ready():
    print('Done!')
    await bot.change_presence(status=discord.Status.online, activity=None)
        
@bot.command()
async def ping(ctx):
    await ctx.channel.send(f'pong! 퐁!')


@bot.command(aliases=['정보','캐릭터','캐릭'])
async def info(ctx, char_name: str) -> None:
    """
    info : 단일 캐릭터 정보를 반환하는 커맨드
    예시) !정보 문학학사공학석사 / !캐릭터 문학학사공학석사
    """
    
    # 캐릭터 검색 객체 호출 -> 개별 캐릭터를 검색하는 메소드 (charInfo)
    search = CharInfoSearch(char_name)
    charInfo = search.charInfo()
    
    if charInfo:    # 검색 결과가 존재함
        await ctx.send(f' {ctx.author.mention} {charInfo["CharacterName"]}, {charInfo["CharacterClassName"]}, {charInfo["ItemAvgLevel"]}')
    
    else:
        await ctx.send(f' {ctx.author.mention} 존재하지 않는 닉네임 입니다.')
    
# info 커맨드에서 캐릭터 이름이 빠질 시 에러 메시지 반환
@info.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('올바른 닉네임 형식을 입력해주세요.')


@bot.command(aliases=['경매','전각','배분', '분배'])
async def auc_distribution(ctx, item_name: str) -> None:
    """
    auc_distribution : 전각 분배 계산기
    예시) !경매 광기 / !전각 고독한 기사
    입찰가와 선점입찰가를 embed 형식으로 출력
    """
    
    # 아이템 검색 객체 호출 -> 각인서 아이템 가격 검색 메소드 (engravingBookPrice)
    item_search = ItemInfoSearch(item_name)
    itemInfo = item_search.engravingBookPrice()
    
    # 검색이 안된다면 결과가 없어 IndexError 발생
    try:
        # 정식 아이템 이름 / 경매장 기준 최근 판매값
        official_name = itemInfo["Items"][-1]["Name"]
        recent_price = itemInfo["Items"][-1]["RecentPrice"]
        
    except IndexError:
        await ctx.send("존재하지 않는 아이템 입니다.")
    
    # 4인 및 8인 파티 일반 입찰가와 선점 입찰가
    bid_4 = recent_price * 0.95 * 3/4
    preempt_bid_4 = recent_price * 0.95 * 10/11 * 3/4
    
    bid_8 = recent_price * 0.95 * 7/8
    preempt_bid_8 = recent_price * 0.95 * 10/11 * 7/8
    
    # 디스코드 메시지로 출력할 embed 형식
    embed = discord.Embed(title='전각 분배금 계산기',
                          discription=f'**{official_name}**',
                          color=0XFFD700)
    
    embed.add_field(name='경매장 최저가',
                    value=f'{recent_price}\n\n\n\n', inline=False)
    
    # 소수점 제한하여 출력
    embed.add_field(name='4인 파티',
                    value=f'입찰가 : {bid_4:.0f}\n선점입찰가 : {preempt_bid_4:.0f}\n\n\n\n', inline=False)
    embed.add_field(name='8인 파티',
                    value=f'입찰가 : {bid_8:.0f}\n선점입찰가 : {preempt_bid_8:.0f}')
    
    await ctx.send(embed=embed)

# 아이템 이름이 누락될 시
@auc_distribution.error
async def auc_distribution_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('올바른 아이템 이름 형식을 입력해주세요.')

bot.run(DISCORD_TOKEN)

