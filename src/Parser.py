"""
Parser for Setlan
Matteo Ferrando, 09-10285
"""

import ply.yacc as yacc

import Errors
from Lexer import tokens, find_column, lexer
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

# to get the position span from a symbol to other
def from_to_span(symbol, from_pos, to_pos):
    start, _ = span(symbol, from_pos)
    _, end = span(symbol, to_pos)
    return start, end


# The first rule to evaluate
# A Setlan program always begins with the reserved word 'program'
# and has one, and only one statement
def p_program(symbol):
    """program : PROGRAM statement"""
    pos = from_to_span(symbol, 1, 2)
    symbol[0] = Program(pos, symbol[2])

###############################################################################
#############################     STATEMENTS      #############################
###############################################################################


# The assign statement
# ID '=' expression
def p_statement_assing(symbol):
    """statement : IDENTIFIER ASSIGN expression"""
    pos = from_to_span(symbol, 1, 3)
    variable = Variable(span(symbol, 1), symbol[1])
    symbol[0] = Assign(pos, variable, symbol[3])


# The block statement
# starts with 'begin' and ends with 'end'
# It has an optional declarations list and a list of statements
# each declaration and each statement is separated by a ';'
def p_statement_block(symbol):
    """statement : LCURLY maybe_statement_list RCURLY
                 | LCURLY USING declare_list IN maybe_statement_list RCURLY"""
    if len(symbol) == 4:
        pos = from_to_span(symbol, 1, 3)
        statements = symbol[2]
        declarations = [] # whatevs
    else:
        pos = from_to_span(symbol, 1, 6)
        statements = symbol[5]
        declarations = symbol[3]

    symbol[0] = Block(pos, statements, declarations)


# A grammar rule to create multiple declarations in a block statement
def p_statement_declare_list(symbol):
    """declare_list : declaration
                    | declare_list declaration"""
    if len(symbol) == 2:
        symbol[0] = symbol[1]
    else:
        symbol[0] = symbol[1] + symbol[2]

# A grammar rule to create a declaration in a list of declarations
def p_statement_declaration(symbol):
    """declaration : data_type declare_comma_list SEMICOLON"""
    symbol[0] = map(lambda var: (symbol[1], var), symbol[2])

# A grammar rule to create multiple variables in a declaration
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : IDENTIFIER
                          | declare_comma_list COMMA IDENTIFIER"""
    if len(symbol) == 2:
        variable = Variable(span(symbol, 1), symbol[1])
        symbol[0] = [variable]
    else:
        variable = Variable(span(symbol, 3), symbol[3])
        symbol[0] = symbol[1] + [variable]

# The type of the declaration
def p_data_type(symbol):
    """data_type : INT
                 | BOOL
                 | SET"""
    # Assigns the class: Int_Type, Bool_Type or Set_Type
    symbol[0] = symbol[1].lower()

# A list of expressions for sets
def p_may_statement_list(symbol):
    """maybe_statement_list : 
                            | statement_list"""
    if len(symbol) == 1:
        symbol[0] = []
    else:
        symbol[0] = symbol[1]

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
def p_statement_scan(symbol):
    """statement : SCAN IDENTIFIER"""
    pos = from_to_span(symbol, 1, 2)
    variable = Variable(span(symbol, 2), symbol[2])
    symbol[0] = Scan(pos, variable)

# The print statement, it prints on standard output the list of elements
# given to it, in order
def p_statement_print(symbol):
    """statement : PRINT print_comma_list
                 | PRINTLN print_comma_list"""
    pos = from_to_span(symbol, 1, 2)
    printables = symbol[2]
    if symbol[1].lower() == 'println':
        _, end = pos
        printables += [String((end, end),r'"\n"')]
    symbol[0] = Print(pos, printables)

# To generate the list of elements for a 'print' or a 'println'
def p_statement_print_comma_list(symbol):
    """print_comma_list : printable
                        | print_comma_list COMMA printable"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]

# An expression is a valid printable
def p_statement_print_printable_exp(symbol):
    """printable : expression"""
    symbol[0] = symbol[1]

