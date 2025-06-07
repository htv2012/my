#!/bin/sh
# ======================================================================
# Copier templates and comands
# ======================================================================

alias copy-uv-makefile='uv tool run copier copy -d script=main.py -d default_target=test ~/my/copier-templates/uv-package-makefile .'

hackerrank() {
    name=${1:?A unique project name is required}
    mkdir "$name"
    cd "$name"
    uv tool run copier copy -d project_name="$name" ~/my/copier-templates/hackerrank .
    uv sync --upgrade
    ls -lA
}


kopier() {
    template=$(builtin cd $HOME/my/copier-templates; ls -1 | fzf)
    copier copy "$HOME/my/copier-templates/$template" .
}

# Create a new copier project
create-copier-project() {
    if [ -z "$1" ]
    then
        echo "This command create a new project using copier"
        echo "Syntax"
        echo "    create-copier-project template-dir dest"
        echo "Missing the template-dir"
        return 1
    fi

    if [ -z "$2" ]
    then
        echo "This command create a new project using copier"
        echo "Syntax"
        echo "    create-copier-project template-dir dest"
        echo "Missing the dest"
        return 1
    fi

    template="$1"
    dest="$2"

    echo "Template dir: $template"
    echo "Destination:  $dest"

    mkdir -p "$dest" || return
    cd "$dest" || return
    copier copy "$template" .
}

# Create a new stackoverflfow work dir
# Syntax
#     so dir-name
so() {
    create-copier-project "$HOME/my/copier-templates/stackoverflow" "$HOME/temp/so/$1"
}

