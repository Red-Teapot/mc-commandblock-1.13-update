from commands.pre_1_13.nbtstr.types import NBTCompound, NBTString
from commands.pre_1_13.parser.primitives import ID
from commands.upgrader.utils.nbt import block as block_nbt
from commands.upgrader.utils import enchant, block, effect

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
    
    if 'display' in nbt:
        if 'Name' in nbt['display']:
            nbt['display']['Name'] = '\"\\"' + nbt['display']['Name'].value + '\\"\"'

    return nbt