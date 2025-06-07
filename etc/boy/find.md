    # Find all Python scripts, but ignore __init__.py

        find . ! -name __init__.py -name '*.py'

    # File name (base name) only

        find . -name '*.py' -printf "%f\n"        # Linux
        find . -name '*.py' -exec basename {} \;  # macOS, as it does not have -printf

    # Modified within the last 3 days

        find . -mtime -3

    # Has not been modified in the last 30 days

        find . -mtime +30

