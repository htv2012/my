#!/usr/bin/env python3
import argparse
import logging
import os
import pathlib
import shutil
import subprocess

import termlib

logging.basicConfig(level=os.getenv("LOGLEVEL", "WARNING"))


def main():
    """Entry"""
    # On some system, the `bat` command is called `batcat`
    bat_command = shutil.which("batcat") or shutil.which("bat") or "cat"

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--edit", default=False, action="store_true")
    parser.add_argument(
        "-p", "--paging", default="always", choices=["never", "auto", "always"]
    )
    parser.add_argument("file", nargs="?", default="", type=str.lower)
    options = parser.parse_args()
    logging.debug("options=%r", options)

    # Use the options.file to come up with a list of candidates
    boy_dir = pathlib.Path("~/myenv/etc/boy").expanduser()
    assert boy_dir.exists()
    candidates = [
        path.name for path in boy_dir.glob("*") if options.file in path.name.lower()
    ]
    logging.debug("candidates=%r", candidates)
    filename = termlib.user_select(candidates)

    # Display or edit the file
    file_path = str(boy_dir / filename)
    if options.edit:
        subprocess.run([os.getenv("EDITOR", "vim"), file_path])
    else:
        subprocess.run([bat_command, "--paging", options.paging, file_path])

    # Create script to inject command to the shell's history
    history_script_path = pathlib.Path("/tmp/boy.sh")
    history_script_path.write_text(f"print -s boy {pathlib.Path(file_path).name}\n")


if __name__ == "__main__":
    main()
