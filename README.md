# Just a thing to convert Minecraft pre-1.13 commands to the new format

This script parses Minecraft pre-1.13 commands and modifies them so they are compatible with the new Minecraft 1.13 command syntax.

It can upgrade commands from console input or inside a world (both command blocks and functions).

# Installation

You will need Python 3 to run the script. Also, virtualenv is recommended.

1. If you have virtualenv installed, create an environment by running `virtualenv env` and then `source env/bin/activate`
2. Run `pip install -r requirements.txt`

That is all you need.

# Usage

## Input commands manually

 - `python run.py (-c|--command) <command>` will write the upgraded version of the command to stdout.

 - `python run.py --cmd-stdinput` is used to upgrade commands as you input them to stdin (e.g. type them by hand). It will write the upgraded versions to stdout.

## Upgrade all commands in a world

The script is also capable of upgrading all commands in command blocks and functions in a Minecraft world.

**WARNING:** It is strongly recommended to make a backup of the world before using the script.

After you make the backup, just run `python run.py (-w|--world) <path_to_the_world>` and wait for some time (depending on the count of commands in the world). All errors will be written to stdout.

# What it does (a more detailed description)

All commands are parsed, including entity selectors, item/block IDs, JSON strings (used in `tellraw` command for example) and NBT data strings (I decided to point it out because there were some implementations that used regular expressions to replace some parts of the command string). All incorrect and unknown commands are left as is and an error message is written. The `commands.pre_1_13` module does just that.

Then all selectors and IDs are upgraded to match the new format (e.g. `r=3` in a selector is replaced with `distance=..3`). The `commands.upgrader.utils` and `commands.upgrader.data` modules are responsible for that.

After that a new command is built using upgraded selectors, IDs etc. Main goal was to generate commands that do the same thing, so some commands (like `testfor ..`) are replaced with different ones (like `execute if entity ...`). See `commands.upgrader.commands` module for implementation.

Finally, the generated command is written to stdout (if using manual mode) or saved to the command block where the old command was or added to a function in the datapack (as after 1.13 functions can be run only in datapacks). See `run.py` and `processing` module for implementation.

# License

The project is licensed under the terms of MIT License (see LICENSE file).