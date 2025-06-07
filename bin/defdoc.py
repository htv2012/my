#!/usr/bin/env python3
"""
Given a function definition 'def myfunction(...):', produces the docstring
template for that function
"""

import ast
import fileinput
import io


def docstring(function_text):
    """
    Given a function declaration, produce the docstring.

    :param function_text: The function declaration that starts with
        'def' and ends with ':'
    :return: The function declaration, plus the docstring
    """
    indent = " " * (len(function_text) - len(function_text.lstrip()) + 4)

    output = io.StringIO()
    output.write(function_text.replace("\n\n", "\n"))
    output.write(f'{indent}"""\n\n')

    function_def = ast.parse(function_text.strip() + "pass")
    for node in ast.walk(function_def):
        if isinstance(node, ast.arg):
            if node.arg in {"self", "cls"}:
                continue

            output.write(f"{indent}:param {node.arg}: ")
            if node.annotation:
                output.write(node.annotation.id)
            output.write("\n")

    output.write(f"{indent}:return:\n")
    output.write(f'{indent}"""')

    return output.getvalue()


def main():
    """Entry"""
    input_lines = "\n".join(fileinput.input())
    print(docstring(input_lines))


if __name__ == "__main__":
    main()
