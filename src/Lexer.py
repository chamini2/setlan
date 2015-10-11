"""
Lexer for Setlan
Matteo Ferrando, 09-10285
"""

import ply.lex as lex

import Errors


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
    Errors.lexer_error.append(message % data)
    token.lexer.skip(1)


# Error to be shown if the lexer finds a number that's too large
def error_NUMBER(token):
    text = token.lexer.lexdata
    message = "ERROR: overflow for int '%s' at line %d, column %d"
    data = token.value, token.lineno, find_column(text, token.lexer.lexpos)
    Errors.lexer_error.append(message % data)


# Build the lexer
lexer = lex.lex()

###############################################################################


# The file (stored in a Python String)
# goes through the lexer and returns the list of tokens
def lexing(file_str, debug=0):

    tokens_list = []

    lexer.input(file_str)

    # Pass entire file through lexer
    for tok in lexer:
        tokens_list.append(tok)

    # If no "Unexpected character" or "Overflow" was found
    if not Errors.lexer_error:
        return tokens_list
    else:
        # Print all the errors
        for error in Errors.lexer_error:
            print error

        # Empty list to indicate error
        return None

def str_tokens(file_str, tokens_list):
    string = ""
    for tok in tokens_list:
        string += 'token ' + tok.type + '            '[:-(len(tok.type))]
        string += 'value (' + str(tok.value) + ') '
        string += 'at line ' + str(tok.lineno) + ', '
        string += 'column ' + str(find_column(file_str, tok.lexpos)) + "\n"
    return string
