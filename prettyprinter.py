#!/usr/bin/python
# -*- coding: utf-8 -*-

"""Simple brainfuck preprocessor.


By default, pretty-printing consists printing the preprocessed code with a
78-character line width. Optionally, a format file describing a more
elaborate formatting of the stripped code can be specified. If so, the
content of the format file is printed with the i:th non-whitespace character
replaced with the i:th brainfuck instruction from the stripped source code.


2008-03-23
Mats Linander
"""

import sys
import re
import optparse
import os
import bfpreprocessor

def format(code, width=78, formatfile=None):
    """Formats code for pretty-printing."""

    output = []

    clen, i = len(code), 0
    if formatfile:
        for f in open(formatfile).read():
            if i >= clen:
                break
            if f.isspace():
                output.append(f)
            else:
                output.append(code[i])
                i += 1
    return '\n'.join([''.join(output)] +
                     [code[j:j+width] for j in xrange(i, clen, width)] +
                     ['\n'])

def main():
    parser = optparse.OptionParser(usage="%prog [options] FILE")
    parser.add_option("-t", "--format",
                      dest="format", metavar="F", default=None,
                      help="write output according to format in file F")
    parser.add_option("-w", "--width",
                      dest="width", type="int", metavar="W",default=78,
                      help="write output using line width W (default 78)")
    (options, args) = parser.parse_args()

    filename = None
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    if args[0] != '-':
        filename = os.path.abspath(args[0])

    code = bfpreprocessor.preprocess(filename)
    sys.stdout.write(format(code, options.width, options.format))

    return 0

if __name__ == "__main__":
    sys.exit(main())
