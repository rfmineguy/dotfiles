import argparse
import platform
import os
import sys

if platform.system() != "Linux":
    print("This script is only tested for linux")
    sys.exit(1)

description = "Utility for symlinking/unlinking configuration files"
targets = {
    'nvim': '~/.config/nvim',
    'qtile': '~/.config/qtile'
}

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

# ====
# Setup the argparse library
parser = MyParser()
subparsers = parser.add_subparsers(dest='subparser', help='subcommand help')

parser_create = subparsers.add_parser('create', help='creates a symlink to a config dir for target')
parser_create.add_argument('--target', dest='target', choices=targets.keys(), required=True, type=str, help='target help')

parser_remove = subparsers.add_parser('remove', help='removes a symlinked target')
parser_remove.add_argument('--target', dest='target', choices=targets.keys(), required=True, type=str, help='target help')

parser_getlinkdir = subparsers.add_parser('getlinkdir', help='prints the link directory for a given target')
parser_getlinkdir.add_argument('--target', dest='target', choices=targets.keys(), required=True, type=str, help='target help')

parser_showtargets = subparsers.add_parser('showtargets', help='displays a list of the valid targets')

# Setup the argparse library
# ====

# ====
# Functions for the target actions
def create_symlink(target):
    print(f"Request to create symlink ... ({target}) {os.path.realpath(target)} -> {os.path.expanduser(targets[target])}")
    if os.path.exists(os.path.expanduser(targets[target])):
        print(f"Error: \"{os.path.expanduser(targets[target])}\" already exists on your computer. Back it up then rerun this script")
        sys.exit(1)
    os.symlink(os.path.realpath(target), os.path.expanduser(targets[target]))

def remove_symlink(target):
    print(f"Request to remove symlink ... {target} -> {os.path.expanduser(targets[target])}")
    if not os.path.exists(os.path.expanduser(targets[target])):
        print(f"Error: {targets[target]} doesn't exist, cant remove the symlink")
        sys.exit(1)
    os.unlink(os.path.expanduser(targets[target]))
    print(f"Unlinked {os.path.expanduser(targets[target])}")

def getlinkdir(target):
    print(f"Linkdir of {target} is {targets[target]}")

def showtargets():
    print("Targets:")
    for key, value in targets.items():
        print(f'{key:<10}   {value:<10}')
# Functions for the target actions
# ====

# ====
# Peform the action based on the argparse output
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()
if args.subparser == 'create':
    create_symlink(args.target)
elif args.subparser == 'remove':
    remove_symlink(args.target)
elif args.subparser == 'getlinkdir':
    getlinkdir(args.target)
elif args.subparser == 'showtargets':
    showtargets()
# Peform the action based on the argparse output
# ====
