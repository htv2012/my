if cmd_found pastebin-cli
then
    eval "$(_PASTEBIN_CLI_COMPLETE=zsh_source pastebin-cli)"
fi
if cmd_found pinboard-cli
then
    eval "$(_PINBOARD_CLI_COMPLETE=zsh_source pinboard-cli)"
fi

