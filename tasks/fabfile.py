import pathlib
import sys

from invoke import Collection

plugins_dir = pathlib.Path(__file__).with_name("plugins")
assert plugins_dir.exists(), f"Plugins directory does not exist: {plugins_dir}"
assert plugins_dir.is_dir(), f"Plugins is not a directory: {plugins_dir}"
sys.path.append(str(plugins_dir))

ns = Collection()
for path in plugins_dir.glob("*.py"):
    module_name = path.stem
    module = __import__(module_name)
    ns.add_collection(Collection.from_module(module))
