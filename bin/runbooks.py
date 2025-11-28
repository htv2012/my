#!/usr/bin/env python3
import os
import pathlib
import shlex
import shutil
import subprocess

import termlib


def execute(name: str, path: pathlib.Path):
    print(f"\n\n{name}\n{len(name) * '='}\n")

    target = shlex.quote(str(path))
    if os.access(path, os.X_OK):
        subprocess.run([target], shell=True)
    else:
        cmd = shutil.which("bat") or "less"
        subprocess.run([cmd, target])


def get_runbooks():
    root = pathlib.Path("~/my/runbooks").expanduser()
    assert root.is_dir()

    # runbooks is a dict of {name: path}
    runbooks = dict(
        sorted(
            (str(path.relative_to(root)), path)
            for path in root.rglob("*")
            if path.is_file() and not path.name.startswith(".")
        )
    )
    return runbooks


def main():
    runbooks = get_runbooks()
    name = termlib.user_select(list(runbooks))
    if name is not None:
        execute(name, runbooks[name])


if __name__ == "__main__":
    main()
