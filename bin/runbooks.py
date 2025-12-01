#!/usr/bin/env python3
import os
import pathlib
import shlex
import shutil
import subprocess

import termlib


def execute(name: str, path: pathlib.Path):
    print(f"\n\n{name}\n{len(name) * '='}\n")

    if os.access(path, os.X_OK):
        target = shlex.quote(str(path))
        subprocess.run([target], shell=True)
    else:
        cmd = shutil.which("bat") or "less"
        subprocess.run([cmd, str(path)])


def get_runbooks():
    root = pathlib.Path("~/my/runbooks").expanduser()
    assert root.is_dir()

    # runbooks is a dict of {name: path}
    runbooks = dict(
        sorted(
            (str(path.relative_to(root)), path)
            for path in root.rglob("*")
            if path.is_file() and "/." not in str(path)
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
