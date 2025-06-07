CC = clang
CFLAGS = -Wall -g -std=c17

.PHONY: format run clean

### Run project
run: main
	./main

### Build executable
main: main.o

### Format C source code
format:
	clang-format -i -style=microsoft main.c

### Clean up files
clean:
	rm -f main.o main
