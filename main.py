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

# 디스코드 봇 개발 API 코드
DISCORD_TOKEN = config.discord_api

class Lovis(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix = '!',
            intents = discord.Intents.default()
            )
        
        self.initial_extention = [
            "Cogs.Auction",
            "Cogs.Character",
            "Cogs.Content",
            "Cogs.TroubleFinder",
            "Cogs.Help"
        ]

    # Cogs 폴더로 분리한 기능 bot에 호출
    async def setup_hook(self):
        for ext in self.initial_extention:
            await self.load_extension(ext)

        await bot.tree.sync()
    
    async def close(self):
        await super().close()
    
    async def on_ready(self):
        print('Done!')
        try:
            synced = await bot.tree.sync()
            print(f'Synced {len(synced)} commands')
            
        except Exception as e:
            print(e)
            
        await bot.change_presence(status=discord.Status.online, 
                                activity=discord.Game(name='명령어 모음은 /help'))

bot = Lovis()    
bot.run(DISCORD_TOKEN)

