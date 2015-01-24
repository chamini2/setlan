#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Parser for Setlan
Matteo Ferrando, 09-10285
"""

import ply.yacc as yacc
from Lexer import tokens, lexer_error, find_column, lexer
from AST import *


# To get position span for a specified symbol,
# line and column for start and end
def span(symbol, pos):
    tok = symbol[pos]
    if isinstance(tok, (int, str)):
        lexspan = symbol.lexspan(pos)
        linespan = symbol.linespan(pos)

        startpos = linespan[0], find_column(lexer.lexdata, lexspan[0])
        endpos = linespan[1], find_column(symbol.lexer.lexdata, lexspan[1])
    elif isinstance(tok, list):
        startpos, _ = tok[0].lexspan
        _, endpos = tok[-1].lexspan
    else:
        startpos, endpos = tok.lexspan

    return startpos, endpos


# The first rule to evaluate
# A Setlan program always begins with the reserved word 'program'
# and has one, and only one statement
def p_program(symbol):
    """program : PROGRAM statement"""
    # start, _ = span(symbol, 1)
    # _, end = span(symbol, 2)
    # symbol[0] = Program((start, end), symbol[2])

###############################################################################
#############################     STATEMENTS      #############################
###############################################################################


# The assign statement
# ID '=' expression
def p_statement_assing(symbol):
    """statement : IDENTIFIER ASSIGN expression"""


# The block statement
# starts with 'begin' and ends with 'end'
# It has an optional declarations list and a list of statements
# each declaration and each statement is separated by a ';'
def p_statement_block(symbol):
    """statement : LCURLY statement_list RCURLY
                 | LCURLY USING declare_list IN statement_list RCURLY"""


# A grammar rule to create multiple declarations in a block statement
def p_statement_declare_list(symbol):
    """declare_list : declaration
                    | declare_list declaration"""

# A grammar rule to create a declaration in a list of declarations
def p_statement_declaration(symbol):
    """declaration : data_type declare_comma_list SEMICOLON"""

# A grammar rule to create multiple variables in a declaration
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : IDENTIFIER
                          | declare_comma_list COMMA IDENTIFIER"""


# The type of the declaration
def p_data_type(symbol):
    """data_type : INT
                 | BOOL
                 | SET"""
    symbol[0] = eval(symbol[1].title()) # Assigns the class: Int, Bool or Set


# Multiple statements in a block statement have a separation token, the ';'
def p_statement_statement_list(symbol):
    """statement_list : statement SEMICOLON
                      | statement_list statement SEMICOLON"""
    if len(symbol) == 3:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[2]]

###############################     IN/OUT      ###############################


# The read statement, it works on a variable
def p_statement_read(symbol):
    """statement : SCAN IDENTIFIER"""


# The print statement, it prints on standard output the list of elements
# given to it, in order
def p_statement_write(symbol):
    """statement : PRINT print_comma_list
                 | PRINTLN print_comma_list"""


