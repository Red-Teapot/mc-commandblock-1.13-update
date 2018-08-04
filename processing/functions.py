from os import path
import os, json, logging, sys, shutil
from commands import upgrader


logger = logging.getLogger(__name__)

old_functions_folder = 'data/functions'

def process_file(file):
    logger.debug('Processing file %s', file)

    result_lines = []

    with open(file, 'r') as f:
        line_num = 0
        for line in f:
            line = line.strip()
            if len(line) == 0 or line[0] == '#':
                result_lines += [line]
            else:
                new_cmd = line
                try:
                    new_cmd = upgrader.upgrade(line)
                except Exception as e:
                    print(json.dumps({
                        'type': 'function',
                        'file': file,
                        'line': line_num + 1,
                        'old_command': line,
                        'exception': str(e)
                    }, ensure_ascii=False))
                result_lines += [new_cmd]
            
            line_num += 1
    
    with open(file, 'w') as f:
        f.write('\n'.join(result_lines))

def process_folder(folder):
    logger.debug('Processing folder %s', folder)

    for file in os.listdir(folder):
        file_abs = path.join(folder, file)

        if path.isfile(file_abs):
            process_file(file_abs)
        else:
            process_folder(file_abs)

def run(world_folder, pack_name='default', pack_description=''):
    logger.debug('Creating necessary folders and files')
    logger.debug('Datapack name is \'%s\', description is \'%s\'', pack_name, pack_description)
    pack_folder = path.join(world_folder, 'datapacks', pack_name)
    old_functions_abs = path.join(world_folder, old_functions_folder)
    new_functions_abs = path.join(pack_folder, 'data', pack_name, 'functions')

    os.makedirs(pack_folder, exist_ok=True)
    os.makedirs(new_functions_abs, exist_ok=True)

    with open(path.join(pack_folder, 'pack.mcmeta'), 'w') as file:
        pack_json = {
            'pack': {
                'pack_format': 3,
                'description': pack_description,
            }
        }

        logger.debug('Creating pack.mcmeta')

        file.write(json.dumps(pack_json, ensure_ascii=False))

    logger.debug('Copying old functions to datapack (original folder will be preserved)')

    for f in os.listdir(old_functions_abs):
        old_file = path.join(old_functions_abs, f)
        new_file = path.join(new_functions_abs, f)
        logger.debug('Copying %s to %s', old_file, new_file)
        if path.isfile(old_file):
            shutil.copy(old_file, new_file)
        else:
            shutil.copytree(old_file, new_file)
    
    logger.debug('Processing copied functions')

    process_folder(new_functions_abs)