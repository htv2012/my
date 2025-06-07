#!/bin/sh
# ============================================================================
# ls and friends
# ============================================================================
if cmd_found eza
then
    alias ls=eza
    alias la='ls -a'
    alias ll='ls -lh --git'
    alias lla='ls -al'
    alias ltr='ll --sort newest'
    export LS_COLORS='di=1;36:ln=1;35:so=32:pi=33:ex=1;32:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43'
elif cmd_found exa
then
    alias ls=exa
    alias la='ls -a'
    alias ll='ls -lh --git'
    alias lla='ls -al'
    alias ltr='ll --sort newest'
    export LS_COLORS='di=1;36:ln=1;35:so=32:pi=33:ex=1;32:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43'
else
    case "$kernel_name" in
        Darwin|*BSD)
            alias ls='ls -G'
            export LSCOLORS='GxFxcxdxCxegedabagacad'
            ;;
        Linux|CYGWIN*)
            alias ls='ls --color=auto'
            export LS_COLORS='di=1;36:ln=1;35:so=32:pi=33:ex=1;32:bd=34;46:cd=34;43:su=30;41:sg=30;46:tw=30;42:ow=30;43'
            ;;
    esac

    alias la='ls -A'
    alias ll='ls -hl'
    alias lla='ls -hAl'
    alias ltr='ls -lGtr'
fi

# Common
alias lld='ll -d'
alias ll.='ls -ld .*'
