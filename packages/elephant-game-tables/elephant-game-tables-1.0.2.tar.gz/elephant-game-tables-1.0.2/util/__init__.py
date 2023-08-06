import sys

from util.options import CommandOptions


def get_command_options_of(option_configs):
    command_args = sys.argv[1:]
    new_command_options = CommandOptions.create_command_options(option_configs)
    new_command_options.parse_args(command_args)
    return new_command_options
