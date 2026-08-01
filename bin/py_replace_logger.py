#!/usr/bin/env python3
"""
Replace logging.debug with logger.debug
"""
import fileinput
import logging

logging.basicConfig(level="WARNING")
logger = logging.getLogger()


def main():
    with fileinput.input(inplace=True) as infile:
        for line in infile:
            line = line.rstrip()
            if line.startswith("import logging"):
                print(line)
                print("\nlogger = logging.getLogger()")
            elif "logging." in line:
                logger.debug(f"Found: {line}")
                line = line.replace("logging.", "logger.")
                print(line)
            else:
                print(line)


if __name__ == "__main__":
    main()
