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


alias tgb='t git.branch'
alias tgls='t git.ls'
alias tgl='t git.pull'
alias tgp='t git.push'
alias tgs='t git.status'

