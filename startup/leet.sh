#!/bin/sh
cpsolution() {
    grep -E -v 'from (nary_tree|tree|list_node) import' solution.py | xsel -b
}

cdleet() {
    cd leetcode || return
    cd *"$1"* 2> /dev/null || return
}


leet() {
    rm -f /tmp/leetdir
    leetcode.py
    # shellcheck source=/dev/null
    . /tmp/leetdir && code .
}
