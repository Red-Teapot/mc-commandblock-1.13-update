from nbt.region import RegionFile
from nbt.nbt import TAG_String

def process_region(reg):
    print('Processing file:', reg)
    
    reg_nbt = RegionFile(reg)

    for m in reg_nbt.get_metadata():
        chunk = reg_nbt.get_chunk(m.x, m.z)
        level = chunk['Level']
        tile_entities = level['TileEntities']

        found_command_block = False

        for ent in tile_entities:
            if str(ent['id']) == 'minecraft:command_block':
                cmd = ent['Command'].valuestr()
                x = ent['x']
                y = ent['y']
                z = ent['z']

                print(x, y, z, cmd)

                cmd += ' lol'

                ent['Command'].value = cmd

                found_command_block = True

        if found_command_block:
            reg_nbt.write_chunk(m.x, m.z, chunk)
    
    reg_nbt.close()