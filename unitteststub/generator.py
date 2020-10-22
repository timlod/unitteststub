# Copyright (c) 2015-2020 Agalmic Ventures LLC (www.agalmicventures.com)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import ast
import collections
from pathlib import Path

from unitteststub import templates


def gen_test(
    root,
    file,
    import_pre,
    include_internal=False,
    class_fmt="%sTest",
    function_fmt="test_%s",
    classmethods=False,
):
    """
        Generates a unit test, given a root directory and a subpath to a file.

        :param root: str
        :param file: str
        :param include_internal: bool
        :return: str or None
        """
    # Skip non-Python files
    if not file.endswith(".py"):
        return None

    # Skip symlinks
    path = Path(root) / file
    if path.is_symlink():
        print("Symlink: %s" % path)
        return None

    module, _ = file.stem

    # Load the file
    try:
        with open(path) as f:
            text = f.read()
    except UnicodeDecodeError as ude:
        print("Unicode decode error for %s: %s" % (path, ude))
        return None

    # Parse it
    try:
        tree = ast.parse(text)
    except Exception as e:  # @suppress warnings since this really does need to catch all
        print("Failed to parse %s" % path)
        print(e)
        return None

    # Walk the AST
    classes = []
    class_functions_dict = collections.defaultdict(list)
    functions = []
    for node in tree.body:
        note_type = type(node)
        if note_type is ast.ClassDef:
            if not node.name.startswith("_") or include_internal:
                classes.append(node.name)

            # Track methods
            for child in node.body:
                if (
                    type(child) is ast.FunctionDef
                    and not child.name.startswith("_")
                    or include_internal
                ):
                    class_functions_dict[node.name].append(child.name)

        elif note_type is ast.FunctionDef:
            if not node.name.startswith("_") or include_internal:
                functions.append(node.name)

    if len(functions) == 0 and len(classes) == 0:
        print(f"No classes or functions in {path}")
        return None

    # Generate a functions test?
    unit_tests = []
    if len(functions) > 0:
        function_comment = f"Tests for functions in the {module} module."
        function_tests = "\n".join(
            templates.function % (function_fmt % function)
            for function in functions
        )

        unit_tests.append(
            templates.cls % (module, function_comment, function_tests)
        )

    # Generate class tests?
    if len(classes) > 0:
        for c in classes:
            class_comment = f"Tests for functions in the {c} class."
            function_tests = "\n".join(
                templates.function % (function)
                for function in class_functions_dict[c]
                if function[0] != "_"
            )
            unit_tests.append(
                templates.cls
                % (
                    class_fmt % c,
                    class_comment,
                    templates.classmethods if classmethods else "",
                    function_tests,
                )
            )
            # TODO: generate instance construction stub

    # Assemble the unit tests in the template
    tests_str = "\n\n".join(test for test in unit_tests if test != "")
    return templates.base % (import_pre, module, tests_str)
