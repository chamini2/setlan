#!/usr/bin/env python
# -*- coding: UTF-8 -*-

############################
#  Proyecto I - CI3725     #
#  Grupo 2                 #
#  Luis Colorado 09-11086  #
#  Nicolas Manan 06-39883  #
############################

import ply.yacc as yacc
from Lexer import tokens, lexer_error, find_column, lexer
from ast import *

# Toma la posicion de un simbolo especifico, linea y columna
# To get position span for a specified symbol,
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

############# INICIO DE LA GRAMATICA SETLAN ###################

# Inicio de un programa Setlan
def p_program(symbol):
    "program : TokenProgram statement"
    start, _ = span(symbol,1)
    _, end = span(symbol,2)
    symbol[0] = Program((start,end),symbol[2])

################### STATEMENTS ################################

# La sentencia de bloque con sus multiples formas de escritura
def p_statement_block(symbol):
    """statement : TokenOpenCurly statement_list TokenCloseCurly
                 | TokenOpenCurly TokenUsing declare_list TokenIn statement_list TokenCloseCurly
                 | TokenOpenCurly empty empty TokenCloseCurly"""
    if len(symbol) == 4:
        start, _ = span(symbol,1)
        _, end = span(symbol,3)
        symbol[0] = Block((start,end),symbol[2])
    elif len(symbol) == 5:
        start, _ = span(symbol,1)
        _, end = span(symbol,4)
        symbol[0] =  Block((start,end),symbol[2],None,None,1)
    else:
        start, _ = span(symbol,1)
        _, end = span(symbol,6)
        symbol[0] = Block((start,end),symbol[5], symbol[3], symbol[2])

# Asignacion de Variables
def p_statement_assign(symbol):
    "statement : TokenID TokenAssign expression"
    variable = Variable(span(symbol,1),symbol[1])
    start, _ = span(symbol,1)
    _, end = span(symbol,3)
    symbol[0] = Assign((start,end),variable,symbol[3])


############# Entrada y Salida ################

# Lectura de variables dadas por el usuario
def p_statement_scan(symbol):
    "statement : TokenScan TokenID"
    variable = Variable(span(symbol,2),symbol[2])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    symbol[0] = Scan((start,end),variable)


# Declaracion de impresion
def p_statement_print(symbol):
    """statement : TokenPrint comma_list
                 | TokenPrintln comma_list"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)
    if symbol[1].upper() == 'TokenPrint':
        symbol[0] = Print((start, end), symbol[2])
    else:
        symbol[0] = Print((start, end), symbol[2])
################## Lista de instrucciones (statement) #################

# Multiples declaraciones en un bloque separadas por ';'
def p_statement_statement_list(symbol):
    """statement_list : statement
                      | statement_list TokenSemicolon statement """
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]


############## Declarar Variables #############

# Regla gramatica para crear multiples declaraciones en un bloque
def p_statement_declare_list(symbol):
    """declare_list : data_type declare_comma_list TokenSemicolon
                    | data_type declare_comma_list TokenSemicolon declare_list"""
    
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
        scope = Table()
        for var in symbol[2]:
            if scope.is_local(var):
                error_already_declared(var,scope,symbol[1])
            else:
                scope.insert(var,symbol[1])
        symbol[0] = scope
    else:
        scope = symbol[4]
        for var in symbol[2]:
            if scope.is_local(var):
                error_already_declared(var,scope,symbol[1])
            else:
                scope.insert(var,symbol[1]) 
        symbol[0] = scope


# Regla para crear multiples variables en una declaracion
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : TokenID
                          | declare_comma_list TokenComma TokenID"""
    if len(symbol) == 2:
        symbol[0] = [Variable(span(symbol,1),symbol[1])]
    else:
        symbol[0] = symbol[1] + [Variable(span(symbol,3),symbol[3])]


############## Condicional ####################

# La declaracion 'If'
def p_statement_if(symbol):
    """statement : TokenIf expression statement
                 | TokenIf expression statement TokenElse statement"""
    if len(symbol) == 4:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 3)
        symbol[0] = If((start,end),symbol[2], symbol[3])
    else:
        start, _ = span(symbol, 1)
        _, end = span(symbol, 5)
        symbol[0] = If((start,end),symbol[2], symbol[3], symbol[5])


################## Ciclos #####################

# Declaracion del for
def p_statement_for(symbol):
    """statement : TokenFor TokenID TokenMin expression TokenDo statement
                 | TokenFor TokenID TokenMax expression TokenDo statement"""
    variable = Variable(span(symbol,2),symbol[2])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 6)
    symbol[0] = For((start,end),variable, symbol[4], symbol[6],symbol[3])


# Declaracion While
def p_statement_while(symbol):
    "statement : TokenWhile expression TokenDo statement"
    start, _ = span(symbol, 1)
    _, end = span(symbol, 4)
    symbol[0] = While((start, end),symbol[2], symbol[4])

