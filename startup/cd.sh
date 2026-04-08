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
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox/3party")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox/books")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox/LICENSE")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox/stdlib")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox/tools")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox/topics")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/python-sandbox/wip")
CDPATH=$(append_if_exists "$CDPATH" "$PROJECTSROOT/go-sandbox")
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

    if cmd_found z
    then
        z "$@" || builtin cd "$@" || return
    else
        builtin cd "$@" || builtin cd "$@" || return
    fi

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

    _find_and_source .enter.sh
    bm ~/.config/cd_history.txt
}


# cd a root dir, and optionally select a sub dir
cdroot() {
    # $1=root dir, $2=filter
    if [ -n "$2" ]
    then
        get-dirs.sh "$1" "$2"
        cd $(cat /tmp/get-dirs.out)
    else
        cd "$1"
    fi
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
alias cdg='cdroot $PROJECTSROOT/go-sandbox'
alias cdp='cdroot $PROJECTSROOT'
alias cdpath='showpath.py $CDPATH'

# Some destinations
alias cdm='cdroot $HOME/my'
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

# Select dir from stdout and go
_cd_select() {
    dest=$(sort | uniq | fzf)
    if [ -n "$dest" ]
    then
        cd "$dest" && print -s "cd $PWD"
    fi
}

# Go to a directory in history
cdh(){
    _cd_select < ~/.config/cd_history.txt
}

# Go to a bookmarked directory
cdb() {
    _cd_select < ~/.config/cd_bookmarks.txt
}

# Bookmark the current directory
bm() {
    bmFile="${1:-$HOME/.config/cd_bookmarks.txt}"
    touch "$bmFile"
    {
        pwd
        cat "$bmFile"
    } | sort | uniq > /tmp/cd_bookmarks.txt
    mv /tmp/cd_bookmarks.txt "$bmFile"
}

