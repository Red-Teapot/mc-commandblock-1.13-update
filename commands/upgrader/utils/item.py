from commands.pre_1_13.parser.primitives import ID
from commands.pre_1_13.nbtstr.types import NBTCompound, NBTString
from commands import upgrader
from . import enchant, block, entity, effect
from .. import data

def upgrade(id: ID, metadata: int, nbt: NBTCompound) -> str:
    if not metadata:
        metadata = 0
    
    if nbt:  # Process stuff that might be in NBT
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
        
        if id.value == 'command_block' and 'BlockEntityTag' in nbt and 'Command' in nbt['BlockEntityTag']:
            nbt['BlockEntityTag']['Command'].value = upgrader.upgrade(nbt['BlockEntityTag']['Command'].value)
        
        if 'CustomPotionEffects' in nbt:
            for i in range(0, len(nbt['CustomPotionEffects'])):
                old_id = nbt['CustomPotionEffects'][i]['id'].value
                nbt['CustomPotionEffects'][i]['id'] = NBTString(effect.upgrade(old_id))
        
        # TODO Maybe also upgrade inventories contents and mob spawner entities?
    
    if id.value in data.item_data_id_map:
        replacement_data = data.item_data_id_map[id.value]

        if type(replacement_data) is dict:
            id.value = data.item_data_id_map[id.value][metadata]
        else:
            id.value = replacement_data
    
    result = str(id)

    if nbt and nbt.values and len(nbt.values) > 0:
        result += str(nbt)
    
    return result