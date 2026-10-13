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
if [ "$HOST" = "nuc" ] && [ -z "$ZELLIJ_SESSION_NAME" ]
then
    echo ""
    echo ""
    echo "============================================================"
    echo "You are connecting to a NUC box"
    echo "Type mux to restore last zelij session"
    echo "============================================================"
    echo ""
fi
