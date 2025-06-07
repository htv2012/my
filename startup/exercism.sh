#!/bin/sh
if [ -e /opt/homebrew/bin/exercism ]
then
    alias xc=/opt/homebrew/bin/exercism
else
    alias xc=exercism
fi

