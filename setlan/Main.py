#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Interpreter for Setlan
Matteo Ferrando, 09-10285
"""

import Errors
import Parser

from signal import signal, SIGINT
from sys import exit


def main(argv=None):
    import sys      # argv

    if argv is None:
        argv = sys.argv


    if len(argv) == 1:
        in_file = sys.stdin
    elif len(argv) == 2:
        in_file = open(argv[1], 'r')
    elif len(argv) > 2:
        print "ERROR: Invalid number of arguments"
        return

    try:
        # Opens and reads file to interpret
        file_string = in_file.read()
    except IOError:
        print "ERROR: Must give an input file"
        return

    ast = Parser.parsing(file_string)

    if ast:
        ast.check()

    # Check for Overflow or Unexpected character errors
    if Errors.lexer_error:
        for error in Errors.lexer_error:
            print error

    # Check for Syntax errors
    elif Errors.parser_error:
        for error in Errors.parser_error:
            print error

    # Check for Static errors
    elif Errors.static_error:
        for error in Errors.static_error:
            print error

    else:
        print ast
        ast.execute()

    return ast


    # Handle keyboard interrupts "better"
    def keyboard_interrupt(signal, frame):
        print "\nKeyboard Interrupt"
        exit()

    signal(SIGINT, keyboard_interrupt)


if __name__ == "__main__":
    main()
