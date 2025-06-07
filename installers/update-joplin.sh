#!/bin/bash
# Script to update Joplin app on Linux

if [[ $(uname) = "Linux" ]]
then
    echo Install or Update Joplin on Linux
    wget -O - https://raw.githubusercontent.com/laurent22/joplin/dev/Joplin_install_and_update.sh | bash
else
    echo Unknown platform
fi
