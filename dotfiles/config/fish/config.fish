if status is-interactive
    fish_add_path -m /opt/homebrew/bin

    # Commands to run in interactive sessions can go here
    zoxide init fish | source

    # git
    abbr --add ga 'git add'
    abbr --add gb 'git branch'
    abbr --add gc 'git commit'
    abbr --add gcmsg 'git commit -m'
    abbr --add gco 'git checkout'
    abbr --add gd 'git diff'
    abbr --add gl 'git pull'
    abbr --add gp 'git push'
    abbr --add gs 'git status'
end
