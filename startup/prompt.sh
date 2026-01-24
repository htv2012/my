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
    PROMPT=$'\n'"%{$(tput setaf 39)%}%n%{$(tput setaf 45)%}@%{$(tput setaf 51)%}%m %{$(tput setaf 195)%}%~ %{$(tput sgr0)%}"$'\n'"$ "
fi
