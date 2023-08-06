import sys
import os
from argparse import ArgumentParser
from ulab_image_contrast.command.command_contrast import command_contrast
from ulab_image_contrast.command.command_help import command_help


class ConsoleMaster:
    def __init__(self, argv=None):
        self.argv = argv or sys.argv[:]
        self.prog_name = os.path.basename(self.argv[0])
        if self.prog_name == '__main__.py':
            self.prog_name = 'python -m ulab-image-contrast'
        self.settings_exception = None

    def execute(self):
        try:
            subcommand = self.argv[1]
        except IndexError:
            subcommand = 'help'  # Display help if no arguments were given.
        parser = CommandParser(None, usage="%(prog)s subcommand [options] [args]", add_help=False)
        parser.add_argument('--settings')
        parser.add_argument('--original')
        parser.add_argument('--modified')
        parser.add_argument('--output_report_dir')
        parser.add_argument('args', nargs='*')  # catch-all
        try:
            options, args = parser.parse_known_args(self.argv[2:])
            # print(options,args)
        except CommandError:
            pass  # Ignore any option errors at this point.
        self.runscipt(subcommand, options, args)

    def runscipt(self, subcommand, options, args):
        if subcommand == 'help':
            command_help(options, args)
        elif subcommand == 'contrast':
            command_contrast(options, args)
        else:
            pass


class CommandError(Exception):
    """
    Exception class indicating a problem while executing a management
    command.

    If this exception is raised during the execution of a management
    command, it will be caught and turned into a nicely-printed error
    message to the appropriate output stream (i.e., stderr); as a
    result, raising this exception (with a sensible description of the
    error) is the preferred way to indicate that something has gone
    wrong in the execution of a command.
    """
    pass


class CommandParser(ArgumentParser):
    """
    Customized ArgumentParser class to improve some error messages and prevent
    SystemExit in several occasions, as SystemExit is unacceptable when a
    command is called programmatically.
    """

    def __init__(self, cmd, **kwargs):
        self.cmd = cmd
        super().__init__(**kwargs)

    def parse_args(self, args=None, namespace=None):
        # Catch missing argument for a better error message
        if (hasattr(self.cmd, 'missing_args_message') and
                not (args or any(not arg.startswith('-') for arg in args))):
            self.error(self.cmd.missing_args_message)
        return super().parse_args(args, namespace)

    def error(self, message):
        if self.cmd._called_from_command_line:
            super().error(message)
        else:
            raise CommandError("Error: %s" % message)
