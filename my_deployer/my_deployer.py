import argparse
from ssh import Ssh_utils
__author__ = "romana_m"


def config(args):
    """ fonction for config subcommand"""
    ssh_obj = Ssh_utils()
    ssh_obj.execute_command(ssh_obj.commands)


# create the top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "config" command
parser_config = subparsers.add_parser('config', help='launch script on remote')
parser_config.set_defaults(func=config)

# parse the args and call whatever function was selected
# can add default argument here or nothing
args = parser.parse_args()
args.func(args)
