from commands.pre_1_13.nbtstr.types import NBTCompound, NBTString
from .. import effect, block, enchant
from . import block as block_nbt

def upgrade(nbt: NBTCompound) -> NBTCompound:
    if 'ench' in nbt:
        nbt['Enchantments'] = nbt['ench']
        del nbt['ench']
    
    if 'Enchantments' in nbt:
        for ench in nbt['Enchantments']:
            ench['id'] = enchant.upgrade(ench['id'])
    
    if 'StoredEnchantments' in nbt:
        for ench in nbt['StoredEnchantments']:
            ench['id'] = enchant.upgrade(ench['id'])
    
    if 'CanDestroy' in nbt:
        for i in range(0, len(nbt['CanDestroy'])):
            nbt['CanDestroy'][i] = block.upgrade(ID(None, nbt['CanDestroy'][i].value), None, None, None)[0].value
    
    if 'CanPlaceOn' in nbt:
        for i in range(0, len(nbt['CanPlaceOn'])):
            nbt['CanPlaceOn'][i] = block.upgrade(ID(None, nbt['CanPlaceOn'][i].value), None, None, None)[0].value
    
    if 'BlockEntityTag' in nbt:
        nbt['BlockEntityTag'] = block_nbt.upgrade(nbt['BlockEntityTag'])
    
    if 'CustomPotionEffects' in nbt:
        for i in range(0, len(nbt['CustomPotionEffects'])):
            old_id = nbt['CustomPotionEffects'][i]['id'].value
            nbt['CustomPotionEffects'][i]['id'] = NBTString(effect.upgrade(old_id))

    return nbt