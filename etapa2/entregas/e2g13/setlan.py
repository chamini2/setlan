#!/usr/bin/env python
# -*- coding: utf-8 -*-'''
from  sys import argv as argumentos_consola
'''
Created on 4/2/2015

@author: Jonnathan Ng    11-10199
         Manuel Gonzalez 11-10399
'''


import ply.yacc as yacc
import ply.lex as lexi
import expresiones
from AST import *

tokens = expresiones.tokens
parser_errores = []

#############################  STATEMENTS   ##################################
def p_program(p):
    'program : PROGRAM statement'
    p[0] = Program(p[2])
    
def p_statement_assing(p):
    'statement : IDENTIFIER ASSIGN expression'
    p[0] = Assign(p[1],p[3])
    
def p_statement_block(p):
    'statement : LCURLY declare statement_list RCURLY'
    p[0] = Block(p[3],p[2])

#############################     IN/OUT    ##################################
def p_statement_function_scan(p):
    'statement : SCAN IDENTIFIER'
    p[0] = Scan(Identifier(p[2]))
    
def p_statement_function_print(p):
    '''statement : PRINT comma_list
                 | PRINTLN comma_list'''
    p[0] = Print(p[1],p[2])


#############################  IF STATEMENT   ################################
def p_statement_if(p):
    '''statement : IF LPARENT expression RPARENT statement ELSE statement
                 | IF LPARENT expression RPARENT statement '''
    if len(p) == 8:
        p[0] = If(p[3],p[5],p[7])
    else:
        p[0] = If(p[3],p[5])

#############################  FOR STATEMENT     #############################
def p_statement_for(p):
    'statement :  FOR IDENTIFIER direction expression DO statement'
    p[0] = For(Identifier(p[2]),p[3],p[4],p[6])

def p_expression_direction(p):
    '''direction : MIN
                  | MAX
    '''
    p[0] = Direction(p[1])
    
####################      REPEAT-WHILE-DO STATEMENT     ###################### 
def p_statement_repeat_while_do(p):
    'statement :  REPEAT statement WHILE LPARENT expression RPARENT DO statement'
    p[0] = RepeatWhileDo(p[2],p[5],p[8])
    
def p_statement_while_do(p):
    'statement :  WHILE LPARENT expression RPARENT DO statement'
    p[0] = WhileDo(p[3],p[6])
    
def p_statement_repeat_while(p):
    'statement :  REPEAT statement WHILE LPARENT expression RPARENT'
    p[0] = RepeatWhile(p[2],p[5])



#############################    DECLARE     #################################
def p_declare_vars(p):
    'declare : USING declare_list IN'
    p[0] = DeclareList(p[2])

def p_declare_empty(p):
    'declare : empty'
    pass
    
def p_declare_list_type(p):
    'declare_list : type identifier_list SEMICOLON declare_list'
    p[0] = [TypeList(p[1],p[2])] + p[4]
    
def p_declare_list_type_empty(p):
    'declare_list : empty'
    p[0] = []

def p_identifier_list(p):
    'identifier_list : IDENTIFIER'
    p[0] = [p[1]]

def p_declare_list_continue_on(p):
    'identifier_list : IDENTIFIER COMMA identifier_list'
    p[0] = [p[1]] + p[3]

#########################     STATEMENT LIST(BLOCK)   ########################
def p_statement_list_continue(p):
    'statement_list : statement SEMICOLON statement_list'
    p[0] = [p[1]] + p[3]

def p_statement_list_empty(p):
    'statement_list : empty'
    p[0] = []
    
#############################   EXPRESSION    #################################
def p_expression_int(p):
    'expression : INTEGER'
    p[0] = Integer(p[1])

def p_expression_bool(p):
    '''expression : FALSE
                  | TRUE
    '''
    p[0] = Bool(p[1])
    
def p_expression_string(p):
    'expression : STRING'
    p[0] = String(p[1])

def p_expression_id(p):
    'expression : IDENTIFIER'
    p[0] = Identifier(p[1])

def p_type_data(p):
    '''type : INT
            | BOOL
            | SET
    '''
    p[0] = p[1]   
    
def p_expression_parent(p):
    ''' expression : LPARENT expression RPARENT'''
    p[0] = Parenthesis(p[2])   
    
##############################     SETS      #################################
def p_expression_set(p):
    ''' expression : LCURLY set_list RCURLY'''
    p[0] = Set(p[2])

def p_set_list(p):
    '''set_list : comma_list'''
    p[0] = p[1]

def p_set_list_empty(p):
    'set_list : empty'
    p[0] = []

def p_comma_list_expression(p):
    'comma_list : expression'
    p[0] = [p[1]]
    
def p_comma_list_expression_comma_continue(p):
    'comma_list : expression COMMA comma_list'
    p[0] = [p[1]] + p[3]
  
#############################    BINARY OP     ###############################
def p_expression_op_bin_integer(p):
    '''expression : expression PLUS expression            
                 | expression MINUS expression            
                 | expression TIMES expression            
                 | expression INTDIVISION expression            
                 | expression RESTDIVISION expression            
    '''
    p[0] = BinaryOP(p[1], expresiones.simbolos[p[2]]+' '+p[2],  p[3])
    
