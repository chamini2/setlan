####
#CI3725 - Entrega 1 Grupo 7.
#Alberto Cols, 09-10177
#Matteo Ferrando, 09-10285
####

#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ply.lex as lex

# Reserverd words of the language
reserved = {
    # Language
    'program' : 'PROGRAM',
    'begin' : 'BEGIN',
    'end' : 'END',

    # Types
    'int' : 'INT',
    'bool' : 'BOOL',
    'range' : 'RANGE',

    ## Values
    'true' : 'TRUE',
    'false' : 'FALSE',

    # Instructions
    'declare' : 'DECLARE',
    'as' : 'AS',

    ## Conditionals
    'if' : 'IF',
    'then' : 'THEN',
    'else' : 'ELSE',

    'case' : 'CASE',
    'of' : 'OF',

    ## Loops
    'do' : 'DO',
    'while' : 'WHILE',

    'for' : 'FOR',
    'in' : 'IN',

    ## In/Out
    'read' : 'READ',

    'write' : 'WRITE',
    'writeln' : 'WRITELN',

    # Expressions/Operators
    'or' : 'OR',
    'and' : 'AND',
    'not' : 'NOT',

    ## Functions
    'rtoi' : 'RTOI',
    'length' : 'LENGTH',
    'top' : 'TOP',
    'bottom' : 'BOTTOM'
}

# Tokens to be recognized
tokens = [
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
    'MODULE',
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
    'BELONG'
] + list(reserved.values())

# Returns the actual value in Python's int type
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

t_COMMA = r','
t_ASSIGN = r'='
t_SEMICOLON = r';'

def t_ID(t):
    r'\w[\w\d]*'
    # If there are no reserved words that match, it's an ID
    t.type = reserved.get(t.value, 'ID')
    return t

t_ARROW = r'->'
# These Strings take input even after new lines, it ends only and only in ' " '
# t_STRING = r'"[^"]*"'

# These Strings take input until a " is found (in the same line),
# if there's a new line it reports an error.
##########
# The ? in the regular expression indicates non-greedy matching,
# for cases like:
#   writeln "number ", N, " is even"
# where it should recognize 6 separate tokens:
#   ['writeln', '"number "', ',', 'N', ',', '" is even"']
# not 2 tokens:
#   ['writeln', '"number ", N, " is even"']
# being the latter one a String
##########
t_STRING = r'".*?"'

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULE = r'%'
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

# The only new line character considered is '\n'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

# To find the column number of the current line
def find_column(text,token):
    last_cr = text.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = -1
    column = token.lexpos - last_cr
    return column

# Error to be shown if the lexer finds an "Unexpected" character in the program
def t_error(t):
    errors_list.append("ERROR: Unexpected character '%s' at line %d, column %d"
                       % (t.value[0], t.lineno, find_column(lexer.lexdata, t)))
    t.lexer.skip(1)

# The file (represented in a Python String)
# goes through the lexer and returns the list of tokens
def lexing(file):

    global errors_list, lexer

    lexer = lex.lex()
    tokens_list = []
    errors_list = []

    lexer.input(file)

    # Pass entire file through lexer
    for tok in lexer:
        tokens_list.append(tok)

    # If no "Unexpected character" was found
    if not errors_list:
        return tokens_list
    else:
        # Print all the "Unexpected character" errors
        for error in errors_list:
            print error

        # Empty list to indicate error
        return []

###############################################################################

# Only to be called if this is the main module (not imported in another one)
def main(argv = None):
    import sys    # argv, exit

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        print "ERROR: No input file"
        sys.exit() ## return (averiguar cuál es mejor)
    elif len(argv) > 2:
        print "ERROR: Invalid number of arguments"
        sys.exit() ## return (averiguar cuál es mejor)

    # Opens file to interpret
    file = open(argv[1], 'r')

    # Reads the file and passes it to the Lexer
    tokens_list = lexing(file.read())

    for tok in tokens_list:
        print 'tok(' + str(tok.type) + ')',
        print 'val(' + str(tok.value) + ')',
        print 'at line ' + str(tok.lineno) + ',',
        print 'column ' + str(find_column(lexer.lexdata, tok))

# If this is the module running
if __name__ == "__main__":
    main()
