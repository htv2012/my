parser = clink.arg.new_parser
local command_parser = parser({
    "ls" .. parser("--", "--verbose", "-v"),
    "wg",
    "update"
})
clink.arg.register_parser("sshconf", command_parser)
clink.arg.register_parser("sshconf.py", command_parser)
