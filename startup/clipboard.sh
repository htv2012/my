if [ "$XDG_SESSION_TYPE" = "wayland" ]
then
    alias pbcopy=wl-copy
    alias pbpaste=wl-paste
elif [ "$XDG_SESSION_TYPE" = "x11" ]
then
    alias pbcopy='xsel -b'
    alias pbpaste='xsel -b'
fi