# To generate the list of elements for a 'print' or a 'println'
def p_statement_print_comma_list(symbol):
    """print_comma_list : printable
                        | print_comma_list COMMA printable"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]

# An expression or a string are both valid printables
def p_statement_print_printable(symbol):
    """printable : expression
                 | STRING"""
    symbol[0] = symbol[1]

############################     CONDITIONAL      #############################


# The if statement, it may or may not have an 'else'
def p_statement_if(symbol):
    """statement : IF LPAREN expression RPAREN statement
                 | IF LPAREN expression RPAREN statement ELSE statement"""


###############################     LOOP      #################################


# The for statement, automatically declares an 'int' variable in the scope of
# the for, this variable has a value of every value in the set specified
def p_statement_for(symbol):
    """statement : FOR IDENTIFIER direction expression DO statement"""

def p_statement_for_direction(symbol):
    """direction : MIN
                 | MAX"""


# The while statement, while some condition holds, keep doing a statement
def p_statement_while(symbol):
    """statement : REPEAT statement WHILE LPAREN expression RPAREN DO statement
                 |                  WHILE LPAREN expression RPAREN DO statement
                 | REPEAT statement WHILE LPAREN expression RPAREN"""

###############################################################################
#############################     EXPRESSIONS     #############################
###############################################################################


# Precedence defined for expressions
precedence = (
    # language
    ("right", 'RPAREN'),
    ("right", 'ELSE'),
    # bool
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),
    # compare
    ("left", 'EQUAL', 'UNEQUAL'),
    ("nonassoc", 'LESS', 'LESSEQ', 'GREATER', 'GREATEREQ'),
    ("nonassoc", 'CONTAINS'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIVIDE', 'MODULO'),
    # set
    ("left", 'UNION', 'DIFFERENCE'),
    ("left", 'INTERSECTION'),
    # int - set
    ("left", 'SPLUS', 'SMINUS'),
    ("left", 'STIMES', 'SDIVIDE', 'SMODULO'),
    # int
    ("right", 'NEGATE', 'SMAX', 'SMIN', 'SSIZE'),
)

##############################     LITERALS     ###############################


# A number is a valid expression
def p_exp_int_literal(symbol):
    """expression : INTEGER"""
    # symbol[0] = Int(span(symbol, 1), symbol[1])


# A boolean is a valid expression
def p_exp_bool_literal(symbol):
    """expression : TRUE
                  | FALSE"""
    # symbol[0] = Bool(span(symbol, 1), symbol[1].upper())


# A set is a valid expression
def p_exp_set_literal(symbol):
    """expression : LCURLY expression_list RCURLY"""

# A list of expressions for sets
def p_exp_list(symbol):
    """expression_list : expression
                       | expression_list COMMA expression"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]


# An ID is a variable expression, since an ID is an int, bool or set
def p_expression_id(symbol):
    """expression : IDENTIFIER"""


# An expression between parenthesis is still an expression
def p_expression_group(symbol):
    """expression : LPAREN expression RPAREN"""

#############################     OPERATORS     ###############################
#############################      BINARY       ###############################

# Binary operations
def p_exp_binary(symbol):
    """expression : expression PLUS         expression
                  | expression MINUS        expression
                  | expression TIMES        expression
                  | expression DIVIDE       expression
                  | expression MODULO       expression
                  | expression UNION        expression
                  | expression DIFFERENCE   expression
                  | expression INTERSECTION expression
                  | expression SPLUS        expression
                  | expression SMINUS       expression
                  | expression STIMES       expression
                  | expression SDIVIDE      expression
                  | expression SMODULO      expression
                  | expression OR           expression
                  | expression AND          expression"""


# Binary operations to compare
def p_exp_compare(symbol):
    """expression : expression LESS      expression
                  | expression LESSEQ    expression
                  | expression GREATER   expression
                  | expression GREATEREQ expression
                  | expression EQUAL     expression
                  | expression UNEQUAL   expression
                  | expression CONTAINS  expression """

#############################       UNARY       ###############################


# Unary minus, defined for int
def p_exp_int_unary(symbol):
    """expression : MINUS expression %prec NEGATE
                  | NOT   expression
                  | SMAX  expression
                  | SMIN  expression
                  | SSIZE expression"""

################################## ERROR ######################################


# Error to be shown if the parser finds a Syntax error
def p_error(symbol):
    if symbol:
        text = lexer.lexdata
        message = "ERROR: unexpected token '%s' at line %d, column %d"
        data = (symbol.value, symbol.lineno, find_column(text, symbol.lexpos))
        parser_error.append(message % data)
    else:
        parser_error.append("ERROR: Syntax error at EOF")


# Build the parser
parser = yacc.yacc(start='program')
parser_error = []


# The file (stored in a Python String) goes through the
# parser and returns an AST that represents the program
def parsing(data, debug=0):
    parser.error = 0
    ast = parser.parse(data, debug=debug)

    if parser.error:
        ast = None

    if ast:
        ast.check()

    return ast

###############################################################################


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
        debug = eval(argv[2])
    else:
        debug = 0

    # Opens file to interpret
    file_string = open(argv[1], 'r').read()

    ast = parsing(file_string, debug)

    if lexer_error:
        ast = None
        for error in lexer_error:
            print error
    elif parser_error:
        ast = None
        for error in parser_error:
            print error
    else:
        print ast

    return ast


# If this is the module running
if __name__ == "__main__":
    main()
