import importlib.metadata

CLI_NAME = "hier"

try:
    __version__ = importlib.metadata.version(CLI_NAME)
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.0.0-dev"

