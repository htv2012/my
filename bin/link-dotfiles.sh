#!/usr/bin/env bash

# Check for stow
if ! which stow > /dev/null 2> /dev/null
then
    echo "Need to install GNU stow before running this script"
    exit 1
else
    echo "stow found"
    exit 1
fi

src=$HOME/my/dotfiles
dest=$HOME

# home
mkdir -p "$dest"
stow --dotfiles --dir=$src --target=$dest home

# .config
mkdir -p $dest/.config
stow  --dotfiles --dir=$src --target=$dest/.config config

tree -a $dest