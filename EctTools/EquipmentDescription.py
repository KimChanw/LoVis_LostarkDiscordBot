def equipmentDescription(equip_name, equip_grade, quality, quality_color, equip_lv, elixir_text, equip_type):
    description = f'{equip_type} - :{quality_color}_square: **[{quality}] [{equip_grade}] {equip_name} ({equip_lv})**'
    
    if elixir_text:
        description += '\n' + f'```{elixir_text}```'
        
    return description

def accDescription(equip_name, equip_grade, quality, quality_color, equip_type, acc_tooltip_text):
    description = f'{equip_type} - :{quality_color}_square: **[{quality}] [{equip_grade}] {equip_name}**'
    
    description += '\n' + f'```{acc_tooltip_text}```'
    
    return description