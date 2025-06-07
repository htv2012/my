#!/usr/bin/env python3
import logging
import os
import subprocess
import tempfile

logging.basicConfig(level=os.getenv("LOGLEVEL", "WARNING"))
LOGGER = logging.getLogger(__name__)


def user_select(candidates: list[str]) -> str:
    """
    Ask the user to select from a list.
    """
    if len(candidates) == 1:
        return candidates[0]
    try:
        # Attempt to launch fzf with candidates
        with tempfile.TemporaryFile(mode="w+", encoding="utf-8") as output:
            subprocess.run(
                ["fzf", "-i"],
                text=True,
                input="\n".join(candidates),
                stdout=output,
            )
            output.seek(0)
            selection = output.read().strip()
    except FileNotFoundError:
        # fzf not installed, use a simple selection method
        for i, element in enumerate(candidates):
            print(f"{i:>3} {element}")
        print()
        index = -1
        while not (0 <= index < len(candidates)):
            index = input("Enter a number: ")
            try:
                index = int(index)
            except ValueError:
                index = -1
        selection = candidates[index]

    LOGGER.debug("Selected: %r", selection)
    return selection