# A string is a valid printables
def p_statement_print_printable_str(symbol):
    """printable : STRING"""
    symbol[0] = String(span(symbol, 1), symbol[1])

############################     CONDITIONAL      #############################


# The if statement, it may or may not have an 'else'
def p_statement_if(symbol):
    """statement : IF LPAREN expression RPAREN statement
                 | IF LPAREN expression RPAREN statement ELSE statement"""
    if len(symbol) == 6:
        pos = from_to_span(symbol, 1, 5)
        else_st = None
    else:
        pos = from_to_span(symbol, 1, 7)
        else_st = symbol[7]
    condition = symbol[3]
    then_st = symbol[5]
    symbol[0] = If(pos, condition, then_st, else_st)

###############################     LOOP      #################################


# The for statement, automatically declares an 'int' variable in the scope of
# the for, this variable has a value of every value in the set specified
def p_statement_for(symbol):
    """statement : FOR IDENTIFIER direction expression DO statement"""
    pos = from_to_span(symbol, 1, 6)
    variable = Variable(span(symbol, 2), symbol[2])
    symbol[0] = For(pos, variable, symbol[3], symbol[4], symbol[6])

def p_statement_for_direction(symbol):
    """direction : MIN
                 | MAX"""
    symbol[0] = symbol[1].lower()


# The while statement, while some condition holds, keep doing a statement
def p_statement_while(symbol):
    """statement : REPEAT statement WHILE LPAREN expression RPAREN DO statement
                 |                  WHILE LPAREN expression RPAREN DO statement
                 | REPEAT statement WHILE LPAREN expression RPAREN"""
    if len(symbol) == 9:
        pos = from_to_span(symbol, 1, 8)
        repeat_st = symbol[2]
        condition = symbol[5]
        do_st = symbol[8]
    else:
        pos = from_to_span(symbol, 1, 6)
        if symbol[1].lower() == 'while':
            repeat_st = None
            condition = symbol[3]
            do_st = symbol[6]
        elif symbol[1].lower() == 'repeat':
            repeat_st = symbol[2]
            condition = symbol[5]
            do_st = None
    symbol[0] = While(pos, repeat_st, condition, do_st)


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
    # unary
    ("right", 'NEGATE', 'SMAX', 'SMIN', 'SSIZE'),
)

##############################     LITERALS     ###############################


# A number is a valid expression
def p_exp_int_literal(symbol):
    """expression : INTEGER"""
    symbol[0] = Int(span(symbol, 1), symbol[1])


# A boolean is a valid expression
def p_exp_bool_literal(symbol):
    """expression : TRUE
                  | FALSE"""
    symbol[0] = Bool(span(symbol, 1), eval(symbol[1].title()))


# A set is a valid expression
def p_exp_set_literal(symbol):
    """expression : LCURLY maybe_expression_list RCURLY"""
    symbol[0] = Set(from_to_span(symbol, 1, 3), symbol[2])

# A list of expressions for sets
def p_may_exp_list(symbol):
    """maybe_expression_list : 
                             | expression_list"""
    if len(symbol) == 1:
        symbol[0] = []
    else:
        symbol[0] = symbol[1]

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
    symbol[0] = Variable(span(symbol, 1), symbol[1])

# An expression between parenthesis is still an expression
def p_expression_parenthesis(symbol):
    """expression : LPAREN expression RPAREN"""
    symbol[0] = symbol[2]
    symbol[0].lexspan = from_to_span(symbol, 1, 3)

#############################     OPERATORS     ###############################
#############################      BINARY       ###############################

