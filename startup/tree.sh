#!/usr/bin/env bash

# Tree with custom options tco
tco() {
    tree \
        -I build \
        -I .git \
        -I htmlcov \
        -I __pycache__ \
        -I .pytest_cache \
        -I .ruff_cache \
        -I .venv \
        --gitignore \
        "$@"
}

3() {
    if [ -e "Cargo.toml" ]
    then
        # Rust project dir
        tco -I target "$@"
    elif [ -e "pyproject.toml" ]
    then
        # Python project dir
        tco -I dist "$@"
    else
        tco "$@"
    fi
}

alias 3d='3 -d'
alias 3py="3 -P '*.py'"
