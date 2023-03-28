import discord
from discord.ext import commands
from discord import app_commands

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='help')
    async def help(self, interaction: discord.Interaction):
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

# Cog 클래스를 이용하여 명령어 분리 시 필수로 작성
async def setup(bot: commands.Bot):
    await bot.add_cog(
        Help(bot)
    )