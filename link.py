import argparse

description = "Utility for symlinking/unlinking configuration files\n"
targets = {
    'nvim': '~/.config/nvim'
}

# ====
# Setup the argparse library
parser = argparse.ArgumentParser(description)
subparsers = parser.add_subparsers(dest='subparser', help='subcommand help')

parser_create = subparsers.add_parser('create', help='creates a symlink to a config dir for target')
parser_create.add_argument('--target', dest='target', choices=['nvim', 'qtile'], type=str, help='target help')

parser_remove = subparsers.add_parser('remove', help='removes a symlinked target')
parser_remove.add_argument('--target', dest='target', choices=['nvim', 'qtile'], type=str, help='target help')
# Setup the argparse library
# ====

# ====
# Peform the action based on the argparse output
args = parser.parse_args()
if args.subparser == 'create':
    print("Create symlink to:", args.target)
elif args.subparser == 'remove':
    print("Remove symlink to:", args.target)
# Peform the action based on the argparse output
# ====
