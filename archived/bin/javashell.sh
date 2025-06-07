#!/usr/bin/env bash

#
# Start jshell with custom CLASSPATH
# Host: giadinh
#

function javaenv() {
    action=${1:-on}

    if [ $action = "on" ] && [ -z "$JAVAENV" ]
    then

        OLD_CLASSPATH=$CLASSPATH
        JAVAENV=1

        export CLASSPATH=$HOME/src/java

        libdir=$HOME/src/java/lib
        for jar in $libdir/*.jar .
        do
            CLASSPATH=$CLASSPATH:$jar
        done

    elif [ $action =  "off" ]
    then

        export CLASSPATH=$OLD_CLASSPATH
        unset JAVAENV
        unset OLD_CLASSPATH

    fi

    tr : \\n <<<$CLASSPATH
}

javaenv on
jshell PRINTING

