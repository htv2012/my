CPPFLAGS = -Wall -Wextra -std=c++20
.PHONY: run clean format lint watch

### Project executable
main: main.cpp main.hpp
	$(CXX) $(CPPFLAGS) -o main main.cpp

### Run the project
run: main
	./main

### Clean up generated files
clean:
	rm -f main

### Format the source code
format:
	clang-format -i --style=microsoft *.cpp *.hpp

### Perform static analysis
lint:
	cppcheck --error-exitcode=1 --enable=all --suppress=missingIncludeSystem .

### Loop to wait for file being modified, then build and run
watch:
	while true; do \
		inotifywait --event modify .; \
		make format && make run; \
	done
