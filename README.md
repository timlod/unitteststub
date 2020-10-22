# unitteststub

unitteststub reads your Python code to generate unit test stubs. Given a module
name, it walks each file in the module. If it encounters a file without a
corresponding test file, it generates one with test stubs for each function and
class method in the file.

Besides reducing time spent on boilerplate, this approach ensures complete
coverage when creating new tests, so developers can focus on the actual tests.
After generation, rework is limited to removing unneeded stubs and duplicating
those which require multiple tests (copy+paste). The resulting skeleton is
sufficiently complete to delegate the test implementation to another developer.

## Installation

Currently, you need to `git clone https://github.com/timlod/unitteststub.git`
and `pip install .` the repository.

## Scripts

### `run.py`
Generates the unit tests, with options like a header file to prepend as
a license:

        > unitteststub -h
        usage: unitteststub [-h] [-F FOOTER] [-H HEADER] [-X EXCLUDE] [-f] [-i] [-m TEST_MODULE] [-p TEST_PREFIX] [-t TAB_WIDTH] [-cf CLASS_FMT]
                    [-ff FUNCTION_FMT] [-cm]
                    module

        Python unittest stub generator

        positional arguments:
          module                The path of the module to test.

        optional arguments:
          -h, --help            show this help message and exit
          -F FOOTER, --footer FOOTER
                                File to use as a footer.
          -H HEADER, --header HEADER
                                File to use as a header.
          -X EXCLUDE, --exclude EXCLUDE
                                Add a child directory name to exclude.
          -f, --force           Force files to be generated, even if they already exist.
          -i, --internal        Include internal classes and methods starting with a _.
          -m TEST_MODULE, --test-module TEST_MODULE
                                The path of the test module to generate. (default ./test)
          -p TEST_PREFIX, --test-prefix TEST_PREFIX
                                The prefix for test files.
          -t TAB_WIDTH, --tab-width TAB_WIDTH
                                The width of a tab in spaces (default 4).
          -cf CLASS_FMT, --class-fmt CLASS_FMT
                                Format/template of test classes (default %sTest)
          -ff FUNCTION_FMT, --function-fmt FUNCTION_FMT
                                Format/template of test function names (default test_%s)
          -cm, --classmethods   Whether to write setUpClass and tearDownClass classmethods.
                usage: GenerateUnitTests.py [-h] [-F FOOTER] [-H HEADER] [-X EXCLUDE] [-f]
                                            [-i] [-m TEST_MODULE] [-p TEST_PREFIX]
                                            [-t TAB_WIDTH]
                                            module

Output is simple and human readable:

        > unitteststub unitteststub
        No classes or functions in unitteststub/__init__.py
        No classes or functions in unitteststub/templates.py
        [test/test_run.py] Writing...
        [test/test_generator.py] Writing...


Output files have stubs for everything (classmethods can be toggled with -cm) but are easily
pruned if e.g. setup methods are not needed:

import unittest
from unitteststub import generator


class generatorTest(unittest.TestCase):
    """
    Tests for functions in the generator module.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_gen_test(self):
        raise NotImplementedError() # TODO: gen_test


if __name__ == "__main__":
    unittest.main()
