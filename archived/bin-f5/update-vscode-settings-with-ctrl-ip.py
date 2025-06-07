#!/usr/bin/env python3
"""Update qe/.vscode/settings.json based on new testenv stack."""
import json
import os
import pathlib


def load_symbols():
    stack_id = os.getenv("stackId")
    assert stack_id is not None, "Environment variable stackId is not defined"
    symbols_path = pathlib.Path(f"~/.testenv/{stack_id}/symbols.json").expanduser()
    assert symbols_path.exists(), f"{symbols_path} does not exists"
    with open(symbols_path, encoding="utf-8") as stream:
        symbols = json.load(stream)
    return symbols


def update_symbols(symbols):
    assert "control_host_ips" in symbols, "Cannot find control_host_ips in the symbols file"
    control_host_ip = symbols["control_host_ips"][0]

    settings_path = pathlib.Path("~/Library/Application Support/Code/User/settings.json").expanduser()
    assert settings_path.exists(), f"{settings_path} does not exist"
    with open(settings_path, encoding="utf-8") as stream:
        settings = json.load(stream)
    settings["rest-client.environmentVariables"]["$shared"]["hostname"] = control_host_ip
    settings["rest-client.environmentVariables"]["$shared"]["host"] = f"https://{control_host_ip}"

    with open(settings_path, "w", encoding="utf-8") as stream:
        json.dump(settings, stream, indent=4)


def main():
    """Entry"""
    try:
        symbols = load_symbols()
        update_symbols(symbols)
    except AssertionError as error:
        raise SystemExit(str(error))


if __name__ == "__main__":
    main()
