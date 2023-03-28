import discord
import discord.message
from discord.ext import commands
from discord import app_commands
from SearchTools import *
from ExtractTools import *
from EctTools import *


class Auction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='전각', description='전설 각인서 가격 및 분배금 정보를 알려줍니다.')
    @app_commands.describe(item_name = '각인서 이름')
    async def auc_book_distrib(self, interaction: discord.Interaction, item_name: str) -> None:
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


    @app_commands.command(name='골드', description='골드 분배금 정보를 알려줍니다.')
    @app_commands.describe(gold = '골드')
    async def auc_gold_distrib(self, interaction: discord.Interaction, gold: int):
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


async def setup(bot: commands.Bot):
    await bot.add_cog(
        Auction(bot)
    )