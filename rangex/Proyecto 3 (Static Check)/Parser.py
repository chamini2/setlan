#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Parser for RangeX Language
Alberto Cols, 09-10177
Matteo Ferrando, 09-10285
"""

import ply.yacc as yacc
from Lexer import tokens, lexer_error, find_column, lexer
from AST import *


# To get position span for a specified symbol,
# line and column for start and end
def span(symbol, pos):
    if isinstance(symbol[pos], (int, str)):
        lexspan = symbol.lexspan(pos)
        linespan = symbol.linespan(pos)

        startpos = linespan[0], find_column(lexer.lexdata, lexspan[0])
        endpos = linespan[1], find_column(symbol.lexer.lexdata, lexspan[1])
    elif isinstance(symbol[pos], list):
        startpos, _ = symbol[pos][0].lexspan
        _, endpos = symbol[pos][-1].lexspan
    else:
        startpos, endpos = symbol[pos].lexspan
    return startpos, endpos


# The first rule to evaluate
# A RangeX program always begins with the reserved word 'program'
# and has one, and only one statement next
def p_program(symbol):
    """program : PROGRAM statement"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    symbol[0] = Program((start, end), symbol[2])

###############################################################################
#############################     STATEMENTS      #############################
###############################################################################


# The assign statement
# ID '=' expression
def p_statement_assing(symbol):
    """statement : ID ASSIGN expression"""
    variable = Variable(span(symbol, 1), symbol[1])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)
    symbol[0] = Assign((start, end), variable, symbol[3])


# The block statement
# starts with 'begin' and ends with 'end'
# It has an optional declarations list and a list of statements
# each declaration and each statement is separated by a ';'
def p_statement_block(symbol):
    """statement : BEGIN statement_list END
                 | BEGIN DECLARE declare_list statement_list END"""
    if len(symbol) == 4:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 3)
        symbol[0] = Block((start, end), symbol[2])
    else:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 5)
        symbol[0] = Block((start, end), symbol[4], symbol[3])


# A grammar rule to create multiple declarations in a block statement
def p_statement_declare_list(symbol):
    """declare_list : declare_comma_list AS data_type
                    | declare_list SEMICOLON declare_comma_list AS data_type"""

    def error_already_declared(variable, scope, data_type):
        message = "ERROR: declaring variable '%s' of type '%s' at "
        message += "line %d, column %d with previous declaration "
        message += "of type '%s' at line %d, column %d"
        old_value = scope.find(variable)
        old_lin, old_col = old_value.lexspan[0]
        new_lin, new_col = variable.lexspan[0]
        data = (variable.name, data_type, new_lin, new_col,
                old_value.data_type, old_lin, old_col)
        static_error.append(message % data)

    if len(symbol) == 4:
        scope = SymTable()
        for var in symbol[1]:
            if scope.is_local(var):
                error_already_declared(var, scope, symbol[3])
            else:
                scope.insert(var, symbol[3])
        symbol[0] = scope
    else:
        scope = symbol[1]
        for var in symbol[3]:
            if scope.is_local(var):
                error_already_declared(var, scope, symbol[5])
            else:
                scope.insert(var, symbol[5])
        symbol[0] = scope


# A grammar rule to create multiple variables in a declaration
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : ID
                          | declare_comma_list COMMA ID"""
    if len(symbol) == 2:
        symbol[0] = [Variable(span(symbol, 1), symbol[1])]
    else:
        symbol[0] = symbol[1] + [Variable(span(symbol, 3), symbol[3])]


# For the 'as' part of a declaration
def p_data_type(symbol):
    """data_type : INT
                 | BOOL
                 | RANGE"""
    symbol[0] = symbol[1].upper()


# Multiple statements in a block statement have a separation token, the ';'
def p_statement_statement_list(symbol):
    """statement_list : statement
                      | statement_list SEMICOLON statement"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]

###############################     IN/OUT      ###############################


# The read statement, it works on a variable
def p_statement_read(symbol):
    """statement : READ ID"""
    variable = Variable(span(symbol, 2), symbol[2])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    symbol[0] = Read((start, end), variable)


