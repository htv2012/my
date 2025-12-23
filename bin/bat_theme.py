#!/usr/bin/env python3
"""Show the bat themes."""

import fileinput
import pathlib
import shutil
import subprocess


def get_bat_config_path(bat_exe: str):
    proc = subprocess.run([bat_exe, "--config-file"], text=True, capture_output=True)
    return proc.stdout.strip()


def ensure_config_file_exists(config_path: str):
    path = pathlib.Path(config_path)
    path.parent.mkdir(exist_ok=True)
    path.touch(exist_ok=True)


def use_theme(bat_exe: str, theme: str):
    config_path = get_bat_config_path(bat_exe)
    ensure_config_file_exists(config_path)

    found = False
    theme_option = f"--theme='{theme}'\n"
    for line in fileinput.input(config_path, inplace=True):
        if "--theme" in line and not line.strip().startswith("#"):
            found = True
            line = theme_option
        print(line, end="")

    if not found:
        with open(config_path, "a") as stream:
            _ = stream.write("\n")
            _ = stream.write(theme_option)


def main():
    bat_exe = shutil.which("batcat") or shutil.which("bat")
    if bat_exe is None:
        raise SystemExit("bat or batcat not found")

    # Get a list of themes
    cmd = subprocess.run([bat_exe, "--list-themes"], text=True, capture_output=True)
    themes = cmd.stdout.splitlines()

    # Show each theme
    for theme in themes:
        _ = subprocess.run(["clear"], shell=True)
        print(f"Theme: {theme}\n")
        cmd = [
            bat_exe,
            f"--theme={theme}",
            "--language=python",
            "--line-range=:25",
            __file__,
        ]
        _ = subprocess.run(cmd)

        print("\n")
        user_input = input("Hit Enter or q to quit, u to use:").strip().lower()
        if user_input == "q":
            break
        elif user_input == "u":
            use_theme(bat_exe, theme)
            break


if __name__ == "__main__":
    main()
