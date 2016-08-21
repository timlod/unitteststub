
# PyTestStub
PyTestStub is a Python unit test stub generator. It takes a module name, and a
path for the test module to generate, then generates test stubs for each class
and function.

## `GenerateUnitTests.py`
Generates the actual unit tests:

	> ~/path/to/PyTestStub/GenerateUnitTests.py -h
	usage: GenerateUnitTests.py [-h] [-p TEST_PREFIX] module test_module

	The Code Monkey.

	positional arguments:
	  module                The path of the module to test.
	  test_module           The path of the test module to generate.

	optional arguments:
	  -h, --help            show this help message and exit
	  -p TEST_PREFIX, --test-prefix TEST_PREFIX
	                        The prefix for test files.

	> ~/path/to/PyTestStub/GenerateUnitTests.py NanoPcap Test2
	No classes or functions in NanoPcap/__init__.py
	Writing test to Test2/NanoPcap/test_Format.py
	Writing test to Test2/NanoPcap/test_Listener.py
	Writing test to Test2/NanoPcap/test_Parser.py
	No classes or functions in NanoPcap/Tools/__init__.py
	Writing test to Test2/NanoPcap/Tools/test_PcapDump.py
	Writing test to Test2/NanoPcap/Tools/test_PcapSummary.py
	No classes or functions in NanoPcap/Utility/__init__.py
	Writing test to Test2/NanoPcap/Utility/test_Statistics.py
	Writing test to Test2/NanoPcap/Utility/test_Units.py