#!/bin/sh
lcnew() {
    leet "$@" && source /tmp/leetdir
}

lccd() {
    builtin cd leetcode || return
    cd "$(ls -d leetcode_*|fzf)"
}

