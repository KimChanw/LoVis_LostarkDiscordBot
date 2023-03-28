import discord
import discord.message
from discord.ext import commands
from discord import app_commands
from SearchTools import *
from ExtractTools import *
from EctTools import *


class TroubleFinder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='사사게', description='인벤 사사게 수록 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def trouble_info(self, interaction: discord.Interaction, char_name: str):
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
        
async def setup(bot: commands.Bot):
    await bot.add_cog(
        TroubleFinder(bot)
    )