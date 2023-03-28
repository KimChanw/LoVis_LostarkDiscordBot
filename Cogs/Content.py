import discord
from discord.ext import commands
from discord import app_commands
from SearchTools import *
from EctTools import *

class Contents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='주간컨텐츠', description='이번 주 도전 컨텐츠 정보를 알려줍니다.')
    async def weeklyContents_info(self, interaction: discord.Interaction):
        """
        no parameters
        
        return:
        주간 도전 컨텐츠 목록
        """
        print(interaction.command.name, toNowTime())
        
        weekly_contents = weeklyContentsSearch()
        
        embed = discord.Embed(title='주간 도전 컨텐츠 목록')
        
        # 던전 리스트, 이미지 url
        sub_abyss = weekly_contents.abyssInfo()
        
        # 가디언 토벌 리스트
        guardian_list = weekly_contents.guardianInfo()
                        
        abyss_description = '```' + '\n'.join(sub_abyss) + '```'
        embed.add_field(name='도전 어비스 던전', value=abyss_description, inline=False)
        
        guardian_descrition = '```' + '\n'.join(guardian_list) + '```'
        embed.add_field(name='도전 가디언 토벌', value=guardian_descrition)
        
        await interaction.response.send_message(embed=embed)
        
async def setup(bot: commands.Bot):
    await bot.add_cog(
        Contents(bot)
    )