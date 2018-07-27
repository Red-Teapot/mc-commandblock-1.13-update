import argparse

from commands.upgrader.upgrade import upgrade

arg_parser = argparse.ArgumentParser('Upgrades commands in functions and in-world command blocks to Minecraft 1.13 format')

arg_parser.add_argument('-c', '--command', type=str, help='Process only given command')

args = arg_parser.parse_args()

if args.command:
    print(upgrade(args.command))