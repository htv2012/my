#!/bin/sh
# Path-related library, works with bash and zsh

TRUE=0
FALSE=1

# =============================================================================
# Returns true (0) if element is in the list, false (1) if not
# $1 = list, $2 = element
# =============================================================================
lcontains() {
    found=$FALSE
    local dir_name
    for dir_name in $(tr : " " <<< $PATH)
    do
        if [ "$2" = "$dir_name" ]
        then
            found=$TRUE
            break
        fi
    done

    return $found
}

# =============================================================================
# Appends a directory into a list only if it exists
# $1 = list, $2 = element
# =============================================================================
append_if_exists() {
    if [ -d "$2" ] && ! lcontains "$1" "$2"
    then
        echo "$1:$2"
    else
        echo "$1"
    fi
}

# =============================================================================
# Preppends into a list an element
# $1 = list, $2 = element
# =============================================================================
prepend_if_exists() {
    if [ -d "$2" ] && ! lcontains "$1" "$2"
    then
        echo "$2:$1"
    else
        echo "$1"
    fi
}

# =============================================================================
# Returns the first dir that exists in a series
# $@ =  list of directories
# =============================================================================
first_exist_dir() {
    local dir_name
    for dir_name
    do
        if [ -d "${dir_name}" ]
        then
            echo "$dir_name"
            return
        fi
    done
}

# =============================================================================
# Setting the paths
# =============================================================================
PROJECTSROOT="$(first_exist_dir ~/Projects ~/projects)"
export PROJECTSROOT
export RIPGREP_CONFIG_PATH=$HOME/my/etc/ripgreprc
SYNODRIVE="$(first_exist_dir ~/SynologyDrive ~/CloudStation)"
export SYNODRIVE

# Add Linux-specific bin
if is_linux
then
    PATH="$(append_if_exists "$PATH" "$HOME/my/bin-linux")"
    export PATH
fi

PATH=$(append_if_exists "$PATH" "/opt/homebrew/bin")
PATH=$(append_if_exists "$PATH" "/opt/homebrew/sbin")
PATH="$(append_if_exists "$PATH" "$HOME/Applications/nvim-macos/bin")"
PATH="$(append_if_exists "$PATH" "$HOME/.cargo/bin")"
PATH="$(append_if_exists "$PATH" "$HOME/.local/bin")"
PATH="$(append_if_exists "$PATH" "$HOME/local-bin")"
PATH="$(append_if_exists "$PATH" "$HOME/.local/node/bin")"
PATH="$(append_if_exists "$PATH" "$HOME/.poetry/bin")"
PATH="$(append_if_exists "$PATH" $HOME/my/bin)"
PATH="$(append_if_exists "$PATH" $HOME/my/usr/bin)"
PATH="$(append_if_exists "$PATH" "/Applications/Visual Studio Code.app/Contents/Resources/app/bin")"
PATH="$(append_if_exists "$PATH" "/opt/nvim-linux64/bin")"
PATH="$(append_if_exists "$PATH" /usr/local/go/bin)"
PATH="$(append_if_exists "$PATH" $HOME/.local/zig)"
export PATH

# Add custom Python path
if [ -d "$HOME/Library/Python" ]
then
    cd "$HOME/Library/Python" || return
    latest=$(ls | sort --version-sort | tail -1)
    cd - || return
    PATH="$(append_if_exists "$PATH" "$HOME/Library/Python/$latest/bin")"
    export PATH
fi
