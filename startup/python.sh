#!/usr/bin/env bash
# ============================================================================
# Python
# ============================================================================

# Tell uv to use this version
UV_PYTHON=3.13
export UV_PYTHON


alias act='source .venv/bin/activate'
alias black='ruff format'
alias ipython='uvx ipython'
alias isort=' ruff check --select I --fix'
alias pypath='echo $PYTHONPATH | tr : \\n'
alias uvt='uv tree -d1'


create-project() {
    uv init "$@"
    projectDir="${*: -1}"
    echo "projectDir=$projectDir"
    cd "$projectDir" || exit
    copier copy \
        -d script=main.py \
        -d default_target=run \
        ~/my/copier-templates/uv-package-makefile .
    uv add --dev ruff pytest ipython
}


nbclean() {  # Clean the Untitled* notebooks
    for root in $HOME/Projects/python_notebooks $HOME/JupyterNotebooks
    do
        if [ -d "$root" ]
        then
            find . -name 'Untitled*.ipynb' -delete
        fi
    done
}

if is_darwin
then
    alias whichpy='which python | tee >(pbcopy)'
elif is_linux
then
    alias whichpy='which python | tee >(xsel -b)'
fi


function pyclean() { # Cleans up all python-generated files
    find . -name '*.pyc' -delete
    find . -type d -name '__pycache__' -delete
    find . -type d -name '.venv' -exec rm -fr {} \;
}

