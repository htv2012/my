#!/usr/bin/env python3
import logging
import os
import subprocess
import tempfile
import contextlib

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
            return selection or None
    except FileNotFoundError:
        # fzf not installed, use a simple selection method
        for i, element in enumerate(candidates):
            print(f"{i:>3} {element}")
        print()

        while (answer := input("> ").strip()) != "":
            with contextlib.suppress(IndexError, ValueError):
                index = int(answer)
                return candidates[index]
        return None
