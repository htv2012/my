#!/usr/bin/env bash

# ======================================================================
# Add Blank lines to separate blocks of text so we can format them
# ======================================================================
function add_blank_lines() {
    awk '$1 ~ /^:/ && last != "" { print "" }; { print; last=$0 }' ${1:--}
}

# ======================================================================
# Create hanging indent for lines under the :param: or :return: lines
# ======================================================================
function hanging_indent() {
    awk '$1 ~ /^:/ { print; indent = "    "; next }; /^$/ { indent = "" } { print indent $0 }'
}

# ======================================================================
# Delete blank lines before param lines
# ======================================================================
function delete_blank_lines() {
    awk '$1 ~ /^:/ { swallow=1 }; /^$/ && swallow==1 { next }; 1'
}

# ======================================================================
# Main
# ======================================================================
add_blank_lines "$@" | fmt | hanging_indent | fmt | delete_blank_lines
