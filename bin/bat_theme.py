#!/usr/bin/env python3
"""Show the bat themes."""

import shutil
import subprocess


def main():
    bat = shutil.which("bat") or shutil.which("batcat")
    if bat is None:
        raise SystemExit("bat or batcat not found")

    cmd = subprocess.run([bat, "--list-themes"], text=True, capture_output=True)
    themes = cmd.stdout.splitlines()

    for theme in themes:
        subprocess.run(["clear"], shell=True)
        print(f"Theme: {theme}\n")
        subprocess.run([bat, "--theme", theme, __file__])

        print("\n")
        user_input = input("Hit Enter or q to quit:")
        if user_input == "q":
            break


if __name__ == "__main__":
    main()
