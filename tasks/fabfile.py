import pathlib
import sys

from invoke import Collection

ns = Collection()
plugins_dir = pathlib.Path(__file__).with_name("plugins")
sys.path.append(str(plugins_dir))

for path in plugins_dir.glob("*.py"):
    module_name = path.stem
    module = __import__(module_name)
    ns.add_collection(Collection.from_module(module))
