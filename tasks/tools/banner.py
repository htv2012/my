from fabric import Connection


def banner(c: Connection, text: str):
    host = getattr(c, "original_host", "")
    if host:
        host += ":"
    print()
    print("# ======================================================================")
    print(f"# {host}{text}")
    print("# ======================================================================")
