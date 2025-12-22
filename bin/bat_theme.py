#!/usr/bin/env python3
"""Show the bat themes."""

import fileinput
import shutil
import subprocess


def get_bat_config_path():
    proc = subprocess.run([bat_exe, "--config-file"], text=True, capture_output=True)
    return proc.stdout.strip()


def use_theme(theme: str):
    config_path = get_bat_config_path()
    for line in fileinput.input(config_path, inplace=True):
        if "--theme" in line:
            line = f"--theme='{theme}'\n"
        print(line, end="")


def main():
    bat_exe = shutil.which("bat") or shutil.which("batcat")
    if bat_exe is None:
        raise SystemExit("bat or batcat not found")

    # Take a short sample of this file
    with open(__file__, "r") as stream:
        sample = stream.read(500)

    # Get a list of themes
    cmd = subprocess.run([bat_exe, "--list-themes"], text=True, capture_output=True)
    themes = cmd.stdout.splitlines()

    # Show each theme
    for theme in themes:
        subprocess.run(["clear"], shell=True)
        print(f"Theme: {theme}\n")
        cmd = [bat_exe, f"--theme={theme}", "--language=python"]
        subprocess.run(cmd, text=True, input=sample)

        print("\n")
        user_input = input("Hit Enter or q to quit, u to use:").strip().lower()
        if user_input == "q":
            break
        elif user_input == "u":
            use_theme(theme)
            break


if __name__ == "__main__":
    main()
