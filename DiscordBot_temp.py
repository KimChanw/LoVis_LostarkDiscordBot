# DiscordBot_temp.py : 디스코드 봇 명령어 모음 / 봇 네이밍 후 파일명 변경

import config as config
import discord
import discord.message
from discord.ext import commands
from InfoSearch import CharInfoSearch


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
    await ctx.send(f'pong! 퐁!')


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
async def auc_distribution(ctx, gold: int) -> None:
    """
    auc_distribution : 경매 골드 분배 계산기
    예시) !경매 3000 / !전각 3000
    손익분기점과 
    """
    

bot.run(DISCORD_TOKEN)

