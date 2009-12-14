#!/usr/bin/python2.6

import os
import sys
import optparse
import bfpreprocessor
import tty
import termios

class Interp():
    def __init__(self, code):
        self.cells = [0] * 30000
        self.maxint = (2 ** 8) - 1
        self.cellpointer = 0
        self.codecursor = 0
        self.socket = None
        self.file = None
        self.code = code
        self.socketbuf = None
        if code == '':
           return None

    def run(self):
        while True:
            i = self.code[self.codecursor]
            if i == '+':
                if self.cells[self.cellpointer] < self.maxint:
                    self.cells[self.cellpointer] += 1
                else:
                    self.cells[self.cellpointer] = 0
            elif i == '-':
                if self.cells[self.cellpointer] == 0:
                    self.cells[self.cellpointer] = self.maxint
                else:
                    self.cells[self.cellpointer] -= 1
            elif i == '<':
                self.cellpointer -= 1
            elif i == '>':
                self.cellpointer += 1
            elif i == '[':
                if self.cells[self.cellpointer] == 0:
                    self.matchingbracket()
            elif i == ']':
                if self.cells[self.cellpointer] != 0:
                    self.matchingbracket()
            if self.codecursor == len(self.code) - 1:
                break
            else:
                self.codecursor += 1
        return (self.cellpointer, self.cells)

    def matchingbracket(self):
        if self.code[self.codecursor] == '[':
            opens = 0
            for i in range(self.codecursor, len(self.code)):
                if self.code[i] == '[':
                    opens += 1
                elif self.code[i] == ']':
                    opens -= 1
                if opens == 0:
                    self.codecursor = i
                    return
        elif self.code[self.codecursor] == ']':
            closeds = 0
            for i in range(self.codecursor, -1, -1):
                if self.code[i] == ']':
                    closeds += 1
                elif self.code[i] == '[':
                    closeds -= 1
                if closeds == 0:
                    self.codecursor = i
                    return

def bfgen(string, sep, reset, value):
    f = open('bfutils/helper.b')
    bfarr = f.readlines()
    f.close()
    for c in string:
        i = (256 + ord(c) - value) % 256
        if i:
            s = bfarr[i-1].strip()
        else:
            s = ""
        print s+sep
        if reset:
            value = 0
        else:
            value = ord(c)


def main():
    parser = optparse.OptionParser(usage="%prog [OPTIONS] STRING")

    parser.add_option("-c", "--check",
                      dest="check", default=False, action="store_true",
                      help="check helper.b")
    parser.add_option("-s", "--separator",
                      dest="sep", default="", action="store",
                      help="select the separator between each letters")
    parser.add_option("-r", "--reset",
                      dest="reset", default=False, action="store_true",
                      help="reset the case after each letter is processed")
    parser.add_option("-v", "--value",
                      dest="value", default=0, action="store",
                      help="value in the current case")
    parser.add_option("-m", "--comment",
                      dest="comment", default=False, action="store_true",
                      help="print the command line used in a comment")
    (options, args) = parser.parse_args()

    if options.check:
        f = open('bfutils/helper.b')
        x = 1
        while True:
            try:
                i = Interp(f.readline())
                if i:
                    (a,b) = i.run()
                    if (a == 0 and b[0] == x and b[1] == 0 and b[2] == 0 
                       and b[3] == 0 and b[4] == 0 and b[5] == 0):
                        print "%d OK" %(x,)
                    else:
                        print "%d FAIL %d, %d|%d|%d|%d|%d|%d" %(x,a,
                            b[0],b[1],b[2],b[3],b[4],b[5])
                    x = x + 1
                else:
                    return -1
                if x == 256:
                    f.close()
                    return 0
            except IOError, msg:
                print msg
                return -1
    else:
        if len(args) != 1:
            parser.error("incorrect number of arguments")
            return -1
        if options.comment:
            print "= helper.py " + str(sys.argv[1:])
        bfgen(args[0], options.sep, options.reset, int(options.value))

if __name__ == '__main__':
    sys.exit(main())

