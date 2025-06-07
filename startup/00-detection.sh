#!/bin/sh

kernel_name=$(uname -s)

case "$kernel_name" in
    Darwin)
        shell_name=$(basename "$(dscl . -read "$HOME" UserShell | awk '{print $2}')")
        ;;
    Linux)
        shell_name=$(basename "$SHELL")
        ;;
esac


cmd_found() {  # Detects if a command is found in the path
    which "$1" > /dev/null 2>&1
}

is_bash() {  # Login shell is bash
    test "$shell_name" = "bash"
}

is_zsh() {  # Login shell is zsh
    test "$shell_name" = "zsh"
}

is_darwin() {  # Detects macOS
    test "$kernel_name" = "Darwin"
}

is_linux() {  # Detects Linux
    test "$kernel_name" = "Linux"
}

is_kitty() {  # Detects kitty terminal
    test -n "$KITTY_WINDOW_ID"
}

