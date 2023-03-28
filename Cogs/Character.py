import discord
import discord.message
from discord.ext import commands
from discord import app_commands
from SearchTools import *
from ExtractTools import *
from EctTools import *

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='정보', description='캐릭터의 다양한 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def char_info(self, interaction: discord.Interaction, char_name: str) -> None:
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
        

    @app_commands.command(name='장비', description='착용한 장비 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def equipment_info(self, interaction: discord.Interaction, char_name: str):
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
        
    @app_commands.command(name='악세', description='착용한 악세서리 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def accessory_info(self, interaction: discord.Interaction, char_name: str):
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
        

    @app_commands.command(name='각인', description='적용 각인 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def engrav_info(self, interaction: discord.Interaction, char_name: str):
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


    @app_commands.command(name='배럭', description='계정 내 배럭 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def siblings_info(self, interaction: discord.Interaction, char_name: str):
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
    @app_commands.command(name='보석', description='장착 보석 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def gems_info(self, interaction: discord.Interaction, char_name: str):
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
        
    @app_commands.command(name='카드', description='장착 카드 정보를 알려줍니다.')
    @app_commands.describe(char_name = '닉네임')
    async def cards_info(self, interaction: discord.Interaction, char_name: str):
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

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Character(bot)
    )