def p_expression_op_bin_compare(p):
    '''expression : expression EQUALBOOL expression
                 | expression UNEQUAL expression
                 | expression LESSTHAN expression
                 | expression LESSOREQUALTHAN expression
                 | expression GREATERTHAN expression
                 | expression GREATEROREQUALTHAN expression
                 | expression BELONG expression
    '''
    p[0] = BinaryOP(p[1],\
                    expresiones.simbolos.get(p[2],expresiones.simbolos_igual.get(p[2],None))+' '+p[2]\
                    ,p[3])
    
def p_expression_op_bin_bool(p):
    '''expression : expression AND expression
                  | expression OR expression '''
    
    p[0] = BinaryOP(p[1], expresiones.reservadas[p[2]]+' '+p[2], p[3])
    
def p_expression_op_set(p):
    '''expression : expression DOUBLEPLUS expression
                 | expression COUNTERSLASH expression
                 | expression INTERSECCION expression
    '''
    operadores = {
        '++' : 'UNION',
        '\\' : 'DIFFERENCE',
        '><' : 'INTERSECTION'
    }
    p[0] = BinaryOP(p[1],  operadores[p[2]]+' '+p[2],  p[3])


def p_expression_op_bin_map_to_set(p):
    '''expression : expression MAPPLUS expression
                 | expression MAPMINUS expression
                 | expression MAPTIMES expression
                 | expression MAPDIVIDE expression
                 | expression MAPREST expression
    '''
    p[0] = BinaryOP(p[1], expresiones.op_mapeados[p[2]]+' '+p[2],  p[3])
    
#############################    UNARY OP   ##################################
def p_expression_uminus(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryOP("NEGATE " + p[1], p[2])

def p_expression_op_not(p):
    'expression : NOT expression'
    p[0] = UnaryOP("NOT " + p[1], p[2])
        
def p_expression_op_unary_set(p):
    '''expression : MAXVALUESET expression
                  | MINVALUESET expression
                  | SIZESET expression'''
    p[0] = UnaryOP(expresiones.unarios_conjuntos[p[1]]+' '+p[1],   p[2])

#############################    EMPTY    #################################### 
def p_empty(p):
    'empty :'
    pass

############################     ERRROR HANDLING       #######################
def p_error(p):
    global parser_errores
    if parser_errores: return
    
    if p:
        msg = 'Error de síntaxis en la línea %d , columna %d. '
        msg += 'No se esperaba Token "%s".'
        value = p.value
        try:
            value = p.value
        except TypeError:
            pass
        
        msg = msg % (p.lineno , expresiones.obtener_columna(p) , value)
    else:
        msg = 'Error de síntasis: No se esperaba final de archivo.'

    parser_errores.append(msg)
    
##################    PRECEDENCE DEFINED FOR EXPRESSION  #####################
precedence = (
    # language
    ("right", 'IF'  ),
    ("right", 'ELSE'),
    # bool
    ("left", 'OR'),
    ("left", 'AND'),
    ("right", 'NOT'),
    # compare
    ("nonassoc", 'LESSTHAN', 'LESSOREQUALTHAN', 'GREATERTHAN', 'GREATEROREQUALTHAN'),
    ("nonassoc", 'EQUALBOOL', 'UNEQUAL'),
    ("nonassoc", 'BELONG'),
    # int
    ("left", 'PLUS', 'MINUS'),
    ("left", 'TIMES', 'INTDIVISION', 'RESTDIVISION'),
    #set
    ('left','DOUBLEPLUS','COUNTERSLASH'),
    ('left','INTERSECCION'),
    #map to set
    ('left','MAPPLUS','MAPMINUS'),
    ('left','MAPTIMES','MAPDIVIDE','MAPREST'),
    #unary over sets
    ('nonassoc','MAXVALUESET','MINVALUESET','SIZESET'),
    # int
    ("right", 'UMINUS'),
)

def salir(mensaje = "ERROR: Ejecute el interprete de la forma: setlan <dir_archivo>",
                codigo = -1):
    print mensaje
    exit(codigo)

def setlan(argv = None):
    
    if argv is None:
        argv = argumentos_consola
        
    if len(argv) != 2:
        salir()
        
    ruta_archivo = argv[1]
 
    lexer = lexi.lex(module=expresiones)
    parser = yacc.yacc()
    
    try:
        with open(ruta_archivo) as file_input:
            content = file_input.read()
            content = content.expandtabs(5)
    except IOError as e :
        salir(str(e) + "\nError: Compruebe que el archivo existe o tiene permisos de lectura")
    
    
    
    lexer.errores  = []
    program = parser.parse(content,lexer)
    if lexer.errores:
        for error in lexer.errores:
            print error
        
    elif parser_errores:
        for error in parser_errores:
            print error
    else:
        program.print_tree()
        
    file_input.close()


if __name__ == '__main__':        
    setlan()
