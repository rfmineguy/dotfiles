#!/usr/bin/env python3

import argparse
import platform
import os
import sys

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def is_platform_supported():
    system = platform.system().lower()
    return system == "linux" or system == "darwin"

description = "Utility for symlinking/unlinking configuration files"
targets = {
    'nvim': {
        'link': [
            ('./nvim', '~/.config/nvim'),
        ]
    },
    'vim': {
        'link': [
            ('./vim/.vimrc', '~/.vimrc')
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
            ('./scripts/startdwm.sh', '~/bin/startdwm'),  ## Note: ~/bin must already exist
        ],
        'message': 'To finalize this script you must add \"exec ~/bin/startdwm\" to .xinitrc'
    },
    'xmonad': {
        'link': [
            ('./xmonad', '~/.config/xmonad')
        ],
        'warning': 'This configuration is by no means ready for use. So don\'t try to use it yet'
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
    target = targets[target]
    link_rules = target['link']
    for link in link_rules:
        system_frm_path = os.path.realpath(link[0])
        system_tgt_path = os.path.expanduser(link[1])
        if os.path.exists(system_tgt_path):
            print(f"{bcolors.FAIL} Error: \"{system_tgt_path}\" already exists on your computer. Back it up then rerun this script {bcolors.ENDC}")
            sys.exit(1)
        try:
            print(f"Creating symlink from {system_frm_path} to {system_tgt_path}")
            os.symlink(system_frm_path, system_tgt_path)
            if 'message' in target:
                print(f"Message: {target['message']}")
            if 'warning' in target:
                print(f"{bcolors.WARNING}Warning: {target['warning']}")
        except Exception as ex:
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)


def remove_symlink(target):
    link_rules = targets[target]['link']
    for link in link_rules:
        system_frm_path = os.path.realpath(link[0])
        system_tgt_path = os.path.expanduser(link[1])
        print(f"Request to remove symlink ... {target} -> {system_tgt_path}")
        if not os.path.exists(system_tgt_path):
            print(f"Error: {system_tgt_path} doesn't exist, cant remove the symlink")
            sys.exit(1)
        os.unlink(system_tgt_path)
        print(f"Unlinked {system_tgt_path}")

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

    print('{1:^{0}}'.format(longestlink_src + longestlink_dst, "Targets"))
    print("="*(longestlink_src + longestlink_dst + len(' -> ')))
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
