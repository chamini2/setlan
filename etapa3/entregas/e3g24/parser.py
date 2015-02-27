#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""Parser para el lenguaje Setlan
Fabio, Castro 10-10132
Antonio, Scaramazza 11-10957
"""

import ply.yacc as yacc
from lexer import tokens, lexer_error, find_column, lexer
from ast import *


# Obtener margen de posicion de un simbolo
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





# Primera regla a evaluar
# Un programa Setlan siempre comienza con la palabra reservada 'program'
def p_program(symbol):
    """program : PROGRAM statement"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    symbol[0] = Program((start, end), symbol[2])

###############################################################################
#############################     STATEMENTS      #############################
###############################################################################


# Declaracion de asignacion
# ID '=' expresion
def p_statement_assing(symbol):
    """statement : ID ASSIGN expression"""
    variable = Variable(span(symbol, 1), symbol[1])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)
    symbol[0] = Assign((start, end), variable, symbol[3])



# Declaracion de bloque
# posee un bloque opcional de declaracion de variables
# este comienza con 'using' y termina con 'in'
def p_statement_block(symbol):
    """statement : OPENCURLY statement_list CLOSECURLY
                 | OPENCURLY USING declare_list IN statement_list CLOSECURLY"""
    if len(symbol) == 4:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 3)
        symbol[0] = Block((start, end), symbol[2])
    else:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 6)
        symbol[0] = Block((start, end), symbol[5], symbol[3])


# Regla de la gramatica para declarar el tipo de una variable
def p_statement_declare_list(symbol):
    """declare_list : data_type declare_comma_list SEMICOLON
                    | declare_list data_type declare_comma_list SEMICOLON"""
    
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
        for var in symbol[2]:
            if scope.is_local(var):
                error_already_declared(var, scope, symbol[1])
            else:
                scope.insert(var, symbol[1])
        symbol[0] = scope
    else:
        scope = symbol[1]
        for var in symbol[3]:
            if scope.is_local(var):
                error_already_declared(var, scope, symbol[2])
            else:
                scope.insert(var, symbol[2])
        symbol[0] = scope


# Regla para crear una lista con el nombre de las variables
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : ID
                          | declare_comma_list COMMA ID"""
    if len(symbol) == 2:
        symbol[0] = [Variable(span(symbol, 1), symbol[1])]
    else:
        symbol[0] = symbol[1] + [Variable(span(symbol, 3), symbol[3])]


# Las declaraciones se separan por un ';'
def p_statement_statement_list(symbol):
    """statement_list : 
                      | statement_list statement SEMICOLON"""
    if len(symbol) == 1:
        symbol[0] = []
    else:
        symbol[0] = symbol[1] + [symbol[2]]


# Tipos permitidos del lenguaje
def p_data_type(symbol):
    """data_type : INT
                 | BOOL
                 | SET """
    symbol[0] = symbol[1].upper()

###############################     IN/OUT      ###############################


# Declaracion scan, se aplica sobre una variable 
def p_statement_scan(symbol):
    "statement : SCAN ID"
    variable = Variable(span(symbol, 2), symbol[2])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    symbol[0] = Scan((start, end), variable)


# Comando 'print', muestra por pantalla las expresiones dadas
def p_statement_print(symbol):
    """statement : PRINT comma_list
                 | PRINTLN comma_list"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    if symbol[1].upper() == 'PRINT':
        symbol[0] = Print((start, end), symbol[2])
    else:
        symbol[0] = PrintLn((start, end), symbol[2])


