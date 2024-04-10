import argparse
import platform
import os
import sys


def is_platform_supported():
    system = platform.system().lower()
    return system == "linux" or system == "darwin"

description = "Utility for symlinking/unlinking configuration files"
targets = {
    'nvim': {
        'link': [
            ('./nvim', '~/.config/nvim')
        ]
    },
    'qtile': {
        'link': [
            ('./qtile', '~/.config/qtile')
        ]
    },
    'tmux': {
        'link': [
            ('./tmux', '~/.config/tmux')
        ]
    },
    'scripts/dwm': {
        'link': [
            ('./scripts/startdwm', '~/bin/startdwm'),
            ('testing', 'to somewhere')
        ]
        #'message': ''
    }
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
    full_local_target_path = os.path.realpath(target)
    link_rules = targets[target].link
    for link in link_rules:
        print(link)
    # full_system_target_path = os.path.expanduser(targets[target])


    # print(f"Request to create symlink ... ({target}) {full_local_target_path} -> {full_system_target_path}")
    # if os.path.exists(full_system_target_path):
    #     print(f"Error: \"{full_system_target_path}\" already exists on your computer. Back it up then rerun this script")
    #     sys.exit(1)
    # os.symlink(full_local_target_path, full_system_target_path)

def remove_symlink(target):
    full_installed_target_path = os.path.expanduser(targets[target])

    print(f"Request to remove symlink ... {target} -> {full_installed_target_path}")
    if not os.path.exists(full_installed_target_path):
        print(f"Error: {targets[target]} doesn't exist, cant remove the symlink")
        sys.exit(1)
    os.unlink(full_installed_target_path)
    print(f"Unlinked {full_installed_target_path}")

def getlinkdir(target):
    print(f"Linkdir of {target} is {targets[target]}")

def showtargets():
    all_links = list(map(lambda v: v['link'], targets.values()))
    all_links = sum(all_links, [])   #flatten list
    longestlink_src = 0
    longestlink_dst = 0
    for target_link in all_links:
        if len(target_link[0]) > longestlink_src:
            longestlink_src = len(target_link[0])
        if len(target_link[1]) > longestlink_dst:
            longestlink_dst = len(target_link[1])

    for l in all_links:
        print('{1:>{0}}'.format(longestlink_src, l[0]), end='')
        print(' -> ', end='')
        print('{1:<{0}}'.format(longestlink_dst, l[1]))

# Functions for the target actions
# ====

# ====
# Peform the action based on the argparse output
if not is_platform_supported():
    print("This script is only tested for linux and macos")
    sys.exit(1)
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
