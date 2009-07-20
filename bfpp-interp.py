#!/usr/bin/python
"""
A brainfuck++ interpertor. Based on pybrain4.

TODO:
 - support all brainfuck++ operators
"""
import os
import sys
import optparse
import bfpreprocessor
import tty
import termios
import socket

class Interp():
    def __init__(self, code):
        self.cells = [0] * 30000
        self.maxint = (2 ** 8)
        self.cellpointer = 0
        self.codecursor = 0
        self.socket = None
        self.file = None
        self.code = code
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
            elif i == '.':
                sys.stdout.write(chr(self.cells[self.cellpointer]))
            elif i == ',':
                self.cells[self.cellpointer] = ord(self.getchar())
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
            elif i == '%':
                if self.socket:
                    self.socket.close()
                    self.socket = None
                else:
                    self.create_socket()
            elif i == '^':
                if self.socket:
                    self.socket.send(chr(self.cells[self.cellpointer]))
            elif i == '!':
                if self.socket:
                    try:
                        self.cells[self.cellpointer] = ord(self.socket.recv(1))
                    except (socket.error, TypeError):
                        self.cells[self.cellpointer] = 0
                else:
                    self.cells[self.cellpointer] = 0
            elif i == '#':
                print "TODO: # encountered"
            elif i == ';':
                print "; encountered"
            elif i == ':':
                print ": encountered"
            elif i == 'D':
                self.debug()
            if self.codecursor == len(self.code) - 1:
                sys.stdout.write('\n')
                break
            else:
                self.codecursor += 1

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

    def getchar(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch if ch != '\r' else '\n'

    def create_socket(self):
        addr = ""
        curcellpointer = self.cellpointer
        while self.cells[curcellpointer] != 0:
            addr = addr + chr(self.cells[curcellpointer])
            curcellpointer += 1
        (host, sep, port) = addr.partition(':')
        if not sep:
            self.cells[self.cellpointer] = self.maxint
            sys.stderr.write("parsing '%s' failed" % (addr,))
            return
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((host, int(port)))
            self.cells[self.cellpointer] = 0
        except socket.error, msg:
            self.socket.close()
            self.socket = None
            self.cells[self.cellpointer] = self.maxint
            sys.stderr.write("creating socket failed (%s,%s) : %s"
                              %(host, port, msg))


    def debug(self):
        print "Current position in the code: %d/%d" % (self.codecursor,
                                                       len(self.code))
        print "Next 5 instructions: ",
        for i in range(self.codecursor + 1, min(self.codecursor + 6, len(self.code))):
            print self.code[i],
        print ''
        print "Current pointer is %d" % (self.cellpointer,)
        print "Print cell range:"
        rng = sys.stdin.readline()
        (x, sep, y) = rng.partition('-')
        if sep:
            try:
                x = int(x)
                y = int(y)
            except ValueError:
                return
            for i in range(x,y):
                print "| %d" % (self.cells[i],),
            print ''

def main():
    parser = optparse.OptionParser(usage="%prog [OPTIONS] FILE")

    parser.add_option("-d", "--debug",
                      dest="debug", default=False, action="store_true",
                      help="run the python in interactive debug mode when 'D' is encountered")
    (options, args) = parser.parse_args()

    filename = None
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    if args[0] != '-':
        filename = os.path.abspath(args[0])

    code = bfpreprocessor.preprocess(filename, options.debug)
    i = Interp(code)
    if i:
        i.run()
        return 0
    else:
        return -1

if __name__ == '__main__':
    sys.exit(main())