# Declaracion Repeat
def p_statement_whileRepeat(symbol):
    """statement : TokenRepeat statement_list TokenWhile expression TokenDo statement"""
    start, _ = span(symbol, 1)
    _, end = span(symbol, 6)
    symbol[0] = WhileRepeat((start,end),symbol[4],symbol[2],symbol[6])

def p_statement_repeatWhile(symbol):
    " statement : TokenRepeat statement_list TokenWhile expression "
    start, _ = span(symbol, 1)
    _, end = span(symbol, 4)
    symbol[0] = RepeatWhile((start,end),symbol[4], symbol[2])
######################## Tipos de Datos #######################

# Para el tipo de dato de la declaracion
def p_data_type(symbol):
    """data_type : TokenInt
                 | TokenBool
                 | TokenSet"""
    symbol[0] = symbol[1].upper()


######################### Declaracion Multiple ##################

# Lista de elementos para ciertas expresiones (print, etc)
def p_statement_comma_list(symbol):
    """comma_list : printable
                  | comma_list TokenComma printable"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]

# Se permite imprimir un string
def p_print_string_literal(symbol):
    """printable : TokenString"""
    symbol[0] = String(span(symbol, 1), symbol[1])


# se permite imprimir una expresion
def p_exp_print(symbol):
    """printable : expression"""
    symbol[0] = symbol[1]

###################     EXPRESSIONS     #######################

# Precedencia definida para las expresiones
precedence = (
    # De lenguaje
    ("right", 'TokenIf'),
    ("right", 'TokenElse'),

    # booleana
    ("left", 'TokenOr'),
    ("left", 'TokenAnd'),
    ("right", 'TokenNot'),
 
    # De comparacion
    ("nonassoc", 'TokenEqual', 'TokenUnequal'),
    ("nonassoc", 'TokenLess', 'TokenLesseq', 'TokenGreat', 'TokenGreateq'),

    # Para conjuntos
    ("left", 'TokenIntersection'),

    # Para enteros
    ("left", 'TokenPlus', 'TokenMinus'),
    ("left", 'TokenTimes', 'TokenDivide', 'TokenModule'),
)


# Un numero es una expresion valida
def p_exp_int_literal(symbol):
    "expression : TokenNumber"
    symbol[0] = Int(span(symbol,1),symbol[1])


# Un booleano es una expresion valida
def p_exp_bool_literal(symbol):
    """expression : TokenTrue
                  | TokenFalse"""
    symbol[0] = Bool(span(symbol,1),symbol[1].upper())

# Un string es una expresion valida
def p_exp_string_literal(symbol):
    "expression : TokenString"
    symbol[0] = String(symbol[1])

def p_expression_comma(symbol):
    """expression_comma : expression 
                        | expression TokenComma expression_comma"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = [symbol[1]] + symbol[3]

def p_expression_set(symbol):
    "expression : TokenOpenCurly expression_comma TokenCloseCurly"
    symbol[0] = Set(symbol[2])
    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)
    symbol[0].lexspan = start,end

# Un TokenID es una expresion valida
def p_expression_id(symbol):
    "expression : TokenID"
    symbol[0] = Variable(span(symbol, 1),symbol[1])


# Una expresion entre parentesis es validaression
def p_expression_group(symbol):
    """expression : TokenLParen expression TokenRParen"""
    symbol[0] = symbol[2]
    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)
    symbol[0].lexspan = start,end

###############   Operadores  Binarios  ####################

# Operadores binarios para int
def p_exp_int_binary(symbol):
    """expression : expression TokenPlus            expression
                  | expression TokenMinus           expression
                  | expression TokenTimes           expression
                  | expression TokenDivide          expression
                  | expression TokenModule          expression
                  | expression TokenIntersection    expression
                  | expression TokenOr              expression
                  | expression TokenAnd             expression"""
    operator = {
        '+': 'TokenPlus',
        '-': 'TokenMinus',
        '*': 'TokenTimes',
        '/': 'TokenDivide',
        '%': 'TokenModule',
        '<>': 'TokenIntersection',
        'or': 'TokenOr',
        'and': 'TokenAnd'
    }.get(symbol[2],None)

    start, _ = span(symbol, 1)
    _, end = span(symbol, 3)

    if operator == 'TokenPlus':
        symbol[0] = Plus((start, end), symbol[1], symbol[3])
    elif operator == 'TokenMinus':
        symbol[0] = Minus((start, end), symbol[1], symbol[3])
    elif operator == 'TokenTimes':
        symbol[0] = Times((start, end), symbol[1], symbol[3])
    elif operator == 'TokenDivide':
        symbol[0] = Divide((start, end), symbol[1], symbol[3])
    elif operator == 'TokenModule':
        symbol[0] = Modulo((start, end), symbol[1], symbol[3])
    elif operator == 'TokenIntersection':
        symbol[0] = Intersection((start, end), symbol[1], symbol[3])
    elif operator == 'TokenOr':
        symbol[0] = Or((start, end), symbol[1], symbol[3])
    elif operator == 'TokenAnd':
        symbol[0] = And((start, end), symbol[1], symbol[3])
    else:
        symbol[0] = Binary((start, end),operator, symbol[1], symbol[3])


