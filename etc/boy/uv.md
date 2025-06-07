# Install

```bash
 curl -LsSf https://astral.sh/uv/install.sh | sh
 ```

# Create with `uv init`

```bash
uv init myapp                         # Create dir myapp, good for CLI application
uv init --app myapp                   # Same as the above
uv init --lib mylib                   # Create dir mylib with files to build a library
uv init --package mypackage           # Create a package
uv init --package --name mypackage .  # Create a package in this dir
```

# Project

```bash
uv run pytest                         # Unit test
uv run <...>                          # Run
source .venv/bin/activate             # Enter the virtual environment
```
