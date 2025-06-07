#!/bin/sh
# ============================================================================
# Editor
# ============================================================================
for editor in nvim vim nano
do
    if cmd_found $editor
    then
        export EDITOR="$editor"
        export VISUAL="$editor"
        break
    fi
done

# Edit the editor init/rc file
vv() {
    if [ "$EDITOR" = "nvim" ]
    then
        nvim ~/.config/nvim/init.lua
    else
        vim ~/.vimrc
    fi
}

