#!/usr/bin/env python3
"""
Add Pytest logging options to pyproject.toml
"""

options = """

[tool.pytest.ini_options]
log_cli = true
log_cli_level = "WARNING"

log_file = "logs/my.log"
log_file_level = "WARNING"

# log_auto_indent (string)
# log_cli (bool):                Enable log display during test run
# log_cli_date_format (string)
# log_cli_format (string)
# log_cli_level (string)
# log_date_format (string)
# log_file_date_format (string)
# log_file_format (string)
# log_file_level (string)
# log_file_mode (string)
# log_file (string):             Default value for --log-file
# log_format (string):           Default value for --log-format
# log_level (string):            Default value for --log-level
"""


def main():
    with open("pyproject.toml", "at") as stream:
        stream.write(options)


if __name__ == "__main__":
    main()
