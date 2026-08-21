#!/bin/sh
leet-create() {
    leet "$@" && source /tmp/leetdir
}

leet-cd() {
    builtin cd leetcode || return
    cd "$(ls -d leetcode_*|fzf)"
}

