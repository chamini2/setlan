#!/usr/bin/env python
# -*- coding: UTF-8 -*-

'''
Creado el 05/02/2015
Ult. Modificacion el 09/02/2015

@author:  Aldrix Marfil     10-10940
@author:  Leonardo Martinez 11-10576
'''

import ply.yacc  as yacc
from   arbolST   import *
from   lexer     import tokens, lexer_errorList, find_column

###############################################################################
#									INICIO				   					  #
###############################################################################

# Manejo del Token semilla 'program'. 
# Siempre se empieza con la palabra reservada program.
def p_program(symbol):
	"program : PROGRAM instruccion"
	symbol[0] = Program(symbol[2])

################################################################################
#                                  VACIO                                       # 
################################################################################

def p_vacio(symbol):
    "vacio :"
    pass

################################################################################
#							   INSTRUCCIONES    					           # 
################################################################################

# Regla para la asignacion a variables.
# IDENTIFIER '=' expresion
def p_instruccion_assign(symbol):
    "instruccion : IDENTIFIER ASSIGN expresion"
    if symbol[2] == '=':
        symbol[0] = Assign(Identifier(symbol[1]),symbol[3])
 
# Regla para las impresiones en pantalla
def p_instruccion_print(symbol):
    """instruccion : PRINT lista_expresiones
                   | PRINTLN lista_expresiones"""
 
    if symbol[1].upper() == "PRINTLN":
        symbol[0] = Print(symbol[1].upper(), symbol[2] + [String("\\n")])
    else:
        symbol[0] = Print(symbol[1].upper(), symbol[2])

# Regla para leer una variable
def p_instruccion_scan(symbol):
    "instruccion : SCAN IDENTIFIER"
    symbol[0] = Scan(Identifier(symbol[2]))

################################################################################
#						    INSTRUCCION DE BLOQUE  					           # 
################################################################################

# Regla para los bloques de instrucciones.
def p_instruccion_block(symbol):
    """instruccion : OPENCURLY vacio CLOSECURLY
                   | OPENCURLY lista_instrucciones CLOSECURLY
                   | OPENCURLY declaracion lista_instrucciones CLOSECURLY"""
    if len(symbol) <= 4:
        symbol[0] = Block(symbol[2])
    else:
        symbol[0] = Block(symbol[3],symbol[2])

# Regla para las declaraciones
def p_instruccion_declare(symbol):
    "declaracion : USING lista_declaraciones IN"
    symbol[0] = Using(symbol[2])

################################################################################
#                         LISTAS PARA LOS BLOQUES                              #
################################################################################
 
# Lista de Instrucciones
def p_instruction_list(symbol):
    """lista_instrucciones : instruccion
                           | instruccion SEMICOLON
                           | instruccion SEMICOLON lista_instrucciones"""
    if len(symbol) <= 3:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = [symbol[1]] + symbol[3]
 
# Lista de Expresiones
def p_expresion_list(symbol):
    """lista_expresiones : expresion
                         | expresion COMMA lista_expresiones"""
    if len(symbol) <= 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = [symbol[1]] + symbol[3]
 
def p_identificador_list(symbol):
    """lista_identificadores : IDENTIFIER
                             | IDENTIFIER COMMA lista_identificadores"""   
    if len(symbol) <= 2:
        symbol[0] = [symbol[1]]
    else:
        symbol[0] = [symbol[1]] + symbol[3]
 
def p_declaracion_list(symbol):
    """lista_declaraciones : type lista_identificadores SEMICOLON
                           | type lista_identificadores SEMICOLON lista_declaraciones"""
     
    if len(symbol) <= 4:
        symbol[0] = [Declaration(symbol[1],symbol[2])]
    else:
        symbol[0] = [Declaration(symbol[1],symbol[2])] + symbol[4]

###############################################################################
#					           INSTRUCCION IF              					  #
###############################################################################

