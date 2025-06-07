_testtool_completion() {
    local cur=${COMP_WORDS[COMP_CWORD]}
    if [[ $COMP_CWORD -eq 1 ]]; then
        COMPREPLY=( $(compgen -W "database equipment run settings tests" -- $cur) )
    fi
    if [[ $COMP_CWORD -eq 2 ]] && [[ ${COMP_WORDS[1]} = 'equipment' ]]; then
        COMPREPLY=( $(compgen -W "dump export list verify" -- $cur) )
    fi
    if [[ $COMP_CWORD -eq 2 ]] && [[ ${COMP_WORDS[1]} = 'tests' ]]; then
        COMPREPLY=( $(compgen -W "dump list verify" -- $cur) )
    fi
    # database
    if [[ $COMP_CWORD -ge 2 ]] && [[ ${COMP_WORDS[1]} = "database" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help" -- $cur) )
    fi
    # equipment dump
    if [[ $COMP_CWORD -ge 3 ]] && [[ ${COMP_WORDS[1]} = "equipment" ]] && [[ ${COMP_WORDS[2]} = "dump" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -e --equipment" -- $cur) )
    fi
    # equipment export
    if [[ $COMP_CWORD -ge 3 ]] && [[ ${COMP_WORDS[1]} = "equipment" ]] && [[ ${COMP_WORDS[2]} = "export" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -e --equipment" -- $cur) )
    fi
    # equipment list
    if [[ $COMP_CWORD -ge 3 ]] && [[ ${COMP_WORDS[1]} = "equipment" ]] && [[ ${COMP_WORDS[2]} = "list" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -e --equipment -t --tests -s --suites -c --config --setting --env -d --debug --tool-debug -n --name" -- $cur) )
    fi
    # equipment verify
    if [[ $COMP_CWORD -ge 3 ]] && [[ ${COMP_WORDS[1]} = "equipment" ]] && [[ ${COMP_WORDS[2]} = "verify" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -e --equipment -t --tests -s --suites -c --config --setting --env -d --debug --tool-debug -n --name" -- $cur) )
    fi
    # run
    if [[ $COMP_CWORD -ge 2 ]] && [[ ${COMP_WORDS[1]} = "run" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help --no-verify -t --tests -s --suites -c --config --setting --env -d --debug --tool-debug -n --name -l --log --log-disable --log-dir -p --purpose --run-start --repeat-count --repeat-time --repeat-forever --repeat-period --repeat-on-ef --pdb --run-sequence --random-seed -e --equipment --db --group --email --to-address -T --trigger" -- $cur) )
    fi
    # settings
    if [[ $COMP_CWORD -ge 2 ]] && [[ ${COMP_WORDS[1]} = "settings" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -t --tests -s --suites -c --config --setting --env -d --debug --tool-debug -n --name -l --log --log-disable --log-dir -p --purpose --run-start --repeat-count --repeat-time --repeat-forever --repeat-period --repeat-on-ef --pdb --run-sequence --random-seed" -- $cur) )
    fi
    # tests dump
    if [[ $COMP_CWORD -ge 3 ]] && [[ ${COMP_WORDS[1]} = "tests" ]] && [[ ${COMP_WORDS[2]} = "dump" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -t --tests -s --suites -c --config --setting --env -d --debug --tool-debug -n --name -e --equipment" -- $cur) )
    fi
    # tests list
    if [[ $COMP_CWORD -ge 3 ]] && [[ ${COMP_WORDS[1]} = "tests" ]] && [[ ${COMP_WORDS[2]} = "list" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -t --tests -s --suites -c --config --setting --env -d --debug --tool-debug -n --name -p --purpose --run-start --repeat-count --repeat-time --repeat-forever --repeat-period --repeat-on-ef --pdb --run-sequence --random-seed -l --log --log-disable --log-dir" -- $cur) )
    fi
    # tests verify
    if [[ $COMP_CWORD -ge 3 ]] && [[ ${COMP_WORDS[1]} = "tests" ]] && [[ ${COMP_WORDS[2]} = "verify" ]]; then
        COMPREPLY=( $(compgen -o default -W "-h --help -t --tests -s --suites -c --config --setting --env -d --debug --tool-debug -n --name -e --equipment --db --group -T --trigger" -- $cur) )
    fi

}
complete -F _testtool_completion testtool.py
