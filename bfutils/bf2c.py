#!/usr/bin/env python
"""
A brainfuck(++) translator to C.

Copyright (C) 2009-2011 Boris 'billiob' Faure
This code is under the DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE Version 2


TODO:
* Do not harcode the path to bfpp.in.c
"""
import os
import sys
import optparse
import bfpreprocessor

def TranslateToC(codelist, file):
    fin = open('bfutils/bfpp.in.c', 'r')
    file.writelines(fin.readlines())
    fin.close()
    for (f,l,c) in codelist:
        file.write('/* %s:%d */\n' % (f,l))
        for op in c:
            if op == '+':
                file.write('++*ptr;                         /* + */\n')
            elif op == '-':
                file.write('--*ptr;                         /* - */\n')
            elif op == '.':
                file.write('putchar(*ptr);                  /* . */\n')
            elif op == ',':
                file.write('*ptr = getchar();               /* , */\n')
            elif op == '<':
                file.write('--ptr;                          /* < */\n')
            elif op == '>':
                file.write('++ptr;                          /* > */\n')
            elif op == '[':
                file.write('while (*ptr) {                  /* [ */\n')
            elif op == ']':
                file.write('}                               /* ] */\n')
            elif op == '%':
                file.write('bf_socket_open_close(&ptr);     /* % */\n')
            elif op == '^':
                file.write('bf_socket_send(&ptr);           /* ^ */\n')
            elif op == '!':
                file.write('bf_socket_read(&ptr);           /* ! */\n')
            elif op == '#':
                file.write('bf_file_open_close(&ptr);       /* # */\n')
            elif op == ';':
                file.write('bf_file_write(&ptr);            /* ; */\n')
            elif op == ':':
                file.write('bf_file_read(&ptr);             /* : */\n')
            elif op == 'D':
                file.write('BF_DEBUG();                     /* D */\n')
    file.write('return 0; }\n')
    file.close()

def main():
    parser = optparse.OptionParser(usage="%prog [OPTIONS] FILE")

    parser.add_option("-c",
                      dest="cfilename", action="store", type="string",
                      help="write to file a version translated to C")

    parser.add_option("-d", "--debug",
                      dest="debug", default=False, action="store_true",
                      help=" in interactive debug mode when 'D' is encountered")
    (options, args) = parser.parse_args()

    filename = None
    if len(args) != 1:
        parser.error("incorrect number of arguments")
        return -1
    if args[0] != '-':
        filename = os.path.abspath(args[0])

    if options.cfilename is not None:
        code = bfpreprocessor.preprocess2(filename, options.debug)
        f = open(options.cfilename, 'w')
        TranslateToC(code, f)

if __name__ == '__main__':
    sys.exit(main())

