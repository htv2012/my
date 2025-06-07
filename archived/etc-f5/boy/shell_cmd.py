class ShellCmd:
    """Wrapper for a shell command."""
    cmd: str
    env: list[str]
    output: str
    rc: int
    child: Any

