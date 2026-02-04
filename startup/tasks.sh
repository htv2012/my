#!/bin/sh

# Start work session
hi(){
    pullall
}

# Finished work session
eod(){
    pushall
}

alias t='fab -r $HOME/my/tasks'
