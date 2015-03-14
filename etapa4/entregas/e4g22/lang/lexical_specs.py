#!/usr/bin/env python
# ------------------------------------------------------------
# lexical_specs.py
#
# Setlan language lexicographical specifications
#
# Author:
# Victor De Ponte, 05-38087, <rdbvictor19@gmail.com>
# ------------------------------------------------------------
from exceptions import SetlanLexicalError, SetlanValueError

from lib.LexerWrapper import Token

################################################################################
############################# Tokens specification #############################
################################################################################

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

reserved = {
    'program' : 'TkProgram',
    'int'     : 'TkInt',
    'bool'    : 'TkBool',
    'set'     : 'TkSet',
    'using'   : 'TkUsing',
    'in'      : 'TkIn',
    'scan'    : 'TkScan',
    'print'   : 'TkPrint',
    'println' : 'TkPrintLn',
    'if'      : 'TkIf',
    'else'    : 'TkElse',
    'for'     : 'TkFor',
    'do'      : 'TkDo',
    'min'     : 'TkMin',
    'max'     : 'TkMax',
    'repeat'  : 'TkRepeat',
    'while'   : 'TkWhile',
    'or'      : 'TkOr',
    'and'     : 'TkAnd',
    'not'     : 'TkNot',
    'true'    : 'TkTrue',
    'false'   : 'TkFalse'
}

tokens = [
    'TkId',            # Variable Identifier
    'TkNum',           # Integer inmediate numbers
    'TkString',        # Strings: "This is a string"
    'TkOBrace',        # {
    'TkCBrace',        # }
    'TkComma',         # ,
    'TkAssign',        # =
    'TkSColon',        # ;
    'TkOPar',          # (
    'TkCPar',          # )
    'TkPlus',          # +
    'TkMinus',         # - and unary minus (as in -42)
    'TkTimes',         # *
    'TkDiv',           # /
    'TkMod',           # %
    'TkUnion',         # ++
    'TkDiff',          # \
    'TkInter',         # ><
    'TkSPlus',         # <+>
    'TkSMinus',        # <->
    'TkSTimes',        # <*>
    'TkSDiv',          # </>
    'TkSMod',          # <%>
    'TkGetMin',        # <?
    'TkGetMax',        # >?
    'TkSize',          # $?
    'TkGreat',         # >
    'TkGreatOrEq',     # >=
    'TkLess',          # <
    'TkLessOrEq',      # <=
    'TkEquals',        # ==
    'TkNotEq',         # /=
    'TkIsIn'           # @
] + list(reserved.values())

# Some helpers for traking line and column numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    plus = 0
    if token.lineno == 1: plus += 1
    column = (token.lexpos - last_cr) + plus
    return column

# Comments specifications which are ignored
def t_COMMENT(t):
    r'\#.*'
    pass

# Token regex specifications

def t_TkId(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.colno = find_column(t.lexer.lexdata,t)
    t.type = reserved.get(t.value,'TkId')    # Check for reserved words
    return Token(t)

def t_TkString(t):
    r'"([^"\\\n\r]|\\.)*"'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkNum(t):
    r'[0-9]+'
    t.colno = find_column(t.lexer.lexdata,t)
    try:
        t.value = int(t.value)
    except ValueError:
        if not hasattr(t.lexer, 'errors'):
            t.lexer.errors = []
        message = "In line %d, column %d: Number %s is too large! MaxInt value assigned instead." % (t.lineno, t.colno, t.value)
        t.lexer.errors.append(SetlanValueError(message))
        import sys
        t.value = sys.maxint
    return Token(t)

def t_TkOBrace(t):
    r'\{'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkCBrace(t):
    r'\}'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkOPar(t):
    r'\('
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkCPar(t):
    r'\)'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkComma(t):
    r','
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkSColon(t):
    r';'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkSPlus(t):
    r'<\+>'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkSMinus(t):
    r'<->'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkSTimes(t):
    r'<\*>'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkSDiv(t):
    r'</>'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkSMod(t):
    r'<%>'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkUnion(t):
    r'\+\+'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkPlus(t):
    r'\+'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkMinus(t):
    r'-'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkTimes(t):
    r'\*'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkNotEq(t):
    r'/='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkDiv(t):
    r'/'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkMod(t):
    r'%'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkDiff(t):
    r'\\'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkInter(t):
    r'><'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkGetMax(t):
    r'>\?'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkGetMin(t):
    r'<\?'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkSize(t):
    r'\$\?'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkEquals(t):
    r'=='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkGreatOrEq(t):
    r'>='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkLessOrEq(t):
    r'<='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkGreat(t):
    r'>'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkLess(t):
    r'<'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkAssign(t):
    r'='
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

def t_TkIsIn(t):
    r'@'
    t.colno = find_column(t.lexer.lexdata,t)
    return Token(t)

# Error handling rule
def t_error(t):
    t.colno = find_column(t.lexer.lexdata,t)
    if not hasattr(t.lexer, 'errors'):
        t.lexer.errors = []
    message = "In line %d, column %d: Unexpected character '%s'." % (t.lineno, t.colno, t.value[0])
    t.lexer.errors.append(SetlanLexicalError(message))
    t.lexer.skip(1)
################################################################################
######################### End of Tokens specification ##########################
################################################################################