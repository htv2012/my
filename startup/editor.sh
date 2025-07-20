#!/bin/sh
# ============================================================================
# Editor
# ============================================================================
if [ -e /opt/nvim-linux-x86_64/bin/nvim ]
then
    PATH=$(append_if_exists "$PATH" /opt/nvim-linux-x86_64/bin)
fi

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

