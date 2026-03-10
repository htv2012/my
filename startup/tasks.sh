#!/bin/sh


t() {
    fab -r $HOME/my/tasks "$@"
}

# Start work session
hi(){
    t git.pull
}

# Finished work session
eod(){
    t git.push
}


