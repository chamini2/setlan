#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""Interpreter for setlan Language
CI3725 - Entrega 2 Grupo 3.
Hosmar Colmenares, 11-1121
Luis Diaz, 11-10293
"""
import parser

def main(argv=None):
	import sys # argv, exit
	if argv is None:
		argv = sys.argv
	if len(argv) == 1:
		print "ERROR: No input file"
		return
	elif len(argv) > 2:
		print "ERROR: Invalid number of arguments"
		return
	try:
		# Opens and reads file to interpret
		file_string = open(argv[1], 'r').read()
	except IOError:
		print "ERROR: Must give an input file"
		return
	ast = parser.parsing(file_string)
	# Check for Overflow or Unexpected character errors
	if parser.ERRORS:
		ast = None
		for error in parser.ERRORS:
			print error
		# Check for Syntax errors
	elif parser.parser_error:
		ast = None
		for error in parser.parser_error:
			print error
	else:
		print ast

if __name__ == "__main__":
	main()
