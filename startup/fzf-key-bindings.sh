#!/bin/sh
# Source fzf completion and key bindings

fz() {
    if is_zsh
    then
        suffix=.zsh
    elif is_bash
    then
        suffix=.bash
    fi


    # shellcheck source=/dev/null
    if [ -d /opt/homebrew/Cellar/fzf ]
    then
        fzfVersion="$(/opt/homebrew/bin/fzf --version | awk '{print $1}')"
        . "/opt/homebrew/Cellar/fzf/$fzfVersion/shell/key-bindings$suffix" 2> /dev/null
        . "/opt/homebrew/Cellar/fzf/$fzfVersion/shell/completion$suffix" 2> /dev/null
    fi

    for d in /usr/share/doc/fzf/examples /usr/share/fzf/shell
    do
        if [ -d "$d" ]
        then
            test -e "$d/key-bindings$suffix" && . "$d/key-bindings$suffix"
            test -e "$d/completion$suffix" && . "$d/completion$suffix"
            break
        fi
    done
}

fz
if cmd_found fzf
then
    eval "$(fzf --"$(basename "$SHELL")" 2> /dev/null)" 
fi


bindkey "ç" fzf-cd-widget
