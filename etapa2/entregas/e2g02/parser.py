#!/usr/bin/env python
# -*- coding: UTF-8 -*-

############################
#  Proyecto I - CI3725     #
#  Grupo 2                 #
#  Luis Colorado 09-11086  #
#  Nicolas Manan 06-39883  #
############################

import ply.yacc as yacc
from lexer import tokens, lexer_error, find_column, lexing
from ast import *

############# INICIO DE LA GRAMATICA SETLAN ###################

# Inicio de un programa Setlan
def p_program(symbol):
    "program : TokenProgram statement"
    symbol[0] = Program(symbol[2])

################### STATEMENTS ################################

# La sentencia de bloque con sus multiples formas de escritura
def p_statement_block(symbol):
    """statement : TokenOpenCurly statement_list TokenCloseCurly
                 | TokenOpenCurly TokenUsing declare_list TokenIn statement_list TokenCloseCurly
                 | TokenOpenCurly empty empty TokenCloseCurly"""
    if len(symbol) == 4:
        symbol[0] = Block(symbol[2])
    elif len(symbol) == 5:
        symbol[0] =  Block(symbol[2],None,None,1)
    else:
        symbol[0] = Block(symbol[5], symbol[2], symbol[3])

# Asignacion de Variables
def p_statement_assign(symbol):
    "statement : TokenID TokenAssign expression"
    symbol[0] = Assign(Variable(symbol[1]), symbol[3])


############# Entrada y Salida ################

# Lectura de variables dadas por el usuario
def p_statement_scan(symbol):
    "statement : TokenScan TokenID"
    symbol[0] = Scan(Variable(symbol[2]))


# Declaracion de impresion
def p_statement_print(symbol):
    """statement : TokenPrint comma_list
                 | TokenPrintln comma_list"""
    if symbol[1].upper() == 'TokenPrint':
        symbol[0] = Print(symbol[2])
    else:
        if len(symbol) == 3:
            symbol[0] = Print(symbol[2] + [String('"\\n"')])
        else:
            symbol[0] = Print([String('"\\n"')])

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
    if len(symbol) == 4:
        symbol[0] = [(symbol[1], symbol[2])]
    else:
        symbol[0] = [(symbol[1],symbol[2])] + symbol[4]


# Regla para crear multiples variables en una declaracion
def p_statement_declare_comma_list(symbol):
    """declare_comma_list : TokenID
                          | declare_comma_list TokenComma TokenID"""
    if len(symbol) == 2:
        symbol[0] = [Variable(symbol[1])]
    else:
        symbol[0] = symbol[1] + [Variable(symbol[3])]


############## Condicional ####################

# La declaracion 'If'
def p_statement_if(symbol):
    """statement : TokenIf expression statement
                 | TokenIf expression statement TokenElse statement"""
    if len(symbol) == 4:
        symbol[0] = If(symbol[2], symbol[3])
    else:
        symbol[0] = If(symbol[2], symbol[3], symbol[5])


################## Ciclos #####################

# Declaracion del for
def p_statement_for(symbol):
    """statement : TokenFor TokenID TokenMin expression TokenDo statement
                 | TokenFor TokenID TokenMax expression TokenDo statement"""
    symbol[0] = For(Variable(symbol[2]), symbol[4], symbol[6], symbol[3])


# Declaracion While
def p_statement_while(symbol):
    "statement : TokenWhile expression TokenDo statement"
    symbol[0] = While(symbol[2], symbol[4])

# Declaracion Repeat
def p_statement_whileRepeat(symbol):
    """statement : TokenRepeat statement_list TokenWhile expression TokenDo statement"""
    symbol[0] = WhileRepeat(symbol[4],symbol[2],symbol[6])

def p_statement_repeatWhile(symbol):
    " statement : TokenRepeat statement_list TokenWhile expression "
    symbol[0] = RepeatWhile(symbol[4], symbol[2])
######################## Tipos de Datos #######################

# Para el tipo de dato de la declaracion
def p_data_type(symbol):
    """data_type : TokenInt
                 | TokenBool
                 | TokenSet"""
    symbol[0] = symbol[1]


