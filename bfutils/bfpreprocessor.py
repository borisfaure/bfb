"""Preprocesses brainfuck sourcecode.

The preprocessor performs comment removal and pretty-printing of brainfuck
source code. It also implements an include statement for building programs
from multiple source files.

The include statement is expected to appear alone on a single line and
be on the form

 @include(FILENAME)

where FILENAME is the path of the file to include. The path must be absolute
or relative to the file holding the include statement.

"""

import sys
import re
import os


def preprocess(filename, debug = False):
    include_re = re.compile(r'\s*@include\(([^)]+)\)')
    if debug:
        BFIS = set([',','.','-','+','[',']','<','>','#',';',':','%','^','!','D'])
    else:
        BFIS = set([',','.','-','+','[',']','<','>','#',';',':','%','^','!'])
    if filename:
        file = open(filename,"r")
        directory = os.path.split(filename)[0]
    else:
        file = sys.stdin
        directory = os.getcwd()

    data = []
    for line in file:
        if len(line) != 0:
            m = include_re.match(line)
            if m:
                line = preprocess(os.path.join(directory, m.group(1)), debug)
            (line, sep, ignore) = line.partition('=')
            data.append(''.join(c for c in line if c in BFIS))
    return ''.join(data)


def preprocess2(filename, debug = False):
    """ Preprocess the brainfuck code, with debugging in mind
        The object returned is a list of tuples (f, l, c) where:
        f(string) current filename
        l(int) current line number
        c(list of char) brainfuck code of the current line
    """
    linenbr = 0
    include_re = re.compile(r'\s*@include\(([^)]+)\)')
    if debug:
        BFIS = set([',','.','-','+','[',']','<','>','#',';',':','%','^','!','D'])
    else:
        BFIS = set([',','.','-','+','[',']','<','>','#',';',':','%','^','!'])
    if filename:
        file = open(filename, "r")
        directory = os.path.split(filename)[0]
    else:
        filename = "STDIN"
        file = sys.stdin
        directory = os.getcwd()

    data = []
    for line in file:
        if len(line) != 0:
            m = include_re.match(line)
            if m:
                l = preprocess2(os.path.join(directory, m.group(1)), debug)
                if l:
                    data.extend(l)
            else :
                (line, sep, ignore) = line.partition('=')
                ops = ''.join(c for c in line if c in BFIS)
                if ops:
                    data.append((filename, linenbr, ops))
        linenbr = linenbr + 1
    return data
