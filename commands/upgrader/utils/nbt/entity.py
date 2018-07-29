from commands.pre_1_13.nbtstr.types import NBTCompound, NBTString
from commands import upgrader


def upgrade(nbt: NBTCompound) -> NBTCompound:
    if 'Command' in nbt:
        nbt['Command'].value = upgrader.upgrade(nbt['Command'].value)
    
    if 'Passengers' in nbt:
        for i in range(0, len(nbt['Passengers'])):
            nbt['Passengers'][i] = upgrade(nbt['Passengers'][i])

    return nbt