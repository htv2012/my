#!/bin/sh
# ============================================================================
# General
# ============================================================================

MANWIDTH=80
export MANWIDTH

# vi editing mode
set -o vi

if is_darwin
then
    alias cal='ncal -C'
    alias cal3='ncal -C -3'
    alias caly='ncal -C -y'
elif is_linux
then
    alias open=xdg-open
    alias pbcopy='xsel -b'
    alias pbpaste='xsel -b'

    if cmd_found ncal
    then
        alias cal='ncal -b'
        alias cal3='ncal -3 -b'
        alias caly='ncal -y -b'
    elif cmd_found cal
    then
        alias cal3='cal -3'
        alias caly='cal -y $(date "+%Y")'
    fi
fi

alias cheat=cht.sh
alias path='showpath.py $PATH'
alias ping3='ping -c3'
alias reshell='exec $SHELL'

# Table: script to show csv file
alias table='uv run $HOME/myenv/bin/table.py'

first_exist() {  # Find first tool that exists
    for tool
    do
        if cmd_found $tool
        then
            echo $tool
            return
        fi
    done
}

# Displays environment variables with optional search capability
e(){
    printenv | grep -E --color=auto -i "${@:-.}"
}

vs() {  # Edit, then source
    script=$1
    if [ -z "$script" ]
    then
        script=$(find "$MYENV/startup" -type f | fzf)
    fi
    # shellcheck source=/dev/null
    $EDITOR "$script" && . "$script"

    # Inject the command into the shell's history
    print -s vs "$script"
}

# Ignore extensions for bash completion
export FIGNORE=".pyc:.class"

x() {  # Touch a file and make it executable
    touch "$@"
    chmod +x "$@"
}
