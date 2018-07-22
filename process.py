from nbt.region import RegionFile
from nbt.nbt import TAG_String

def process_region(reg):
    print('Processing file:', reg)
    
    reg_nbt = RegionFile(reg)

    for m in reg_nbt.get_metadata():
        chunk = reg_nbt.get_chunk(m.x, m.z)
        level = chunk['Level']
        tile_entities = level['TileEntities']

        chunk_needs_update = False

        for ent in tile_entities:
            if ent['id'].value == 'minecraft:command_block':
                cmd = ent['Command'].value
                x = ent['x'].value
                y = ent['y'].value
                z = ent['z'].value

                print(x, y, z, '|' + cmd + '|')

                #cmd += ' lol'

                #ent['Command'].value = cmd

                #chunk_needs_update = True

        if chunk_needs_update:
            reg_nbt.write_chunk(m.x, m.z, chunk)
    
    reg_nbt.close()