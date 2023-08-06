import os
from ulab_image_contrast.command.common import getargs, print_line

MainHelpText = '''ulab-image-contrast-PYTHON 0.0.1
usage: python [subcommand] [option] [arg] 
subcommand:

'''


def command_help(options, args):
    print_line(MainHelpText)
