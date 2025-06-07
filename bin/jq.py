import json
import shutil
import subprocess


def jq(obj):
    """Print a JSON object."""

    text = json.dumps(obj, indent=4)
    if shutil.which("jq"):
        subprocess.run(["jq", ".", "--indent", "4"], input=text, encoding="utf-8")
    else:
        print(text)
