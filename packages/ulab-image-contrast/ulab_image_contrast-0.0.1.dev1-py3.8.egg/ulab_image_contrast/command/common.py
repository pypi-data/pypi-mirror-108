import sys


def getargs(sourse, num):
    try:
        args0 = sourse[num]
        return args0
    except IndexError:
        return None


def print_line(line: str):
    sys.stdout.write(line + '\n')
