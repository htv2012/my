#!/usr/bin/env python3
"""
Add Pytest logging options to pyproject.toml
"""

options = """

[tool.pytest.ini_options]
log_cli = true
log_cli_level = "DEBUG"

"""


def main():
    with open("pyproject.toml", "at") as stream:
        stream.write(options)


if __name__ == "__main__":
    main()
