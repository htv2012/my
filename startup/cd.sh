#!/usr/bin/env bash
# ============================================================================
# cd and friends
# ============================================================================
CDPATH="."
CDPATH=$(append_if_exists $CDPATH ..)
CDPATH=$(append_if_exists "$CDPATH" "$HOME")
CDPATH=$(append_if_exists "$CDPATH" "$HOME/Sync")
CDPATH=$(append_if_exists "$CDPATH" "$HOME/workspaces")
CDPATH=$(append_if_exists "$CDPATH" "$HOME/my")
CDPATH=$(append_if_exists "$CDPATH" "$HOME/my/etc")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/rust-sandbox")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-rust-cli")
CDPATH=$(append_if_exists "$CDPATH" "$SYNODRIVE")
CDPATH=$(append_if_exists "$CDPATH" "$SYNODRIVE/src")
CDPATH=$(append_if_exists "$CDPATH" ~/.CMVolumes)
CDPATH=$(append_if_exists "$CDPATH" "/media/$USER")
CDPATH=$(append_if_exists "$CDPATH" /mnt)
CDPATH=$(append_if_exists "$CDPATH" /Volumes)
CDPATH=$(append_if_exists "$CDPATH" /Volumes/Lexar/$HOST)

export CDPATH

if [ -d "${PROJECTSROOT}/python-sandbox" ]
then
    for subdir in ${PROJECTSROOT}/python-sandbox "${PROJECTSROOT}/python-sandbox/"*
    do
        if [ -d "$subdir" ]
        then
            CDPATH=$(append_if_exists "$CDPATH" "$subdir")
        fi
    done
fi

if [ -d "${PROJECTSROOT}/pytest-sandbox/src" ]
then
    CDPATH=$(append_if_exists "$CDPATH" "${PROJECTSROOT}/pytest-sandbox/src")
fi

if [ -d "${PROJECTSROOT}/interview-questions" ]
then
    for subdir in "${PROJECTSROOT}/interview-questions/"*
    do
        if [ -d "$subdir" ]
        then
            CDPATH=$(append_if_exists "$CDPATH" "$subdir")
        fi
    done
fi


function _find_and_source() {
    curdir=$PWD
    while [[ $curdir != "/" ]]
    do
        if [[ -e "$curdir/$1" ]]
        then
            # shellcheck source=/dev/null
            source "$curdir/$1"
            return
        fi
        curdir=$(dirname "$curdir")
    done
}

# When cd into a directory, we execute the .enter.sh script if found.
# Likewise, executing .exit.sh if exiting
cd() {
    _find_and_source .exit.sh
    builtin cd "$@" || return
    _find_and_source .enter.sh

    if cmd_found eza
    then
        cmd=eza
    else
        cmd="ls --color=auto"
    fi
    if [ $(ls -1 | wc -l) -lt $LINES ]
    then
        cmd="$cmd -l"
    fi
    eval $cmd
}

# cd interactive, $1=root
cdi() {
    cd "$1" || return
    cd $( ls -1 -d */ | fzf )
}

if is_bash
then
    shopt -s cdable_vars
elif is_zsh
then
    setopt cdablevars
    unsetopt autocd
fi

function mcd() {
    mkdir -p "$@" && cd "$@" || return
}

function up() {
    parent=$PWD
    while true
    do
        parent=$(dirname "$parent")
        directory=$(basename "$parent")
        if [ "$directory" = / ]
        then
            break
        elif [[ "$directory" = *"$1"* ]]
        then
            cd "$parent" || return
            break
        fi
    done

}

alias ..='cd ..'
alias ...='cd ../..'
alias ....='cd ../../..'
alias .....='cd ../../../..'
alias ......='cd ../../../../..'
alias cdd='cd ~/Downloads'
alias cdp='cd $PROJECTSROOT'
alias cdpath='showpath.py $CDPATH'
alias cds='cd startup'

# Some destinations
alias cdm='cd $HOME/my'
alias cdw='cd workspaces; ls -l'

cdpy() { # Navigate the python-sandbox dirs
    cd python-sandbox || return
    if [ "$1" = "." ]
    then
        return
    elif [ -n "$1" ]
    then
        cd $(find . -mindepth 1 -maxdepth 4 -type d | grep "$1" | fzf)
    else
        cd $(find . -mindepth 1 -maxdepth 4 -type d | fzf)
    fi
}


# Mark the current location so we can go to it later
# perhaps from a different window
# here=mark, there=goto
here() {
    bindir="$HOME/.local/bin"
    test -d "$bindir" || mkdir -p "$bindir"
    echo cd \"$PWD\" > "$bindir/there"
    chmod +x "$bindir/there"
}
alias there='source $HOME/.local/bin/there'