def p_instruccion_if(symbol):
    """instruccion : IF LPARENTHESIS expresion RPARENTHESIS instruccion ELSE instruccion 
                   | IF LPARENTHESIS expresion RPARENTHESIS instruccion"""
    if len(symbol) == 8:
        symbol[0] = If(symbol[3],symbol[5],symbol[7])
    else:
        symbol[0] = If(symbol[3],symbol[5])

###############################################################################
#					           INSTRUCCION FOR             					  #
###############################################################################

def p_instruccion_for(symbol):
    "instruccion : FOR IDENTIFIER direccion expresion DO instruccion"
    symbol[0] = For(Identifier(symbol[2]),symbol[3],symbol[4],symbol[6])

def p_expresion_direccion(symbol):
    """direccion : MIN
                 | MAX"""
    symbol[0] = Direction(symbol[1])

###############################################################################
#					   INSTRUCCION REPEAT - WHILE - DO     					  #
###############################################################################

def p_instruccion_repeat_while_do(symbol):
    "instruccion : REPEAT instruccion WHILE LPARENTHESIS expresion RPARENTHESIS DO instruccion"
    symbol[0] = RepeatWhileDo(symbol[2],symbol[5],symbol[8])

def p_instruccion_while_do(symbol):
    "instruccion : WHILE LPARENTHESIS expresion RPARENTHESIS DO instruccion"
    symbol[0] = WhileDo(symbol[3],symbol[6])

def p_instruccion_repeat_while(symbol):
    "instruccion : REPEAT instruccion WHILE LPARENTHESIS expresion RPARENTHESIS"
    symbol[0] = RepeatWhile(symbol[2],symbol[5])

###############################################################################
#							     EXPRESIONES			   					  #
###############################################################################

# Un numero es una expresion valida.
def p_expresion_number(symbol):
 	"expresion : NUMBER"
 	symbol[0] = Number(symbol[1])

# STRING es una expresion valida.
def p_expresion_string(symbol):
	"expresion : STRING"
	symbol[0] = String(symbol[1])

# Un valor booleano es una expresion valida.
def p_expresion_bool(symbol):
    """expresion : FALSE
                 | TRUE """
    symbol[0] = Bool(symbol[1])

# IDENTIFIER es una expresion variable.
def p_expresion_identifier(symbol):
 	"expresion : IDENTIFIER"
 	symbol[0] = Identifier(symbol[1])

# Una expresion entre parentesis es una expresion valida.
def p_expression_parentesis(symbol):
 	"expresion : LPARENTHESIS expresion RPARENTHESIS"
 	symbol[0] = Parenthesis(symbol[2])

################################################################################
#                                CONJUNTOS                                     #
################################################################################

# Un conjunto es una expresion valida.
def p_expresion_set(symbol):
    """expresion : OPENCURLY vacio CLOSECURLY 
                 | OPENCURLY lista_expresiones CLOSECURLY"""
    symbol[0] = Set(symbol[2])

################################################################################
#							   TIPOS DE DATO   						           # 
################################################################################

# Tipos de datos permitidos para las variables.
def p_tipo_dato(symbol):
    """type : INT
            | BOOL
            | SET"""
    symbol[0] = Type(symbol[1])

################################################################################
#                            OPERADORES BINARIOS                               #
################################################################################
 
# Operadores binarios para las operaciones matematicas
def p_binary_operator_math(symbol):
    """expresion : expresion PLUS expresion
                 | expresion MINUS expresion
                 | expresion TIMES expresion
                 | expresion DIVIDE expresion
                 | expresion MODULE expresion"""
    symbol[0] = BinaryOperator(symbol[1],symbol[2],symbol[3])
 
