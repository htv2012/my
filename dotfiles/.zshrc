if [[ -e "${HOME}/.iterm2_shell_integration.zsh" ]]
then
    source "${HOME}/.iterm2_shell_integration.zsh"
fi

fpath+=${ZDOTDIR:-~}/.zsh_functions

for file in ~/my/startup/*.{sh,zsh}
do
    source "$file"
done

