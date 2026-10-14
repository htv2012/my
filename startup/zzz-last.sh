PATH=$(rmduppath.py $PATH)
export PATH

# Start tmux if a sentinel exists
if [[ -e /tmp/start-tmux ]]
then
    mux
fi

#
# host-specific config
#
if [ "$HOST" = "nuc" ]
then
    if ! ( [ -n "$ZELLIJ_SESSION_NAME" ] || [ -n "$TMUX" ] )
    then
        echo ""
        echo ""
        echo "============================================================"
        echo "You are connecting to a NUC box"
        echo "Type mux to restore last zelij session"
        echo "or type tmux attach to restore a tmux session"
        echo "============================================================"
        echo ""
    fi
fi
