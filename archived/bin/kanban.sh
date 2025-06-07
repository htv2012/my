#!/usr/bin/env bash

# Create a vim-based Kanban system

KANDIR=~/.kanban
if ! [[ -d $KANDIR ]]
then
    mkdir $KANDIR
    printf "BACKLOG\n=======\n\n" > $KANDIR/1-backlog.txt
    printf "DOING\n=====\n\n" > $KANDIR/2-doing.txt
    printf "DONE\n====\n\n" > $KANDIR/3-done.txt
fi

vim -O $KANDIR/*