# The write statement, it prints on standard output the list of elements
# given to it, in order
def p_statement_write(symbol):
    """statement : WRITE comma_list
                 | WRITELN comma_list"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    if symbol[1].upper() == 'WRITE':
        symbol[0] = Write((start, end), symbol[2])
    else:
        symbol[0] = WriteLn((start, end), symbol[2])


# To generate the list of elements for a 'write' or a 'writeln'
def p_statement_comma_list(symbol):
    """comma_list : printable
                  | comma_list COMMA printable"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]


# A string is a valid printable
def p_print_string_literal(symbol):
    """printable : STRING"""
    symbol[0] = String(span(symbol, 1), symbol[1])


# An expression is a valid printable
def p_exp_print(symbol):
    """printable : expression"""
    symbol[0] = symbol[1]

############################     CONDITIONAL      #############################


# The if statement, it may or may not have an 'else'
def p_statement_if(symbol):
    """statement : IF expression THEN statement
                 | IF expression THEN statement ELSE statement"""
    if len(symbol) == 5:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 4)
        symbol[0] = If((start, end), symbol[2], symbol[4])
    else:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 6)
        symbol[0] = If((start, end), symbol[2], symbol[4], symbol[6])


# The case statement, an integer to check if is in a series of ranges
# If in the range, run the statement for this one
def p_statement_case(symbol):
    """statement : CASE expression OF case_list END"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 5)
    symbol[0] = CaseOf((start, end), symbol[2], symbol[4])


# A list of range '->' statement
def p_statement_case_list(symbol):
    """case_list : expression ARROW statement SEMICOLON
                 | case_list expression ARROW statement SEMICOLON"""
    if len(symbol) == 5:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 4)
        case = Case((start, end), symbol[1], symbol[3])
        symbol[0] = [case]
    else:
        start, _ = span(symbol, 2)
        _, end = span(symbol, 5)
        case = Case((start, end), symbol[2], symbol[4])
        symbol[0] = symbol[1] + [case]

###############################     LOOP      #################################


# The for statement, automatically declares an 'int' variable in the scope of
# the for, this variable has a value of every value in the range specified
def p_statement_for(symbol):
    """statement : FOR ID IN expression DO statement"""
    variable = Variable(span(symbol, 2), symbol[2])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 6)
    symbol[0] = For((start, end), variable, symbol[4], symbol[6])


# The while statement, while some condition holds, keep doing a statement
def p_statement_while(symbol):
    """statement : WHILE expression DO statement"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 4)
    symbol[0] = While((start, end), symbol[2], symbol[4])

###############################################################################
#############################     EXPRESSIONS     #############################
###############################################################################


# Precedence defined for expressions
precedence = (
    # language
    ("right", 'IF'),
    ("right", 'THEN'),
    ("right", 'ELSE'),
    # bool
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),
    # compare
    ("nonassoc", 'BELONG'),
    ("nonassoc", 'EQUAL', 'UNEQUAL'),
    ("nonassoc", 'LESS', 'LESSEQ', 'GREAT', 'GREATEQ'),
    # range
    ("left", 'INTERSECTION'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIVIDE', 'MODULO'),
    # range
    ("nonassoc", 'FROMTO'),
    # int
    ("right", 'UMINUS'),
)

##############################     LITERALS     ###############################


# A number is a valid expression
def p_exp_int_literal(symbol):
    """expression : NUMBER"""
    symbol[0] = Int(span(symbol, 1), symbol[1])


# A boolean is a valid expression
def p_exp_bool_literal(symbol):
    """expression : TRUE
                  | FALSE"""
    symbol[0] = Bool(span(symbol, 1), symbol[1].upper())


