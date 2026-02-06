#!/usr/bin/env bash

# ======================================================================
# Set the Prompt, only needed for bash
# ======================================================================
if is_bash
then
    export PS1=$(ps1gen.py newline \
        "gray user at host" space \
        "brightcyan dir" space \
        "brightyellow exec git_current_branch" \
        "red exec git_dirty_marker" \
        newline bang history space "brightgreen dollar" space \
    )
elif is_zsh
then
    start=196
    PROMPT="%{$(tput setaf $start)%}%n%{$(tput setaf $((start + 6)))%}@%{$(tput setaf $((start + 12)))%}%m %{$(tput setaf $((start + 18)))%}%~ %{$(tput sgr0)%}"$'\n'"$ "
fi
