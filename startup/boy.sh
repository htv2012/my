#!/bin/sh
boy() {
    rm -f /tmp/boy.sh
    boy.py "$@"
    test -e /tmp/boy.sh && . /tmp/boy.sh
}