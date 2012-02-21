CC=cc

bfb: bfb.c
	${CC} -Wall -Wextra -g -ggdb -O0 -DBFPP -DBFPP_SSL bfb.c -o bfb -lcrypto -lssl

bfb.c: bfutils/bf2c.py src/*bfpp src/msg/*bfpp bfutils/bfpp.in.c
	bfutils/bf2c.py -d -c bfb.c src/bfb.bfpp

clean:
	rm bfb.c
	rm bfb
	rm bfutils/*pyc
	rm bfutils/*pyo

