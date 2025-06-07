#!/usr/bin/env python3
"""
Open a path using web UI.
"""
import argparse
import pathlib
import shlex
import subprocess
import webbrowser


def get_output(cmd):
    """Execute a command and return output."""
    cmd = shlex.split(cmd)
    completed_process = subprocess.run(
        cmd, encoding="utf-8", stdout=subprocess.PIPE, check=False
    )
    return completed_process.stdout.strip()


def main():
    """Open a path using web UI."""
    # Parses command line
    parser = argparse.ArgumentParser()
    parser.add_argument("path")
    options = parser.parse_args()

    # Get the Git root
    root = pathlib.Path.cwd()
    while not (root / ".git").is_dir():
        root = root.parent

    # Calculate the path relative to root
    path = pathlib.Path(options.path).resolve()
    path = path.relative_to(root)

    # Get the branch
    branch = get_output("git branch --show-current")

    # Get the Web URL
    url = get_output("git remote get-url origin")
    url = url.replace("git@", "").replace(".git", "").replace(":", "/")
    url = f"https://{url}/-/blob/{branch}/{path}"

    # Open the web UI
    webbrowser.open(url)


if __name__ == "__main__":
    main()
