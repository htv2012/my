#!/usr/bin/env python3
"""
Manipulates vscode launch.json
"""
import argparse
import json
import pathlib
import shutil


def equipment_collate(config):
    name = config["name"]
    if name.startswith("f5-"):
        # f5-xyz-abcd -> f5-abcd-xyz for sorting
        tokens = name.split("-")
        tokens[1], tokens[2] = tokens[2], tokens[1]
        name = "-".join(tokens)
    return name


def create_config(name, app_path):
    config = {
        "name": name,
        "type": "python",
        "request": "launch",
        "program": str(app_path),
        "args": [
            "run",
            "-e",
            name,
            "-t",
            "${file}"
        ],
        "console": "integratedTerminal",
    }
    return config


def find_testtool(root):
    found = next(root.glob("**/testtool.py"), "")
    return found


def main():
    """ Entry """
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--new")
    parser.add_argument("launch_json", type=pathlib.Path)
    options = parser.parse_args()

    launch_path = options.launch_json
    backup_path = options.launch_json.with_suffix(".json.bak")
    shutil.copyfile(src=launch_path, dst=backup_path)

    with open(launch_path) as stream:
        data = json.load(stream)

    configs = data["configurations"]

    if options.new:
        root = launch_path.parent.parent.resolve()
        testtool_path = find_testtool(root)
        config = create_config(options.new, testtool_path)
        configs.append(config)

    print(f"{len(configs)} configurations")
    configs.sort(key=equipment_collate)
    for config in configs:
        print(f"- {config['name']}")

    with open(launch_path, "w") as stream:
        json.dump(data, stream, indent=4)


if __name__ == '__main__':
    main()
