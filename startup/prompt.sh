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
    autoload -Uz vcs_info
    precmd_vcs_info() { vcs_info }
    precmd_functions+=( precmd_vcs_info )
    setopt prompt_subst
    RPROMPT='${vcs_info_msg_0_}'
    # %r=root, %b=branch, %u=unstaged changes
    zstyle ':vcs_info:git:*' formats "[%r:%b:%u]"

    PROMPT="
%F{yellow}%n@%m %F{green}%8~%F{red}%(?.. !%?)
%F{green}%#%f "
fi
