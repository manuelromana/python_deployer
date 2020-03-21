import argparse
from ssh import Ssh_utils
import config as config_file
__author__ = "romana_m"


def config(args):
    """ fonction for config subcommand"""
    ssh_obj = Ssh_utils()
    ssh_obj.execute_command(ssh_obj.commands)


def build(args):
    """ fonction for build subcommand"""
    ssh_copy_build = Ssh_utils()
    service = args.service
    print("choosen {} service".format(args.service))
    ssh_copy_build.build_service(args.service, config_file.CHECKER_LIST_FILES)


# create the top-level parser
parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(help='sub-command help')

# create the parser for the "config" command
parser_config = subparsers.add_parser('config', help='launch script on remote')
parser_config.set_defaults(func=config)

# create the parser for the "build" command
parser_build = subparsers.add_parser(
    'build', help='build docker image -h to get help')
parser_build.add_argument('--service', type=str,
                          help='microservice you want to build')
parser_build.set_defaults(func=build)

# parse the args and call whatever function was selected
# catch error if no command pass to script

try:
    args = parser.parse_args()
    args.func(args)
except Exception as e:
    parser.parse_args(['--help'])
