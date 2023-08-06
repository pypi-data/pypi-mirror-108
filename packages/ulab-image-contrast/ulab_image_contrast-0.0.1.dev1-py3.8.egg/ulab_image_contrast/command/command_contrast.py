from ulab_image_contrast.command.common import getargs, print_line
import os
import sys
from ulab_image_contrast.core.ssim import ssim


def command_contrast(options, args):
    print(options.original)
    print(options.modified)
    ssim(options.original, options.modified)
