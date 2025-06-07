# Matcher Selection

    -E, --extended-regexp: Same as egrep
    -F, --fixed-strings: Same as fgrep

# Matching Control

    -e PATTERN
    -f FILE
    -v, --invert-matc

# Output Control

    --color, --colour=never,always,auto
    -H, --with-filename
    -h, --no-filename
    -L, --files-without-match
    -l, --files-with-matches
    -n, --line-number
    -o, --only-matching

# Context

    -A, --after-context
    -B, --before-context
    -C, --context

# Include, Exclude

    --exclude-from=FILE
    --exclude-dir=DIR
    --exclude=GLOB
    --include=GLOB
    -r, --recursive

# Examples

    # Look for those import lines in Python modules
    grep --no-filename --include="*.py" "^import"

