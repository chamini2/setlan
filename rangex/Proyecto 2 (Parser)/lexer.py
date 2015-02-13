#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Lexer for RangeX Language
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285
"""

import ply.lex as lex

# Reserverd words of the language
RESERVED = {
    # Language
    'program': 'PROGRAM',
    'begin': 'BEGIN',
    'end': 'END',

    # Types
    'int': 'INT',
    'bool': 'BOOL',
    'range': 'RANGE',

    ## Values
    'true': 'TRUE',
    'false': 'FALSE',

    # Instructions
    'declare': 'DECLARE',
    'as': 'AS',

    ## Conditionals
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',

    'case': 'CASE',
    'of': 'OF',

    ## Loops
    'do': 'DO',
    'while': 'WHILE',

    'for': 'FOR',
    'in': 'IN',

    ## In/Out
    'read': 'READ',

    'write': 'WRITE',
    'writeln': 'WRITELN',

    # Expressions/Operators
    'or': 'OR',
    'and': 'AND',
    'not': 'NOT',

    ## Functions
    'rtoi': 'RTOI',
    'length': 'LENGTH',
    'top': 'TOP',
    'bottom': 'BOTTOM'
}

# Tokens to be recognized
tokens = list(RESERVED.values()) + [
    # Language
    'NUMBER',
    'COMMA',
    'ASSIGN',
    'SEMICOLON',

    # Identifiers
    'ID',

    # Instructions
    'ARROW',
    'STRING',

    # Expressions/Operators
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'MODULO',
    'LPAREN',
    'RPAREN',
    'FROMTO',
    'INTERSECTION',
    'LESS',
    'LESSEQ',
    'GREAT',
    'GREATEQ',
    'EQUAL',
    'UNEQUAL',
    'BELONG',
]


# Returns the actual value in Python's int type
# Numbers are between -2^31 and 2^31
def t_NUMBER(token):
    r'\d+'
    val = int(token.value)
    if val > 2147483648:
        error_NUMBER(token)

    token.value = val
    return token

t_COMMA = r','
t_ASSIGN = r'='
t_SEMICOLON = r';'


def t_ID(token):
    r'\w[\w\d]*'
    # If there are no reserved words that match, it's an ID
    token.type = RESERVED.get(token.value, 'ID')
    return token

t_ARROW = r'->'

# These Strings take input until a " is found (in the same line),
# if there's a new line it reports an error.
########################
# The ? in the regular expression indicates non-greedy matching,
# for cases like:
#   writeln "number ", N, " is even"
# where it should recognize 6 separate tokens:
#   _________     ___________     ___     ___     ___     ____________
#   'writeln'  -  '"number "'  -  ','  -  'N'  -  ','  -  '" is even"'
# not 2 tokens:
#   ________      __________________________
#   'writeln'  -  '"number ", N, " is even"'
# being the latter one a String
t_STRING = r'\"([^\\\n]|(\\(n|"|\\)))*?\"'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_FROMTO = r'\.\.'
t_INTERSECTION = r'<>'
t_LESS = r'<'
t_LESSEQ = r'<='
t_GREAT = r'>'
t_GREATEQ = r'>='
t_EQUAL = r'=='
t_UNEQUAL = r'/='
t_BELONG = r'>>'

# Ignores spaces, tabs and (C style) comments
t_ignore = " \t"
t_ignore_COMMENT = r'//.*'


# The only new line character considered is \n
def t_newline(token):
    r'\n+'
    token.lexer.lineno += token.value.count('\n')


# To find the column number of the current line
def find_column(text, token):
    last_new = text.rfind('\n', 0, token.lexpos)
    if last_new < 0:
        last_new = -1
    column = token.lexpos - last_new
    return column


# Error to be shown if the lexer finds an "Unexpected" character
def t_error(token):
    text = token.lexer.lexdata
    message = "ERROR: Unexpected character '%s' at line %d, column %d"
    data = (token.value[0], token.lineno, find_column(text, token))
    lexer_error.append(message % data)
    token.lexer.skip(1)


# Error to be shown if the lexer finds a number that's too large
def error_NUMBER(token):
    text = token.lexer.lexdata
    message = "ERROR: Overflow for int '%s' at line %d, column %d"
    data = (token.value, token.lineno, find_column(text, token))
    lexer_error.append(message % data)


# Build the lexer
lex.lex()
lexer_error = []

###############################################################################


# The file (stored in a Python String)
# goes through the lexer and returns the list of tokens
def lexing(file_string, debug=0):

    lexer = lex.lex()
    tokens_list = []

    lexer.input(file_string, debug=debug)

    # Pass entire file through lexer
    for tok in lexer:
        tokens_list.append(tok)

    # If no "Unexpected character" or "Overflow" was found
    if not lexer_error:
        return tokens_list
    else:
        # Print all the errors
        for error in lexer_error:
            print error

        # Empty list to indicate error
        return []


# Only to be called if this is the main module
def main(argv=None):
    import sys      # argv, exit

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        print "ERROR: No input file"
        return
    elif len(argv) > 3:
        print "ERROR: Invalid number of arguments"
        return

    if len(argv) == 3:
        debug = argv[2]
    else:
        debug = 0

    # Opens file to interpret
    file_string = open(argv[1], 'r').read()

    # Reads the file and passes it to the Lexer
    tokens_list = lexing(file_string, debug)

    for tok in tokens_list:
        print 'tok(' + str(tok.type) + ')' + '            '[:-(len(tok.type))],
        print 'val(' + str(tok.value) + ')',
        print 'at line ' + str(tok.lineno) + ',',
        print 'column ' + str(find_column(file_string, tok))


# If this is the module running
if __name__ == "__main__":
    main()
