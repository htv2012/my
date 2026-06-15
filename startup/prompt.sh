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
    # 1. Load the version control system module
    autoload -Uz vcs_info
    setopt PROMPT_SUBST

    # 2. Run vcs_info before every prompt display
    precmd() { vcs_info }

    # 3. Style the output: (branch_name) with a space after it
    zstyle ':vcs_info:git:*' formats '[%b] '

    # 4. Your updated prompt
    if is_bsd
    then
        start=30
    else
        start=202
    fi
    PROMPT=$'\n'"%? $(tput setaf $start)\${vcs_info_msg_0_}%{$(tput setaf $((start + 6)))%}%n%{$(tput setaf $((start + 6)))%}@%{$(tput setaf $((start + 6)))%}%m %{$(tput setaf $((start + 12)))%}%~ %{$(tput sgr0)%}"$'\n'"%# "
fi
