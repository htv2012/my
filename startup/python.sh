# ============================================================================
# Python
# ============================================================================
#PYTHONSTARTUP=$HOME/my/etc/pythonstartup.py
export PYTHONSTARTUP
VENV_ROOT=$HOME/.local/share/venv
export VENV_ROOT

# Tell uv to use this version
UV_PYTHON=3.13
export UV_PYTHON


alias act='source .venv/bin/activate'
alias black='ruff format'
alias isort=' ruff check --select I --fix'
alias pypath='echo $PYTHONPATH | tr : \\n'
alias venv-clean="rm -fr ${VENV_ROOT}"


nbclean() {  # Clean the Untitled* notebooks
    for root in $HOME/Projects/python_notebooks $HOME/JupyterNotebooks
    do
        if [ -d $root ]
        then
            find -name 'Untitled*.ipynb' -delete
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
    find . -name '__pycache__' -delete
}

function mkpy(){ # Creates a python project with Makefile
    mkdir "$1"
    cd "$1" || exit
    mkmake
}

function sandbox() { # Activate the sandbox virtualenv
    venv ${VENV_ROOT}/sandbox $HOME/my/etc/requirements-sandbox.txt
}


pipw() {  # Pip wrapper: use uv if available
    if cmd_found uv
    then
        uv pip "${@}"
    else
        pip install --upgrade pip
        pip "${@}"
    fi
}


pf() {  # pip freeze, with grep
    pipw freeze | grep "${@:-.}"
}

fulfill() {  # Fulfills the requirements.txt
    requirements="${1:-requirements.txt}"
    pipw install --requirement "$requirements"
}

require() { # Installs the required packages
    tr ' ' '\n' <<< "$@" >> requirements.txt
    tmp_file=$(mktemp)
    sort requirements.txt > "$tmp_file"
    mv "$tmp_file" requirements.txt
    fulfill requirements.txt
}

venv() {  # Sets up a virtual environment
    deactivate > /dev/null 2> /dev/null
    venv_dir="${1:-${VENV_ROOT}/$(basename $PWD)}"
    requirements_file="${2:-requirements.txt}"

    if [[ ! -d $venv_dir ]]
    then
        if cmd_found uv
        then
            uv venv --python python3 $venv_dir
        else
            python3 -m venv $venv_dir
        fi

        source $venv_dir/bin/activate

        if [ -e $requirements_file ]
        then
            echo "Install requirements"
            fulfill "$requirements_file"
        else
            echo "No requirements found"
        fi

        deactivate
    fi
    source $venv_dir/bin/activate
}