# Binary operations
def p_exp_binary(symbol):
    """expression : expression PLUS   expression
                  | expression MINUS  expression
                  | expression TIMES  expression
                  | expression DIVIDE expression
                  | expression MODULO expression

                  | expression UNION        expression
                  | expression DIFFERENCE   expression
                  | expression INTERSECTION expression

                  | expression SPLUS   expression
                  | expression SMINUS  expression
                  | expression STIMES  expression
                  | expression SDIVIDE expression
                  | expression SMODULO expression

                  | expression OR  expression
                  | expression AND expression

                  | expression LESS      expression
                  | expression LESSEQ    expression
                  | expression GREATER   expression
                  | expression GREATEREQ expression
                  | expression EQUAL     expression
                  | expression UNEQUAL   expression
                  | expression CONTAINS  expression"""
    pos = from_to_span(symbol, 1, 3)
    if symbol[2] == '+':
        exp = Plus(pos, symbol[1], symbol[3])
    elif symbol[2] == '-':
        exp = Minus(pos, symbol[1], symbol[3])
    elif symbol[2] == '*':
        exp = Times(pos, symbol[1], symbol[3])
    elif symbol[2] == '/':
        exp = Divide(pos, symbol[1], symbol[3])
    elif symbol[2] == '%':
        exp = Modulo(pos, symbol[1], symbol[3])
    elif symbol[2] == '++':
        exp = Union(pos, symbol[1], symbol[3])
    elif symbol[2] == '\\':
        exp = Difference(pos, symbol[1], symbol[3])
    elif symbol[2] == '><':
        exp = Intersection(pos, symbol[1], symbol[3])
    elif symbol[2] == '<+>':
        exp = SetPlus(pos, symbol[1], symbol[3])
    elif symbol[2] == '<->':
        exp = SetMinus(pos, symbol[1], symbol[3])
    elif symbol[2] == '<*>':
        exp = SetTimes(pos, symbol[1], symbol[3])
    elif symbol[2] == '</>':
        exp = SetDivide(pos, symbol[1], symbol[3])
    elif symbol[2] == '<%>':
        exp = SetModulo(pos, symbol[1], symbol[3])
    elif symbol[2] == 'or':
        exp = Or(pos, symbol[1], symbol[3])
    elif symbol[2] == 'and':
        exp = And(pos, symbol[1], symbol[3])
    elif symbol[2] == '<':
        exp = Less(pos, symbol[1], symbol[3])
    elif symbol[2] == '<=':
        exp = LessEq(pos, symbol[1], symbol[3])
    elif symbol[2] == '>':
        exp = Greater(pos, symbol[1], symbol[3])
    elif symbol[2] == '>=':
        exp = GreaterEq(pos, symbol[1], symbol[3])
    elif symbol[2] == '==':
        exp = Equal(pos, symbol[1], symbol[3])
    elif symbol[2] == '/=':
        exp = Unequal(pos, symbol[1], symbol[3])
    elif symbol[2] == '@':
        exp = Contains(pos, symbol[1], symbol[3])
    symbol[0] = exp

#############################       UNARY       ###############################


# Unary minus, defined for int
def p_exp_int_unary(symbol):
    """expression : MINUS expression %prec NEGATE
                  | NOT   expression
                  | SMAX  expression
                  | SMIN  expression
                  | SSIZE expression"""
    pos = from_to_span(symbol, 1, 2)
    if symbol[1] == '-':
        exp = Negate(pos, symbol[2])
    elif symbol[1] == 'not':
        exp = Not(pos, symbol[2])
    elif symbol[1] == '>?':
        exp = Max(pos, symbol[2])
    elif symbol[1] == '<?':
        exp = Min(pos, symbol[2])
    elif symbol[1] == '$?':
        exp = Size(pos, symbol[2])
    symbol[0] = exp

################################## ERROR ######################################


# Error to be shown if the parser finds a Syntax error
def p_error(symbol):
    if symbol:
        text = lexer.lexdata
        message = "ERROR: unexpected token '%s' at line %d, column %d"
        data = (symbol.value, symbol.lineno, find_column(text, symbol.lexpos))
        Errors.parser_error.append(message % data)
    else:
        Errors.parser_error.append("ERROR: Syntax error at EOF")


# Build the parser
parser = yacc.yacc(start='program')


# The file (stored in a Python String) goes through the
# parser and returns an AST that represents the program
def parsing(data, debug=0):
    parser.error = 0
    ast = parser.parse(data, debug=debug)

    if parser.error:
        ast = None

    return ast
