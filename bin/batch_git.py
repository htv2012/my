#!/usr/bin/env python3
import argparse
import os
import pathlib
import shlex
import subprocess


def exec_git(cmd: str, path: pathlib.Path, should_print):
    os.chdir(path)
    command = ["git"] + shlex.split(cmd)
    proc = subprocess.run(
        command,
        text=True,
        capture_output=True,
        check=False,
    )

    output = f"{proc.stderr}\n{proc.stdout}".strip()
    if should_print(output):
        print(f"\n# {path}")
        print(output)


def git_branch(path: pathlib.Path):
    exec_git(
        "branch --show-current",
        path,
        should_print=lambda output: not ("master" in output or "main" in output),
    )


def git_status(path: pathlib.Path):
    exec_git(
        "status --short",
        path,
        should_print=lambda output: output,
    )


def git_pull(path: pathlib.Path):
    exec_git(
        "pull --rebase --autostash",
        path,
        should_print=lambda output: "up to date." not in output,
    )


def git_push(path: pathlib.Path):
    exec_git(
        "push",
        path,
        should_print=lambda output: "up-to-date" not in output,
    )


def find_all_repos():
    def find_repos(root: pathlib.Path):
        return [
            path
            for path in root.glob("*")
            if path.is_dir() and (path / ".git").is_dir()
        ]

    roots = [
        pathlib.Path.home(),
        pathlib.Path("~/Projects").expanduser(),
    ]
    for root in roots:
        yield from find_repos(root)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["status", "pull", "push", "branch"])
    options = parser.parse_args()

    actions = {
        "status": git_status,
        "pull": git_pull,
        "push": git_push,
        "branch": git_branch,
    }

    action = actions[options.action]
    for path in find_all_repos():
        action(path)


if __name__ == "__main__":
    main()
