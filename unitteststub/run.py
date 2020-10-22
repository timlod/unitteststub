#!/usr/bin/env python3

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

# TODO: move fully to pathlib

import argparse
import os
import sys
from pathlib import Path

_current_file = Path(".").resolve()
sys.path.insert(0, _current_file.parent.parent)

from unitteststub.generator import gen_test


def main(argv=None):
    """
        The main function of the unit test generator tool.

        :param argv: optional arguments (defaults to sys.argv if not specified)
        :return: int
        """
    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Python unittest stub generator"
    )

    parser.add_argument("module", help="The path of the module to test.")

    parser.add_argument("-F", "--footer", help="File to use as a footer.")
    parser.add_argument("-H", "--header", help="File to use as a header.")
    parser.add_argument(
        "-X",
        "--exclude",
        action="append",
        default=[],
        help="Add a child directory name to exclude.",
    )

    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force files to be generated, even if they already exist.",
    )
    parser.add_argument(
        "-i",
        "--internal",
        action="store_true",
        help="Include internal classes and methods starting with a _.",
    )
    parser.add_argument(
        "-m",
        "--test-module",
        default="test",
        help="The path of the test module to generate.",
    )
    parser.add_argument(
        "-p",
        "--test-prefix",
        default="test_",
        help="The prefix for test files.",
    )
    parser.add_argument(
        "-t",
        "--tab-width",
        type=int,
        help="The width of a tab in spaces (default actual tabs).",
    )
    parser.add_argument(
        "-cf",
        "--class-fmt",
        type=str,
        default="%sTest",
        help="Format/template of test classes (default %sTest)",
    )
    parser.add_argument(
        "-ff",
        "--function-fmt",
        type=str,
        default="test_%s",
        help="Format/template of test function names (default test_%s)",
    )
    parser.add_argument(
        "-cm",
        "--classmethods",
        action="store_true",
        help="Whether to write setUpClass and tearDownClass classmethods.",
    )

    if argv is None:
        argv = sys.argv
    arguments = parser.parse_args(argv[1:])

    # Open the header and footer
    header = ""
    footer = ""
    if arguments.header is not None:
        with open(arguments.header) as f:
            header = f.read()
    if arguments.footer is not None:
        with open(arguments.footer) as f:
            footer = f.read()

    module = Path(arguments.module).resolve()
    # Walk the directory finding Python files
    for root, _, files in os.walk(module):
        for file in files:
            # Skip ignored directories
            child_dir = Path(root).relative_to(module)
            if child_dir.name in arguments.exclude:
                continue

            if child_dir == Path("."):
                import_pre = arguments.module
            else:
                import_pre = ".".join([arguments.module] + child_dir.parts)

            # Generate unit test, skipping ignored files
            unit_test = gen_test(
                root,
                file,
                import_pre,
                arguments.internal,
                arguments.class_fmt,
                arguments.function_fmt,
                arguments.classmethods,
            )
            if unit_test is None:
                continue

            # Replace tabs
            if arguments.tab_width is not None:
                unit_test = unit_test.replace("\t", " " * arguments.tab_width)

            # Add header and footer
            unit_test = header + unit_test + footer

            # Write it
            outfile = "%s%s" % (arguments.test_prefix, file)
            outdir = Path(arguments.test_module)
            outdir.mkdir(parents=True, exist_ok=True)

            # TODO: do this at every level
            test_init = outdir / "__init__.py"
            test_init.touch()

            outpath = outdir / child_dir / outfile
            if (
                arguments.force
                or not os.path.exists(outpath)
                or os.stat(outpath).st_size == 0
            ):
                print("[%s] Writing..." % outpath)
                with open(outpath, "w") as f:
                    f.write(unit_test)
            else:
                print("[%s] Already exists" % outpath)

    return 0


if __name__ == "__main__":
    sys.exit(main())
