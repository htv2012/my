PATH=$(rmduppath.py $PATH)
export PATH

# Start tmux if a sentinel exists
if [[ -e /tmp/start-tmux ]]
then
    mux
fi