# Lista de elementos a imprimir con la funcion 'print' 
def p_statement_comma_list(symbol):
    """comma_list : expression
                  | comma_list COMMA expression"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]



############################     CONDICIONALES      #############################


# Declaracion 'IF', puedo o no haber 'ELSE"
def p_statement_if(symbol):
    """statement :  IF OPENPAREN expression CLOSEPAREN  statement ELSE statement
                  |   IF OPENPAREN expression CLOSEPAREN  statement  """
    if len(symbol) == 6:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 5)
        symbol[0] = If((start, end), symbol[3], symbol[5])
    else:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 7)
        symbol[0] = If((start, end), symbol[3], symbol[5], symbol[7])


###############################     LAZOS      #################################


# Declaracion for, la variable recorre el conjunto en la direccion indicada
def p_statement_for(symbol):
    """statement : FOR ID MAX expression DO statement
                 | FOR ID MIN expression DO statement"""
    variable = Variable(span(symbol, 2), symbol[2])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 6)
    symbol[0] = For((start, end), variable,symbol[4], symbol[6], symbol[3])

# Declaracion while-do, despues de pasar el chequeo de guarda,
# se realizan las expresiones en el bloque
def p_statement_while(symbol):
    "statement : WHILE OPENPAREN expression CLOSEPAREN DO statement"
    start, _ = span(symbol, 1)
    _, end = span(symbol, 6)
    symbol[0] = While((start, end), symbol[3], symbol[6])

# Declaracion repeat-while, realiza las instruciones en el bloque,
# luego evalua la expresion en el while, si se cumple vuelve al bloque
def p_statement_repeat(symbol):
    "statement : REPEAT statement WHILE OPENPAREN expression CLOSEPAREN "
    start, _ = span(symbol, 1)
    _, end = span(symbol, 6)
    symbol[0] = Repeat((start, end), symbol[2], symbol[5])


# Combinacion de ambos lazos
def p_statement_repeat_while(symbol):
    "statement : REPEAT statement WHILE OPENPAREN expression CLOSEPAREN DO statement"
    start, _ = span(symbol, 1)
    _, end = span(symbol, 8)
    symbol[0] = RepeatWhile((start, end), symbol[2], symbol[5], symbol[8])


###############################################################################
#############################     EXPRESIONES     #############################
###############################################################################


# Precedencia de los operadores
precedence = (
    # lenguaje
    ("right", 'CLOSEPAREN'),
    ("right", 'ELSE'),
    # booleano
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),

    # comparador
    ("nonassoc", 'SETBELONG'),
    ("nonassoc", 'EQUAL', 'UNEQUAL'),
    ("nonassoc", 'LESS', 'LESSEQ', 'GREAT', 'GREATEQ'),
    # conjunto 
    ("left", 'SETUNION','SETDIFFERENCE'),
    ("left",'SETINTERSECTION'),
    ("right",'SETMAX','SETMIN','SETLEN'),
    # int sobre conjunto
    ("left", 'SETPLUS','SETMINUS'),
    ("left", 'SETTIMES','SETDIVITION','SETMOD'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'DIVIDE', 'MODULE'), 
    ("right", 'UMINUS'),
)

##############################     TIPOS     ###############################


# Numeros
def p_exp_int_literal(symbol):
    "expression : NUMBER"
    symbol[0] = Int(span(symbol, 1), symbol[1])

# Booleanos
def p_exp_bool_literal(symbol):
    """expression : TRUE
                  | FALSE"""
    symbol[0] = Bool(span(symbol, 1), symbol[1].upper())

# Conjuntos
def p_exp_set_literal(symbol):
    """expression : OPENCURLY comma_list CLOSECURLY
                  | OPENCURLY CLOSECURLY """
    if len(symbol) == 4:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 3)
        symbol[0] = Set((start, end), symbol[2])
    else:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 2)
        symbol[0] = Set((start, end), None)

# Cadena de caracteres
def p_exp_string_literal(symbol):
    "expression : STRING"
    symbol[0] = String(span(symbol, 1),symbol[1])


# Variables
def p_expression_id(symbol):
    "expression : ID"
    symbol[0] = Variable(span(symbol, 1), symbol[1])


# Expresiones entre parentesis
def p_expression_group(symbol):
    """expression : OPENPAREN expression CLOSEPAREN"""
    symbol[0] = symbol[2]
    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)
    symbol[0].lexspan = start, end

#############################    OPERADORES     ###############################


# Operadores bianrios de enteros
def p_exp_binary(symbol):
    """expression : expression PLUS   expression
                  | expression MINUS  expression
                  | expression TIMES  expression
                  | expression DIVIDE expression
                  | expression MODULE expression
                  | expression SETUNION expression
                  | expression SETINTERSECTION expression
                  | expression SETDIFFERENCE expression 
                  | expression SETPLUS   expression
                  | expression SETMINUS  expression
                  | expression SETTIMES  expression
                  | expression SETDIVITION expression
                  | expression SETMOD expression
                  | expression OR           expression
                  | expression AND          expression
                  | expression SETBELONG       expression"""
    operator = {
        '+': 'PLUS',
        '-': 'MINUS',
        '*': 'TIMES',
        '/': 'DIVIDE',
        '%': 'MODULE',
        '++': 'SETUNION',
        '><': 'SETINTERSECTION',
        '\\': 'SETDIFFERENCE',
        '<+>': 'SETPLUS',
        '<->': 'SETMINUS',
        '<*>': 'SETTIMES',
        '</>': 'SETDIVITION',
        '<%>': 'SETMOD',
        'or': 'OR',
        'and': 'AND',
        '@': 'SETBELONG'
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
    elif operator == 'MODULE':
        symbol[0] = Module((start, end), symbol[1], symbol[3])
    elif operator == 'SETUNION':
        symbol[0] = Setunion((start, end), symbol[1], symbol[3])
    elif operator == 'SETINTERSECTION':
        symbol[0] = Setintersection((start, end), symbol[1], symbol[3])
    elif operator == 'SETDIFFERENCE':
        symbol[0] = Setdifference((start, end), symbol[1], symbol[3])
    elif operator == 'SETPLUS':
        symbol[0] = Setplus((start, end), symbol[1], symbol[3])
    elif operator == 'SETMINUS':
        symbol[0] = Setminus((start, end), symbol[1], symbol[3])
    elif operator == 'SETTIMES':
        symbol[0] = Settimes((start, end), symbol[1], symbol[3])
    elif operator == 'SETDIVITION':
        symbol[0] = Setdivition((start, end), symbol[1], symbol[3])
    elif operator == 'SETMOD':
        symbol[0] = Setmod((start, end), symbol[1], symbol[3])
    elif operator == 'OR':
        symbol[0] = Or((start, end), symbol[1], symbol[3])
    elif operator == 'AND':
        symbol[0] = And((start, end), symbol[1], symbol[3])
    elif operator == 'SETBELONG':
        symbol[0] = Setbelong((start, end), symbol[1], symbol[3])
    else:
        symbol[0] = Binary((start, end), operator, symbol[1], symbol[3])

# Operadores binarios de comparacion
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


# Menos unario para enteros
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


# Operadores unarios de conjuntos
def p_exp_set_unary(symbol):
    """expression : SETMAX   expression 
                  | SETMIN   expression 
                  | SETLEN   expression """
    operator = {
        '>?': 'SETMAX',
        '<?': 'SETMIN',
        '$?': 'SETLEN'
    }[symbol[1]].upper()              

    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)       
    if operator == 'SETMAX':
        symbol[0] = Setmax((start, end), symbol[2])
    elif operator == 'SETMIN':
        symbol[0] = Setmin((start, end), symbol[2])
    elif operator == 'SETLEN':
        symbol[0] = Setlen((start, end), symbol[2])
    else:
        symbol[0] = Unary((start, end), operator, symbol[2])




# Error a imprimir si el parser encuentra un error
def p_error(symbol):
    if symbol:
        text = lexer.lexdata
        message = "ERROR: unexpected token '%s' at line %d, column %d"
        data = (symbol.value, symbol.lineno, find_column(text, symbol.lexpos))
        parser_error.append(message % data)
    else:
        parser_error.append("ERROR: Syntax error at EOF")


# Generar el parser
parser = yacc.yacc(start='program')
parser_error = []


# EL archivo pasa por el parser, y es devuelto como el AST
def parsing(data, debug=0):
    parser.error = 0
    ast = parser.parse(data, debug=debug)
    if parser.error:
        ast = None
    if ast:
        ast.check()
    return ast

###############################################################################



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



if __name__ == "__main__":
    main()
