#!/usr/bin/env python3
import contextlib
import os
import pathlib
import shlex
import shutil
import subprocess


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


def menu(runbooks: dict):
    names = list(runbooks)
    for i, name in enumerate(names):
        print(f"{i:>2}. {name}")
    print("Enter a number, or Enter to quit")

    while (answer := input("> ").strip()) != "":
        with contextlib.suppress(ValueError, IndexError):
            index = int(answer)
            name = names[index]
            return name, runbooks[name]
    return None, None


def main():
    runbooks = get_runbooks()
    name, path = menu(runbooks)
    if path is not None:
        execute(name, path)


if __name__ == "__main__":
    main()