######################### Declaracion Multiple ##################

# Lista de elementos para ciertaas expresiones (print, etc)
def p_statement_comma_list(symbol):
    """comma_list : expression
                  | comma_list TokenComma expression"""
    if len(symbol) == 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = symbol[1] + [symbol[3]]



###################     EXPRESSIONS     #######################

# Precedence defined for expressions
precedence = (
    # bool
    ("left", 'TokenOr'),
    ("left", 'TokenAnd'),
    ("right", 'TokenNot'),
 
    # compare
    ("nonassoc", 'TokenEqual', 'TokenUnequal'),
    ("nonassoc", 'TokenLess', 'TokenLesseq', 'TokenGreat', 'TokenGreateq'),

    # range
    ("left", 'TokenIntersection'),

    # int
    ("left", 'TokenPlus', 'TokenMinus'),
    ("left", 'TokenTimes', 'TokenDivide', 'TokenModule'),
)


# Un numero es una expresion valida
def p_exp_int_literal(symbol):
    "expression : TokenNumber"
    symbol[0] = Int(symbol[1])


# Un booleano es una expresion valida
def p_exp_bool_literal(symbol):
    """expression : TokenTrue
                  | TokenFalse"""
    symbol[0] = Bool(symbol[1].upper())

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

# Un TokenID es una expresion valida
def p_expression_id(symbol):
    "expression : TokenID"
    symbol[0] = Variable(symbol[1])


# Una expresion entre parentesis es validaression
def p_expression_group(symbol):
    """expression : TokenLParen expression TokenRParen"""
    symbol[0] = symbol[2]

###############   Operadores    ####################

# Operadores binarios para int
def p_exp_int_binary(symbol):
    """expression : expression TokenPlus   expression
                  | expression TokenMinus  expression
                  | expression TokenTimes  expression
                  | expression TokenDivide expression
                  | expression TokenModule expression"""
    operator = {
        '+': 'TokenPlus +',
        '-': 'TokenMinus -',
        '*': 'TokenTimes *',
        '/': 'TokenDivide /',
        '%': 'TokenModule %'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


# Operador unario menos '-'
def p_exp_int_unary(symbol):
    "expression : TokenMinus expression"
    symbol[0] = Unary('TokenMinus', symbol[2])

# Operadores binarios booleanos
def p_exp_bool_binary(symbol):
    """expression : expression TokenOr      expression
                  | expression TokenAnd     expression"""
    operator = {
    'or' : 'TokenOr',
    'and': 'TokenAnd',
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])


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
        '<?': 'TokenMinValue <?',
        '>?': 'TokenMaxValue >?',
        '$?': 'TokenNumberElements $?'
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
        '<': 'TokenLess <',
        '<=': 'TokenLesseq <=',
        '>': 'TokenGreat >',
        '>=': 'TokenGreateq >=',
        '==': 'TokenEqual ==',
        '/=': 'TokenUnequal /='
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])

def p_exp_set_operation(symbol):
    """ expression : expression TokenUnion expression
                   | expression TokenSubset expression
                   | expression TokenPlusMap expression
                   | expression TokenMinusMap expression
                   | expression TokenDivideMap expression
                   | expression TokenModuleMap expression
                   | expression TokenTimesMap expression
                   | expression TokenIntersection expression"""
    operator = {
        '++': 'TokenUnion ++',
        '@': 'TokenSubset @',
        '<+>': 'TokenPlusMap <+>',
        '<->': 'TokenMinusMap <->',
        '</>': 'TokenDivideMap </>',
        '<*>': 'TokenTimesMap <*>',
        '<%>': 'TokenModuleMap <%>',
        '><' : 'TokenIntersection ><'
    }[symbol[2]]
    symbol[0] = Binary(operator, symbol[1], symbol[3])

def p_empty(symbol):
    "empty :"
    pass

################### Errores #################################

# Error mostrado si el parser encuentra un error de sintaxis

def p_error(symbol):
    if symbol:
        text = symbol.lexer.lexdata
        message = "Error: Error de sintaxis en la linea %d columna %d: "
        message += "Token inesperado '%s' "
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
