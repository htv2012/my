#!/usr/bin/env bash
# .bash_profile
# Contains common start-up code for all hosts

SCRIPT_DIR="$( cd "$( dirname $(readlink "${BASH_SOURCE[0]}") )" >/dev/null && pwd )"

if [ -e ${HOME}/.bashrc ]
then
    source ${HOME}/.bashrc
elif [ -e $SCRIPT_DIR/.bashrc ]
then
    source $SCRIPT_DIR/.bashrc
fi
