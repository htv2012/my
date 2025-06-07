#!/usr/bin/env python3
"""
Update the vscode .env file
"""
import argparse
import csv
import pathlib

def ensure_exists(dir: pathlib.Path, filename: str):
    path = dir / filename
    if not path.exists():
        raise SystemExit(f"File does not exist: {path}")
    return str(path)


def main():
    """ Entry """
    parser = argparse.ArgumentParser()
    parser.add_argument("env_path", type=pathlib.Path)
    parser.add_argument("stack_id")
    options = parser.parse_args()

    # Ensure file exists
    env_path: pathlib.Path = options.env_path
    env_path.touch()

    # Read the .env file
    with open(env_path) as stream:
        reader = csv.reader(stream, delimiter="=")
        env_vars = dict(reader)

    # Ensure files exist
    stack_id = options.stack_id
    stack_dir = pathlib.Path.home() / ".testenv" / stack_id
    symbols_path = ensure_exists(stack_dir, "symbols.json")
    key_path = ensure_exists(stack_dir, "id_ed25519_testenv")
    ssh_config_path = ensure_exists(stack_dir, "ssh.cfg")

    # Update
    env_vars["stackId"] = stack_id
    env_vars["SYSTEST_SYMBOLS"] = symbols_path
    env_vars["TESTRUN_SYMBOLS"] = symbols_path
    env_vars['TESTRUN_SSHKEY'] = key_path

    # Save
    with open(env_path, "w") as stream:
        for key, value in env_vars.items():
            stream.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()