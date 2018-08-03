from os import path
import os, json, logging
import nbt
from commands import upgrader


logger = logging.getLogger(__name__)

def process_region(region_file):
    region = nbt.region.RegionFile(region_file)

    for meta in region.get_metadata():
        chunk = region.get_chunk(meta.x, meta.z)
        tile_entities = chunk['Level']['TileEntities']

        chunk_needs_update = False

        for tile_entity in tile_entities:
            if tile_entity['id'].value in ['minecraft:command_block', 'command_block']:
                x = tile_entity['x'].value
                y = tile_entity['y'].value
                z = tile_entity['z'].value
                old_command = tile_entity['Command'].value.strip()

                if not old_command:
                    continue

                try:
                    new_command = upgrader.upgrade(old_command)
                    tile_entity['Command'].value = new_command
                    chunk_needs_update = True
                    logger.debug('Upgraded cmd at %s %s %s: %s', x, y, z, new_command)
                except Exception as e:
                    print(json.dumps({
                        'type': 'command_block',
                        'x': x, 
                        'y': y, 
                        'z': z,
                        'old_command': old_command,
                        'exception': str(e)
                    }, ensure_ascii=False))

        if chunk_needs_update:
            region.write_chunk(meta.x, meta.z, chunk)

def run(world_folder):
    region_folder = path.join(world_folder, 'region')
    region_files = [path.join(region_folder, f) for f in os.listdir(region_folder) if path.isfile(path.join(region_folder, f))]
    
    for region_file in region_files:
        process_region(region_file)