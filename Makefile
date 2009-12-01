bfb: bfb.c
	gcc -g -ggdb -O0 -DBFPP -DBFPP_SSL bfb.c -o bfb -lssl

bfb.c: src/*b
	bfutils/bf2c.py -c bfb.c src/brainfuckerbot.b

clean:
	rm bfb.c
	rm bfb