# A range is a valid expression
def p_exp_range_literal(symbol):
    """expression : expression FROMTO expression"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)
    symbol[0] = Range((start, end), symbol[1], symbol[3])


# An ID is a variable expression, since an ID is an int, bool or range
def p_expression_id(symbol):
    """expression : ID"""
    symbol[0] = Variable(span(symbol, 1), symbol[1])


# An expression between parenthesis is still an expression
def p_expression_group(symbol):
    """expression : LPAREN expression RPAREN"""
    symbol[0] = symbol[2]
    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)
    symbol[0].lexspan = start, end

#############################     OPERATORS     ###############################
#############################      BINARY       ###############################


# Binary operations
def p_exp_binary(symbol):
    """expression : expression PLUS         expression
                  | expression MINUS        expression
                  | expression TIMES        expression
                  | expression DIVIDE       expression
                  | expression MODULO       expression
                  | expression INTERSECTION expression
                  | expression OR           expression
                  | expression AND          expression
                  | expression BELONG       expression"""
    operator = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'TIMES',
        '/': 'DIVIDE',
        '%': 'MODULO',
        '<>': 'INTERSECTION',
        'or': 'OR',
        'and': 'AND',
        '>>': 'BELONG'
    }.get(symbol[2], None)

    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)

    if operator == 'PLUS':
        symbol[0] = Plus((start, end), symbol[1], symbol[3])
    elif operator == 'MINUS':
        symbol[0] = Minus((start, end), symbol[1], symbol[3])
    elif operator == 'TIMES':
        symbol[0] = Times((start, end), symbol[1], symbol[3])
    elif operator == 'DIVIDE':
        symbol[0] = Divide((start, end), symbol[1], symbol[3])
    elif operator == 'MODULO':
        symbol[0] = Modulo((start, end), symbol[1], symbol[3])
    elif operator == 'INTERSECTION':
        symbol[0] = Intersection((start, end), symbol[1], symbol[3])
    elif operator == 'OR':
        symbol[0] = Or((start, end), symbol[1], symbol[3])
    elif operator == 'AND':
        symbol[0] = And((start, end), symbol[1], symbol[3])
    elif operator == 'BELONG':
        symbol[0] = Belong((start, end), symbol[1], symbol[3])
    else:
        symbol[0] = Binary((start, end), operator, symbol[1], symbol[3])


# Binary operations to compare
def p_exp_compare(symbol):
    """expression : expression LESS    expression
                  | expression LESSEQ  expression
                  | expression GREAT   expression
                  | expression GREATEQ expression
                  | expression EQUAL   expression
                  | expression UNEQUAL expression"""
    operator = {
        '<': 'LESS',
        '<=': 'LESSEQ',
        '>': 'GREAT',
        '>=': 'GREATEQ',
        '==': 'EQUAL',
        '/=': 'UNEQUAL'
    }.get(symbol[2], None)

    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)

    if operator == 'LESS':
        symbol[0] = Less((start, end), symbol[1], symbol[3])
    elif operator == 'LESSEQ':
        symbol[0] = LessEq((start, end), symbol[1], symbol[3])
    elif operator == 'GREAT':
        symbol[0] = Great((start, end), symbol[1], symbol[3])
    elif operator == 'GREATEQ':
        symbol[0] = GreatEq((start, end), symbol[1], symbol[3])
    elif operator == 'EQUAL':
        symbol[0] = Equal((start, end), symbol[1], symbol[3])
    elif operator == 'UNEQUAL':
        symbol[0] = Unequal((start, end), symbol[1], symbol[3])
    else:
        symbol[0] = Binary((start, end), operator, symbol[1], symbol[3])

#############################       UNARY       ###############################


# Unary minus, defined for int
def p_exp_int_unary(symbol):
    """expression : MINUS expression %prec UMINUS
                  | NOT expression"""
    operator = {
        '-': 'MINUS',
        'not': 'NOT'
    }.get(symbol[1], None)

    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)

    if operator == 'MINUS':
        symbol[0] = UMinus((start, end), symbol[2])
    elif operator == 'NOT':
        symbol[0] = Not((start, end), symbol[2])
    else:
        symbol[0] = Unary((start, end), operator, symbol[2])


# Considered these functions as unary operators for range
def p_exp_int_range_unary(symbol):
    """expression : RTOI   LPAREN expression RPAREN
                  | LENGTH LPAREN expression RPAREN
                  | TOP    LPAREN expression RPAREN
                  | BOTTOM LPAREN expression RPAREN"""
    operator = symbol[1].upper()

    start, _ = span(symbol, 1)
    _, end = span(symbol, 4)

    if operator == 'RTOI':
        symbol[0] = RtoI((start, end), symbol[3])
    elif operator == 'LENGTH':
        symbol[0] = Length((start, end), symbol[3])
    elif operator == 'TOP':
        symbol[0] = Top((start, end), symbol[3])
    elif operator == 'BOTTOM':
        symbol[0] = Bottom((start, end), symbol[3])
    else:
        symbol[0] = Unary((start, end), operator, symbol[3])

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
