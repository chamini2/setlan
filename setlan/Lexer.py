#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Lexer for Setlan
Matteo Ferrando, 09-10285
"""

import ply.lex as lex

# Reserverd words of the language
words = [
    # Language
      'program'

    # Types
    , 'int'
    , 'bool'
    , 'set'

    # Values
    , 'true'
    , 'false'

    # Statements
    , 'using'
    , 'in'

    ## I/O
    , 'scan'

    , 'print'
    , 'println'

    ## Conditional
    , 'if'
    , 'else'

    ## Loops
    , 'for'
    , 'min'
    , 'max'
    , 'do'

    , 'repeat'
    , 'while'

    # Expressions / Operators
    , 'or'
    , 'and'
    , 'not'
    ]

# Tokens that need a regex specification
regexes = [
    # Values
      'INTEGER'
    , 'COMMA'

    # Identifiers
    , 'IDENTIFIER'

    # Statements
    , 'ASSIGN'
    , 'SEMICOLON'
    , 'LCURLY'
    , 'RCURLY'
    , 'LPAREN'
    , 'RPAREN'

    # Expressions / Operators
    , 'STRING'
    ## int
    , 'PLUS'
    , 'MINUS'
    , 'TIMES'
    , 'DIVIDE'
    , 'MODULO'
    ## set
    , 'UNION'
    , 'DIFFERENCE'
    , 'INTERSECTION'
    ## int - set
    , 'SPLUS'
    , 'SMINUS'
    , 'STIMES'
    , 'SDIVIDE'
    , 'SMODULO'
    , 'SMAX'
    , 'SMIN'
    , 'SSIZE'
    ## bool
    , 'LESS'
    , 'GREATER'
    , 'LESSEQ'
    , 'GREATEREQ'
    , 'EQUAL'
    , 'UNEQUAL'
    , 'CONTAINS'
    ]

# For PLY to generate automatic rules
RESERVED = { w: w.upper() for w in words }

# List of all the tokens to be recognized
tokens = RESERVED.values() + regexes

# Easy regexes
t_COMMA    = r'\,'

t_ASSIGN    = r'\='
t_SEMICOLON = r'\;'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'

t_PLUS   = r'\+'
t_MINUS  = r'\-'
t_TIMES  = r'\*'
t_DIVIDE = r'\/'
t_MODULO = r'\%'

t_UNION        = r'\+\+'
t_DIFFERENCE   = r'\\'
t_INTERSECTION = r'\>\<'

t_SPLUS   = r'\<\+\>'
t_SMINUS  = r'\<\-\>'
t_STIMES  = r'\<\*\>'
t_SDIVIDE = r'\<\/\>'
t_SMODULO = r'\<\%\>'
t_SMAX    = r'\>\?'
t_SMIN    = r'\<\?'
t_SSIZE   = r'\$\?'

t_LESS      = r'\<'
t_GREATER   = r'\>'
t_LESSEQ    = r'\<\='
t_GREATEREQ = r'\>\='
t_EQUAL     = r'\=\='
t_UNEQUAL   = r'\/\='
t_CONTAINS  = r'\@'

# Returns the actual value in Python integers
# Numbers are between -2^31 and 2^31
def t_INTEGER(token):
    r'\d+'
    val = int(token.value)
    if val > 2147483648:
        error_NUMBER(token)
    token.value = val
    return token

# Gets identifiers
def t_IDENTIFIER(token):
    r'\w[\w\d]*'
    # If there are no reserved words that match, it's an IDENTIFIER
    token.type = RESERVED.get(token.value, 'IDENTIFIER')
    return token

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
def t_STRING(token):
    r'\"([^\\\n]|(\\(n|"|\\)))*?\"'
    return token

################### Whitespace

# Ignores spaces, tabs and (Python style) comments
t_ignore = " \t"
t_ignore_COMMENT = r'\#.*'


# The only new line character considered is \n
def t_newline(token):
    r'\n+'
    token.lexer.lineno += token.value.count('\n')


# To find the column number of the current line
def find_column(text, lexpos):
    last_new_line = text.rfind('\n', 0, lexpos)
    if last_new_line < 0:
        last_new_line = -1
    column = lexpos - last_new_line
    return column


# Error to be shown if the lexer finds an "Unexpected" character
def t_error(token):
    text = token.lexer.lexdata
    message = "ERROR: unexpected character '%s' at line %d, column %d"
    data = token.value[0], token.lineno, find_column(text, token.lexer.lexpos)
    lexer_error.append(message % data)
    token.lexer.skip(1)


# Error to be shown if the lexer finds a number that's too large
def error_NUMBER(token):
    text = token.lexer.lexdata
    message = "ERROR: overflow for int '%s' at line %d, column %d"
    data = token.value, token.lineno, find_column(text, token.lexer.lexpos)
    lexer_error.append(message % data)


# Build the lexer
lexer = lex.lex()
lexer_error = []

###############################################################################


# The file (stored in a Python String)
# goes through the lexer and returns the list of tokens
def lexing(file_string, debug=0):

    tokens_list = []

    lexer.input(file_string)

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

    # Opens and reads the file to interpret
    file_string = open(argv[1], 'r').read()

    # Passes the file as a string to the Lexer
    tokens_list = lexing(file_string, debug)

    for tok in tokens_list:
        print 'token', tok.type, '            '[:-(len(tok.type))],
        print 'value (' + str(tok.value) + ')',
        print 'at line', str(tok.lineno) + ',',
        print 'column', find_column(file_string, tok.lexpos)


# If this is the module running
if __name__ == "__main__":
    main()
