import argparse, sys, logging, logging.config, os

from commands.upgrader import upgrade
from commands.pre_1_13.cmdex import CMDEx

from processing import command_blocks

arg_parser = argparse.ArgumentParser('Upgrades commands in functions and in-world command blocks to Minecraft 1.13 format')

arg_parser.add_argument('-c', '--command', type=str, help='Process only given command')
arg_parser.add_argument('--cmdex', type=str, help='Try to match given CMDEx')
arg_parser.add_argument('--debug', help='Allow debugging messages', action='store_true')
arg_parser.add_argument('--cmd-stdinput', help='Read command from standard in', action='store_true')
arg_parser.add_argument('-w', '--world', type=str, help='Upgrade commands in specified world folder')

args = arg_parser.parse_args()

log_format = '[%(levelname)s] %(name)s: %(message)s'
logging.basicConfig(level=(logging.DEBUG if args.debug else logging.INFO), format=log_format)

if not args.cmdex and args.command:
    print(upgrade(args.command))
    
    sys.exit(0)

if args.cmdex and args.command:
    cmdex = CMDEx(args.cmdex)
    order, props = cmdex.match(args.command)

    print(order)
    print(props)

    sys.exit(0)

if args.cmd_stdinput:
    for command in sys.stdin:
        if command:
            print(upgrade(command))
    
    sys.exit(0)

if args.world:
    command_blocks.run(os.path.abspath(args.world))

    sys.exit(0)

arg_parser.print_usage()