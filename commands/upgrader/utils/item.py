from commands.pre_1_13.parser.primitives import ID
from commands.pre_1_13.nbtstr.types import NBTCompound, NBTString
from commands import upgrader
from .nbt import item as item_nbt
from .. import data

def upgrade(id: ID, metadata: int, nbt: NBTCompound) -> str:
    if not metadata:
        metadata = 0
    
    if nbt:  # Process stuff that might be in NBT
        nbt = item_nbt.upgrade(nbt)
    
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