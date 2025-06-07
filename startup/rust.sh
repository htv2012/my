# Rust-related functions and aliases. They have "rs" prefix

cdrust() {  # Navigate the rust-sandbox dirs
    # rscd:    To rust-sandbox
    # rscd [partial name]: Use fzf to select dir
    cd rust-sandbox || return
    if [ "$1" = "." ]
    then
        return
    elif [ -n "$1" ]
    then
        cd $(find . -mindepth 1 -type d -exec test -d '{}/src' \; -print | grep "$1" | fzf)
    else
        cd $(find . -mindepth 1 -type d -exec test -d '{}/src' \; -print | fzf)
    fi
}

rsnew() {  # Create a new project
    cargo new "${1:?Please supply a directory}" || return
    cd "$1"
    $EDITOR src/main.rs
    cargo run -q
}

rscat() {  # cat the contents of main.rs
    echo bat "${1:-.}/src/main.rs"
    bat "${1:-.}/src/main.rs"
}

rse() {  # Edit a rust source
    file=$(find -name '*.rs' | fzf)
    if [ -e "$file" ]
    then 
        $EDITOR "$file"
        # Inject to history
        print -s $EDITOR "$file"
    fi
}

alias rs='make -f $HOME/my/etc/Makefile.rust'
