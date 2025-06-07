#!/usr/bin/env bash
# ======================================================================
# Script to start a tmux session with multiple panes
# ======================================================================

SESSION_NAME=${1:-tux}

if ! tmux has-session -t $SESSION_NAME 2> /dev/null
then
    if [[ -n $TMUX ]]
    then
        echo Please detach before running this script
        exit
    fi

    # Create a new session and a window
    tmux new-session -s $SESSION_NAME -n main -d

    # Create the additional panes
    tmux select-window -t main           # Go to window 0
    tmux split-window -v -l 30% -t main   # Split to make top/bottom panes
    tmux select-pane -t 0                # Go to pane 0
    tmux split-window -h -l 65 -t main   # Split to make 2 side-by-side panes
fi

if [[ -n $TMUX ]]
then
    tmux -u switch-client -t $SESSION_NAME  # Inside a session, switch to it
else
    tmux attach -t $SESSION_NAME            # Not inside any session, attach
fi

