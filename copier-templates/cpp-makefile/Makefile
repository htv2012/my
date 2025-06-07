CPPFLAGS = -Wall -Wextra -std=c++20
.PHONY: run clean format

# The first target is always to build
main: main.cpp

run: main
	./main

clean:
	rm -f main

format:
	clang-format -i --style=microsoft *.cpp
