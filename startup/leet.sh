#!/bin/sh
create-leet() {
    leet "$@" && source /tmp/leetdir
}

cdleet() {
    builtin cd leetcode || return
    cd *"$1"* 2> /dev/null || return
}

