cdcli() {
    cd python-rust-cli
    dest=$(for path in *; do test -d "$path" && echo "$path"; done | fzf)
    cd "$dest"
}

