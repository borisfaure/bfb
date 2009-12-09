CC=clang

bfb: bfb.c
	${CC} -Wall -Wextra -g -ggdb -O0 -DBFPP -DBFPP_SSL bfb.c -o bfb -lssl

bfb.c: src/*b bfutils/bfpp.in.c
	bfutils/bf2c.py -d -c bfb.c src/bfb.b

clean:
	rm bfb.c
	rm bfb
	rm bfutils/*pyc
	rm bfutils/*pyo

