#!/bin/sh
# ============================================================================
# History
# ============================================================================

if is_bash
then
    HISTCONTROL=ignoreboth # spaces and dups
    export HISTCONTROL
    HISTFILESIZE=500
    export HISTFILESIZE
    HISTSIZE=500
    export HISTSIZE
    HISTTIMEFORMAT="%F %T  "
    export HISTTIMEFORMAT

    ha() {
        # History add: Add an entry to history
        history -s "$@"
    }
elif is_zsh
then
    bindkey '^R' history-incremental-search-backward
    HISTFILE=~/.zsh_history
    export HISTFILE
    HISTSIZE=5000
    export HISTSIZE
    SAVEHIST=5000
    export SAVEHIST
    setopt HIST_EXPIRE_DUPS_FIRST
    setopt HIST_IGNORE_DUPS
    setopt HIST_IGNORE_ALL_DUPS
    setopt HIST_IGNORE_SPACE
    setopt HIST_FIND_NO_DUPS
    setopt HIST_SAVE_NO_DUPS
    setopt appendhistory

    ha() {
        # History add: Add an entry to history
        print -s "$@"
    }
fi

h() {
    history | grep -E --color=auto "${@:-}"
}
