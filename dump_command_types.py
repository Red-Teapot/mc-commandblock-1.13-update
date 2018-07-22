import os, sys
from os import path

from process import process_region

world_folder = path.abspath(sys.argv[1])
result_file = path.abspath(sys.argv[2])

print('World path is', world_folder)
print('Result file path is', result_file)

regions_folder = path.join(world_folder, 'region')
region_files = [f for f in os.listdir(regions_folder) if path.isfile(path.join(regions_folder, f))]
functions_folder = path.join(world_folder, 'data/functions')

command_names = list()
commands = list()

# Process in-world command blocks

print('Processing in-world CBs')

def process_callback(cb):
    cmd = cb['Command'].value.replace('\n', '')
    cmd_name = cmd[0:cmd.find(' ')]

    global command_names
    global commands

    if cmd:
        commands += [cmd]
    if cmd_name not in command_names:
        command_names += [cmd_name]

    return False

for f in region_files:
    reg = path.join(regions_folder, f)

    print('Opening', reg)

    process_region(reg, process_callback)

# Process functions

print('Processing functions')

def check_folder(folder):
    files = os.listdir(folder)

    global command_names
    global commands

    for file in files:
        if path.isfile(path.join(folder, file)):
            with open(path.join(folder, file)) as f:
                for cmd in f.readlines():
                    cmd = cmd.replace('\n', '')
                    cmd_name = cmd[0:cmd.find(' ')]

                    if cmd:
                        commands += [cmd]
                    if cmd_name not in command_names:
                        command_names += [cmd_name]
                    
        else:
            check_folder(os.path.join(folder, file))

check_folder(functions_folder)

# Save result

with open(result_file, 'w') as f:
    f.write('Command names:\n')
    for cmd in command_names:
        f.write(cmd + '\n')
    f.write('\n\nCommands:\n')
    for cmd in commands:
        f.write(cmd + '\n')