#!/bin/zsh
for script in ~/myenv/startup/*.sh
do
    source $script
done
host_specific=$MYENV/etc/bashrc_${HOST:-$HOSTNAME}.sh
test -e $host_specific && source $host_specific

