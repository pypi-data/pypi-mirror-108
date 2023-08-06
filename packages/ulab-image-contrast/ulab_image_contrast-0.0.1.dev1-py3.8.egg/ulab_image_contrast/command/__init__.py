import os
from ulab_image_contrast.command.console_master import ConsoleMaster
def command_line(argv=None):
    master=ConsoleMaster(argv)
    master.execute()
