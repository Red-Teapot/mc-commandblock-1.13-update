from commands.pre_1_13.nbtstr.types import NBTCompound, NBTString
from commands import upgrader
from . import item as item_nbt


def upgrade(nbt: NBTCompound) -> NBTCompound:
    if 'Command' in nbt:
        nbt['Command'].value = upgrader.upgrade(nbt['Command'].value)

    return nbt