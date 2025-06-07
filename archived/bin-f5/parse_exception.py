#!/usr/bin/env python3
"""Parse exception message.

Sample clipboard text is at https://hastebin.es.f5net.com/izacu
"""
import fileinput
import json
import subprocess
import shutil

RESPONSE_TEXT = 'response_text'


# Assume the message is in the clipboard, retrieve it
completed_process = subprocess.run(['pbpaste'], capture_output=True,text=True)

curly_brace_index = completed_process.stdout.index("{")
clipboard_contents = completed_process.stdout[curly_brace_index:]
error = json.loads(clipboard_contents)

if RESPONSE_TEXT in error:
    error[RESPONSE_TEXT] = json.loads(error[RESPONSE_TEXT])

output = json.dumps(error, indent=4)
jq = shutil.which("jq")
if jq:
    subprocess.run(["jq", "."], input=output, text=True)
else:
    print(output)
