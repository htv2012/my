#!/usr/bin/env python3
"""
Tools to create the bash PS1 prompt
"""

from __future__ import print_function

import os
import sys
from io import StringIO

# pylint: disable=anomalous-backslash-in-string
VALID_COLORS = {
    "black": ("\[\e[0;30m\]", ""),
    "blue": ("\[\e[0;34m\]", ""),
    "cyan": ("\[\e[0;36m\]", ""),
    "gray": ("\[\e[0;37m\]", ""),
    "green": ("\[\e[0;32m\]", ""),
    "magenta": ("\[\e[0;35m\]", ""),
    "red": ("\[\e[0;31m\]", ""),
    "white": ("\[\e[1;37m\]", ""),
    "yellow": ("\[\e[0;33m\]", ""),
    "brightblue": ("\[\e[1;34m\]", ""),
    "brightcyan": ("\[\e[1;36m\]", ""),
    "brightgreen": ("\[\e[1;32m\]", ""),
    "brightmagenta": ("\[\e[1;35m\]", ""),
    "brightred": ("\[\e[1;31m\]", ""),
    "brightyellow": ("\[\e[1;33m\]", ""),
    "colordefault": ("\[\e[0m\]", ""),
}

VALID_TOKENS = {
    "at": ("@", "At sign"),
    "bang": ("!", "Exclamation sign"),
    "cmd": ("\\#", "Command number"),
    "dir": ("\w", "The current dir"),
    "dollar": ("$", "Dollar sign"),
    "exec": ("", "Execute external command or function"),
    "gt": (">", "Greater-than sign"),
    "history": ("\\!", "History number"),
    "host": ("\\h", "Host name"),
    "lbracket": ("[", "Left square bracket"),
    "lt": ("<", "Less-than sign"),
    "newline": ("\\n", "New line"),
    "pipe": ("|", "Pipe symbol"),
    "rbracket": ("]", "Right square bracket"),
    "space": (" ", "The space"),
    "user": ("\\u", "The User alias"),
}
# pylint: enable=anomalous-backslash-in-string

COMMANDS = VALID_COLORS.copy()
COMMANDS.update(VALID_TOKENS)


def show_usage():
    """Prints the usage"""
    print("ps1gen.py - Create bash PS1 prompt")
    print("\nSYNOPSIS")
    print("    PS1=$(ps1gen.py tokens...)")
    print("\nEXAMPLE")
    print(
        '    export PS1=$(ps1gen.py "yellow user" at "cyan host" space dir dollar space)'
    )

    print("\nVALID TOKENS")
    max_token_length = max(len(k) for k in COMMANDS)
    for token, (_, desc) in sorted(VALID_TOKENS.items()):
        print("    {} - {}".format(token.ljust(max_token_length), desc))

    print("\nVALID COLORS")
    for token in sorted(VALID_COLORS):
        print("    {}".format(token))


def make_prompt(tokens):
    """Given a list of tokens, create the prompt"""
    prompt = StringIO()
    for token in tokens:
        token = token.strip()
        if token.startswith("exec"):
            command = token.replace("exec", "").strip()
            prompt.write("$({})".format(command))
        elif " " in token:
            prompt.write(make_prompt(token.split(" ", 1)))
            prompt.write(COMMANDS["colordefault"][0])
        else:
            try:
                prompt.write(COMMANDS[token][0])
            except KeyError:
                sys.stderr.write("Invalid code: {!r}\n".format(token))
                return os.getenv("PS1", "$ ")
    return prompt.getvalue()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        show_usage()
        sys.exit(1)
    print(make_prompt(sys.argv[1:]), end="")
