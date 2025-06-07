#!/usr/bin/env bash
# whatis: Format and static analysys on dirty python modules
git status -s | while read -r status filename
do
    if [[ $status != "D" ]] && [[ ${filename:-3} = ".py" ]]
    then
        echo
        echo "===================================================================="
        echo "$filename"
        echo "===================================================================="
        pycheck "$filename"
    fi
done