# Operador unario menos '-'
def p_exp_int_unary(symbol):
    "expression : TokenMinus expression"
    symbol[0] = Unary('TokenMinus', symbol[2])


# Operador booleano 'not'
def p_exp_bool_unary(symbol):
    "expression : TokenNot expression"
    if isinstance(symbol[2], Bool):
        expr = eval(symbol[2].value.title())
        expr = str(not expr).upper()
        symbol[0] = Bool(expr)
    else:
        symbol[0] = Unary(symbol[1].upper(), symbol[2])

def p_exp_set_unary(symbol):
    """expression :  TokenMinValue expression
                  |  TokenMaxValue expression
                  |  TokenNumberElements expression"""
    operator = {
        '<?': 'TokenMinValue',
        '>?': 'TokenMaxValue',
        '$?': 'TokenNumberElements'
    }[symbol[1]]
    symbol[0] = Unary(operator,symbol[2])

# Operadores binarios de comparacion
def p_exp_bool_compare(symbol):
    """expression : expression TokenLess    expression
                  | expression TokenLesseq  expression
                  | expression TokenGreat   expression
                  | expression TokenGreateq expression
                  | expression TokenEqual   expression
                  | expression TokenUnequal expression"""
    operator = {
        '<': 'TokenLess',
        '<=': 'TokenLesseq',
        '>': 'TokenGreat',
        '>=': 'TokenGreateq',
        '==': 'TokenEqual',
        '/=': 'TokenUnequal'
    }.get(symbol[2], None)

    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)

    if operator == 'TokenLess':
        symbol[0] = Less((start, end), symbol[1], symbol[3])
    elif operator == 'TokenLesseq':
        symbol[0] = LessEq((start, end), symbol[1], symbol[3])
    elif operator == 'TokenGreat':
        symbol[0] = Great((start, end), symbol[1], symbol[3])
    elif operator == 'TokenGreateq':
        symbol[0] = GreatEq((start, end), symbol[1], symbol[3])
    elif operator == 'TokenEqual':
        symbol[0] = Equal((start, end), symbol[1], symbol[3])
    elif operator == 'TokenUnequal':
        symbol[0] = Unequal((start, end), symbol[1], symbol[3])
    else:
        symbol[0] = Binary((start, end),operator, symbol[1], symbol[3])

def p_exp_set_operation(symbol):
    """ expression : expression TokenUnion expression
                   | expression TokenSubset expression
                   | expression TokenPlusMap expression
                   | expression TokenMinusMap expression
                   | expression TokenDivideMap expression
                   | expression TokenModuleMap expression
                   | expression TokenTimesMap expression"""
    operator = {
        '++': 'TokenUnion',
        '@': 'TokenSubset',
        '<+>': 'TokenPlusMap',
        '<->': 'TokenMinusMap',
        '</>': 'TokenDivideMap',
        '<*>': 'TokenTimesMap',
        '<%>': 'TokenModuleMap'
    }.get(symbol[2], None)

    start, _ = span(symbol, 1)
    _, end = span(symbol, 2)

    if operator == 'TokenUnion':
        symbol[0] = Union((start, end), symbol[1], symbol[3])
    elif operator == 'TokenSubSet':
        symbol[0] = SubSet((start, end), symbol[1], symbol[3])
    elif operator == 'TokenPlusMap':
        symbol[0] = PlusMap((start, end), symbol[1], symbol[3])
    elif operator == 'TokenMinusMap':
        symbol[0] = MinusMap((start, end), symbol[1], symbol[3])
    elif operator == 'TokenDivideMap':
        symbol[0] = DivideMap((start, end), symbol[1], symbol[3])
    elif operator == 'TokenTimesMap':
        symbol[0] = TimesMap((start, end), symbol[1], symbol[3])
    elif operator == 'TokenModuleMap':
        symbol[0] = ModuleMap((start, end), symbol[1], symbol[3])
    else:
        symbol[0] = Binary((start, end),operator, symbol[1], symbol[3])

def p_empty(symbol):
    "empty :"
    pass

################### Errores #################################

# Error mostrado si el parser encuentra un error de sintaxis

def p_error(symbol):
    if symbol:
        text = symbol.lexer.lexdata
        message = "Error: Error de sintaxis en la linea %d columna %d: "
        data = (symbol.lineno, find_column(text, symbol), symbol.value)
        parser_error.append(message % data)
    else:
        parser_error.append("Error. Error de sintaxis en EOF")


# Constructor del parser
parser = yacc.yacc(start='program')
parser_error = []


# El archivo <input> es leido por el parser y 
# retorna el AST que representa el programadef parsing(data, debug=0):
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
    import sys      

    if argv is None:
        argv = sys.argv

    if len(argv) == 1:
        print "ERROR: No se encontro el archivo"
        return
    elif len(argv) > 3:
        print "ERROR: Numero invalido de argumentos"
        return

    if len(argv) == 3:
        debug = eval(argv[2])
    else:
        debug = 0

    # Abre el archivo
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
