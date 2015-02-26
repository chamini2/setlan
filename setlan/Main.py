#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Interpreter for Setlan
Matteo Ferrando, 09-10285
"""

import Errors
import Lexer
import Parser

from sys import stdin
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='?', type=argparse.FileType('r'), default=stdin)
parser.add_argument('-t', help="tokens list",  action="store_true")
parser.add_argument('-a', help="AST",          action="store_true")
parser.add_argument('-s', help="symbol table", action="store_true")
args = parser.parse_args()

# reads the file to interpret
file_str = args.file.read()
ast = Parser.parsing(file_str)

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
    if args.t:
        tokens = Lexer.lexing(file_str)
        print Lexer.str_tokens(file_str, tokens)

    if args.a:
        print ast

    if args.s:
        print ast.table_str()

    ast.execute()

return ast