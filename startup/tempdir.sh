#!/usr/bin/env bash
# Temp dir

tempdir_home=~/temp
test -d ${HOME}/temp && tempdir_home=${HOME}/temp
test -d $tempdir_home || mkdir -p $tempdir_home

function _get_temp_dest() {  # Use argument if supplied, otherwise use fzf to find the destination
    if [[ -z $1 ]]
    then
        if cmd_found fzf
        then
            find $tempdir_home -type d -not -iwholename '*/.git/*' | fzf
        else
            echo "$tempdir_home"
        fi
    else
        echo "$tempdir_home/$1"
    fi
}

function tcd() {  # cd into a temp dir, create it if needed
    local dest
    dest=$(_get_temp_dest $1)
    test -d $dest || mkdir $dest
    cd $dest
    ls
}

function tclean() {  # Clean up old dirs
    test -d "$tempdir_home" && rm -fr $(find "$tempdir_home" -mtime +60)
}

# Setup autocompletion for bash
if is_bash
then
    # Helper function to help with command autocompletion
    function _list_dirs()
    {
        local cur
        local choices
        COMPREPLY=()
        cur=${COMP_WORDS[COMP_CWORD]}
        choices=$(tls)
        COMPREPLY=($( compgen -W "$choices" -- $cur ) )
    }

    complete -F _list_dirs tcd
    complete -F _list_dirs tls
    complete -F _list_dirs tpushd
fi
