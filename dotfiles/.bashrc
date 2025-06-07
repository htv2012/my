#!/bin/zsh
for script in ~/my/startup/*.sh
do
    source $script
done
host_specific=$HOME/my/etc/bashrc_${HOST:-$HOSTNAME}.sh
test -e $host_specific && source $host_specific

