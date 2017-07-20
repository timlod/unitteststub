#!/usr/bin/env python3

import argparse
import os
import sys

from PyTestStub import Generator

def main(argv=None):
	"""
	The main function of the unit test generator tool.

	:param argv: optional arguments (defaults to sys.argv if not specified)
	:return: int
	"""
	#Parse arguments
	parser = argparse.ArgumentParser(description='Python Unit Test Stub Generator')

	parser.add_argument('module', help='The path of the module to test.')

	parser.add_argument('-F', '--footer',
		help='File to use as a footer.')
	parser.add_argument('-H', '--header',
		help='File to use as a header.')

	parser.add_argument('-f', '--force', action='store_true',
		help='Force files to be generated, even if they already exist.')
	parser.add_argument('-m', '--test-module', default='test',
		help='The path of the test module to generate.')
	parser.add_argument('-p', '--test-prefix', default='test_',
		help='The prefix for test files.')
	parser.add_argument('-t', '--tab-width', type=int,
		help='The width of a tab in spaces (default actual tabs).')

	if argv is None:
		argv = sys.argv
	arguments = parser.parse_args(argv[1:])

	#Open the header and footer
	header = ''
	footer = ''
	if arguments.header is not None:
		with open(arguments.header) as headerFile:
			header = headerFile.read()
	if arguments.footer is not None:
		with open(arguments.footer) as footerFile:
			footer = footerFile.read()

	#Walk the directory finding Python files
	for root, directoryNames, fileNames in os.walk(arguments.module):
		for fileName in fileNames:
			#Skip ignored files
			unitTest = Generator.generateUnitTest(root, fileName)
			if unitTest is None:
				continue

			#Replace tabs
			if arguments.tab_width is not None:
				unitTest = unitTest.replace('\t', ' ' * arguments.tab_width)

			#Add header and footer
			unitTest = header + unitTest + footer

			#Write it
			outFile = '%s%s' % (arguments.test_prefix, fileName)
			outFolder = arguments.test_module
			if not os.path.exists(outFolder):
				os.makedirs(outFolder)

			#TODO: do this at every level
			testInit = os.path.join(outFolder, '__init__.py')
			if not os.path.exists(testInit):
				with open(testInit, 'w') as testInitFile:
					testInitFile.write('')

			outPath = os.path.join(outFolder, outFile)
			if not os.path.exists(outPath) or arguments.force:
				print('[%s] Writing...' % outPath)
				with open(outPath, 'w') as outFile:
					outFile.write(unitTest)
			else:
				print('[%s] Already exists' % outPath)

	return 0

if __name__ == '__main__':
	sys.exit(main())
