#!/usr/bin/env bash

# Script to rename files
#
# Syntax:
#
#   rn [ -e SED-EXPRESSION ... ] [ -x ] files ...

# Help
function usage(){
    me=$(basename "$0")
    echo "Syntax: $me -e SED-EXPRESSION [ -x ] files ..."
    exit 1
}

if [[ $# -eq 0 ]]
then
    usage
fi

execute=0
transformations=()
while getopts "e:xh" flag
do
    if [[ $flag = "e" ]]
    then
        transformations=("${transformations[@]}" -e "$OPTARG")
    elif [[ $flag = "x" ]]
    then
        execute=1
    elif [[ $flag = "h" ]]
    then
        usage
    fi
done

shift $((OPTIND-1))

# Check the last argument for excecution

for old_name
do
    new_name=$(sed "${transformations[@]}" <<< "$old_name")

    if [[ $new_name != "$old_name" ]]
    then
        if [[ $execute == 1 ]]
        then
            mv "$old_name" "$new_name"
        else
            echo mv \""$old_name"\" \""$new_name"\"
        fi
    fi
done
