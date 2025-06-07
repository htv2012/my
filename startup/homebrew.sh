#!/bin/sh

if [ -d "/opt/homebrew" ]
then
    export HOMEBREW_PREFIX="/opt/homebrew"
    export HOMEBREW_CELLAR="$HOMEBREW_PREFIX/Cellar"
    export MANPATH="/opt/homebrew/share/man${MANPATH+:$MANPATH}:"
    export INFOPATH="/opt/homebrew/share/info:${INFOPATH:-}"
elif [ -d "/usr/local/homebrew" ]
then
    export HOMEBREW_PREFIX="/usr/local/homebrew"
    export HOMEBREW_CELLAR="/usr/local/Cellar"
    export MANPATH="/opt/homebrew/share/man${MANPATH+:$MANPATH}:"
    export INFOPATH="/opt/homebrew/share/info:${INFOPATH:-}"
fi


export HOMEBREW_REPOSITORY="$HOMEBREW_PREFIX"

