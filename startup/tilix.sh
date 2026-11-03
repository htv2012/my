#!/usr/bin/env zsh

# Fix for issue https://gnunn1.github.io/tilix-web/manual/vteconfig/

if [ $TILIX_ID ] || [ $VTE_VERSION ]; then

    files=(/etc/profile.d/vte*.sh(N))
    if (( ${#files} ))
    then
      source "${files[-1]}"
    fi

fi

