#!/usr/bin/env python
"""
A brainfuck++ interpertor. Based on pybrain4.
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
                self.readFromSocket()
            elif i == '#':
                if self.file is not None:
                    self.file.close()
                    self.file = None
                else:
                    fname = ""
                    curcellpointer = self.cellpointer
                    while self.cells[curcellpointer] != 0:
                        fname = fname + chr(self.cells[curcellpointer])
                        curcellpointer += 1
                    try:
                        self.file = open(fname)
                        self.cells[self.cellpointer] = 0
                    except IOError as msg:
                        self.file = None
                        self.cells[self.cellpointer] = self.maxint
                        sys.stderr.write("opening file '%s' failed: %s"
                              %(fname, msg))
            elif i == ';':
                if self.file is not None:
                    try:
                        self.file.write(chr(self.cells[self.cellpointer]))
                    except IOError as msg:
                        self.cells[self.cellpointer] = 0
                        sys.stderr.write("error writing to file: %s" %(msg,))
            elif i == ':':
                if self.file is not None:
                    try:
                        s = self.file.read(1)
                        if len(s) == 0:
                           sys.stderr.write("error reading from file")
                           self.cells[self.cellpointer] = 0
                        else:
                           self.cells[self.cellpointer] = ord(s[0])
                    except IOError as msg:
                        self.cells[self.cellpointer] = 0
                        sys.stderr.write("error reading from file: %s" %(msg,))
            elif i == 'D':
                self.debug()
            if self.codecursor == len(self.code) - 1:
                sys.stdout.write('\n')
                break
            else:
                self.codecursor += 1

    def readFromSocket(self):
        if self.socketbuf:
            if self.socketbufpos < len(self.socketbuf):
                self.cells[self.cellpointer] = \
                    ord(self.socketbuf[self.socketbufpos])
                self.socketbufpos += 1
                return
            else:
                self.socketbuf = None
        if self.socket:
            try:
                self.socketbuf = self.socket.recv(4096)
                self.cells[self.cellpointer] = ord(self.socketbuf[0])
                self.socketbufpos = 1
            except (socket.error, TypeError):
                self.cells[self.cellpointer] = 0
                return
        else:
            self.cells[self.cellpointer] = 0

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
        l = addr.split(':')
        if len(l) < 2:
            self.cells[self.cellpointer] = self.maxint
            sys.stderr.write("parsing '%s' failed" % (addr,))
            return
        host = l[0]
        port = l[1]
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if (len(l) > 2) and (l[2] == "ssl"):
                import ssl
                self.socket = ssl.wrap_socket(self.socket)
            self.socket.connect((host, int(port)))
            self.socket.setblocking(1)
            self.cells[self.cellpointer] = 0
        except socket.error as msg:
            self.socket.close()
            self.socket = None
            self.cells[self.cellpointer] = self.maxint
            sys.stderr.write("creating socket failed (%s,%s) : %s"
                              %(host, port, msg))


    def debug(self):
        print("Current position in the code: %d/%d" % (self.codecursor,
                                                       len(self.code)))
        print("Next 5 instructions: ", end=' ')
        for i in range(self.codecursor + 1, min(self.codecursor + 6, len(self.code))):
            print(self.code[i], end=' ')
        print('')
        print("Current pointer is %d" % (self.cellpointer,))
        print("Print cell range:")
        rng = sys.stdin.readline()
        (x, sep, y) = rng.partition('-')
        if sep:
            try:
                x = int(x)
                y = int(y)
            except ValueError:
                return
            for i in range(x,y+1):
                print("| %d" % (self.cells[i],), end=' ')
            print('')

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