# Operadores binarios para la comparacion
def p_binary_operator_compare(symbol):
    """expresion : expresion LESS expresion
                 | expresion GREAT expresion
                 | expresion LESSEQ expresion
                 | expresion GREATEQ expresion
                 | expresion EQUAL expresion
                 | expresion UNEQUAL expresion"""   
    symbol[0] = BinaryOperator(symbol[1],symbol[2],symbol[3])
 
# Operadores binarios sobre conjuntos
def p_binary_operator_sets(symbol):
    """expresion : expresion CONTAINMENT expresion
                 | expresion UNION expresion
                 | expresion INTERSECTION expresion
                 | expresion DIFERENCE expresion
                 | expresion PLUSMAP expresion
                 | expresion MINUSMAP expresion
                 | expresion TIMESMAP expresion
                 | expresion DIVIDEMAP expresion
                 | expresion MODULEMAP expresion"""   
    symbol[0] = BinaryOperator(symbol[1],symbol[2],symbol[3])

# Operadores binarios logicos
def p_binary_operator_logical(symbol):
    """expresion : expresion AND expresion
                 | expresion OR expresion"""
    symbol[0] = BinaryOperator(symbol[1],symbol[2],symbol[3])
    
################################################################################
#						     OPERADORES UNARIOS 					           # 
################################################################################

#Operador unario numero negativo
def p_expresion_unary_minus(symbol):
    "expresion : MINUS expresion %prec UNARY_MINUS"
    symbol[0] = UnaryOperator(symbol[1],symbol[2])

# Operador unario de negacion logica
def p_expresion_not(symbol): 
    "expresion : NOT expresion"
    symbol[0] = UnaryOperator(symbol[1],symbol[2])

def p_expresion_unary_set(symbol):
    """expresion : MAXVALUE expresion
                 | MINVALUE expresion
                 | NUMELEMENTS expresion"""

    symbol[0] = UnaryOperator(symbol[1],symbol[2])

################################################################################
#                        PRECEDENCIA DE OPERADORES                             #
################################################################################

precedence = (

    #Lenguaje
     ("right", 'IF' ),
     ("right", 'ELSE'),

    #Operadores Aritmeticos
     ("left", 'PLUS', 'MINUS'),
     ("left", 'TIMES', 'DIVIDE', 'MODULE'),

    #Operadores Comparativos
     ("nonassoc", 'LESS', 'LESSEQ', 'GREAT', 'GREATEQ'),
     ("nonassoc", 'EQUAL', 'UNEQUAL'),
     ("nonassoc", 'CONTAINMENT'),

    #Operadores Booleanos
     ("left", 'OR'),
     ("left", 'AND'),
     ("right", 'NOT'),

    #Operadores sobre Conjuntos
     ('left','UNION','DIFERENCE'),
     ('left','INTERSECTION'),

    #Operadores unarios aritmeticos
     ("right",'UNARY_MINUS'),

    #Operadores entre Conjuntos-Aritmeticas
     ('left','PLUSMAP','MINUSMAP'),
     ('left','TIMESMAP','DIVIDEMAP','MODULEMAP'),

    #Operadores unarios sobre conjuntos
     ('nonassoc','MAXVALUE','MINVALUE','NUMELEMENTS'),
)
 
################################################################################
#                              MANEJO DE ERRORES                               #
################################################################################
 
#Manejo de errores
def p_error(symbol):

    if symbol:
        code = symbol.lexer.lexdata
        errorString  = 'Error: se encontro un caracter inesperado {0}' .format(symbol.value)
        errorString += '(Línea {0}, Columna {1})'.format(symbol.lineno, find_column(code,symbol))
        parser_errorList.append(errorString)
    else:
        parser_errorList.append('Error: error de sintaxis al final del archivo.')


#Lista de Errores del Parser
parser_errorList = []

################################################################################

#Contrustor del parser
def build_parser(code):
    
    parser = yacc.yacc(debug=True)
    parser.error = 0
    arbol = parser.parse(code)
    if parser.error:
        ast = None
    return arbol

if __name__ == '__main__':
    pass