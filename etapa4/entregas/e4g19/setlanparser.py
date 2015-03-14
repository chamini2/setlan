
# -*- coding: utf-8 -*-
'''
Created on 31/1/2015

@author: David Klie
@author : Gustavo Benzecri
'''

import ply.yacc,ply.lex,sys
from setlanlex import *
from Arbol import *

parser_error=[]


# Inicio del programa, semilla de la gramatica
def p_program(p):
    '''program : PROGRAM statement
    '''
    p[0]=Program(p[2])
    

# Bloque del programa
def p_block(p):
    'block : BLOCK using blockInstruction END_BLOCK'
    p[0]=Block(p[2],p[3])

# Seccion opcional de un bloque donde se definen variables
def p_using(p):
    '''using : USING declaration IN
            | empty
    '''
    if len(p)==4:
        p[0]=Using(p[2])
        p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
    

# Declaracion de las variables
def p_declaration(p):
    '''declaration : type identifier_list SEMICOLON declaration
                | empty
    ''' 
    if len(p)==5:
        p[0]=[(p[1],p[2])]
        if p[4]!=None:
            p[0]+=p[4]
    
def p_identifier_list(p):
    '''identifier_list : IDENTIFIER COMMA identifier_list
                       | IDENTIFIER
    ''' 
    if len(p)==4:
        p[0]=[p[1]]+p[3]
    elif len(p)==2:
        p[0]=[p[1]]

# Tipo de la variable
def p_type(p):
    '''type : INT
            | BOOL 
            | SET
    '''
    p[0]=p[1]
    
def p_blockInstruction(p):
    ''' blockInstruction : statement SEMICOLON blockInstruction
                        | empty
    '''
    if len(p)==4:
        p[0]=[p[1]]
        if p[3]!=None:
            p[0]+=p[3]

def p_statement(p):
    '''statement : IDENTIFIER ASSIGN expression
                |  SCAN IDENTIFIER
                |  print
                | if
                | for
                | repeat_while_do
                | block
    '''
    if len(p)==4:
        p[0]=Assign(Variable(p[1]),p[3])
        p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
    elif len(p)==3:
        p[0]=Scan(Variable(p[2]))
        p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
    else:
        p[0]=p[1]
        
################################################################
#                EXPRESIONES
################################################################

def p_identifier(p):
    'expression : IDENTIFIER'
    p[0] = Variable(p[1])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
    
def p_group_expression(p):
    'expression : LPAREN expression RPAREN %prec GROUP'
    p[0] = GroupedExpression(p[2])

############ Expresiones de conjuntos ############

def p_binary_set_expression(p):
    '''expression :   expression UNION expression
                        | expression INTERSECTION expression
                        | expression DIFFERENCE expression
                        | expression SETPLUS expression
                        | expression SETMINUS expression
                        | expression SETTIMES expression
                        | expression SETDIV expression
                        | expression SETMOD expression
    '''
    p[0] = BinaryExpression(p[1],p[2],p[3])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))

def p_unary_set_expression(p):
    '''expression :   MINSET expression
                        | MAXSET expression
                        | CARDINALITY expression
    '''
    p[0] = UnaryExpression(p[1],p[2])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))

def p_group_set_expression(p):
    '''expression : BLOCK set_element END_BLOCK %prec GROUP'''
    p[0]= SetExpression(p[2])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
    
def p_set_element(p):
    '''set_element :  expression COMMA set_element
                    | expression
                    | empty 
    '''
    if len(p)==4:
        p[0]=[p[1]]
        if p[3]!=None:
            p[0]=[p[1]]+p[3]
    elif p[1]!=None:
        p[0]=[p[1]]

############ Expresiones de enteros ############
            
def p_binary_int_expression(p):
    '''expression : expression PLUS expression
                        | expression MINUS expression
                        | expression TIMES expression
                        | expression DIVIDE expression
                        | expression MOD expression
    '''
    p[0] = BinaryExpression(p[1],p[2],p[3])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
                               
def p_unary_int_expression(p):
    'expression : MINUS expression %prec UMINUS'
    p[0] = UnaryExpression(p[1],p[2])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
    
def p_number(p):
    'expression : INTEGER'
    p[0] = Integer(p[1])
    
    
############ Expresiones booleanas ############    
            
def p_binary_bool_expression(p):
    '''expression :  expression GREATERTHAN expression
                        | expression LESSTHAN expression
                        | expression GREATEREQUALTHAN expression
                        | expression LESSEQUALTHAN expression
                        | expression EQUALS expression
                        | expression NOTEQUALS expression
                        | expression AND expression
                        | expression OR expression
                        | expression ARROBA expression
    '''
    p[0] = BinaryExpression(p[1],p[2],p[3])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))
    
def p_unary_bool_expression(p):
    '''expression : NOT expression'''
    p[0] = UnaryExpression(p[1],p[2])
    p[0].line_col=(p.lineno(1),find_column(p.lexer.lexdata,p.lexer))

def p_boolean_constant(p):
    '''expression : TRUE
                       | FALSE
    '''
    p[0] = Boolean(p[1])
    
################################################################
#                INSTRUCCIONES
################################################################


############ Salida ############   
    
def p_print(p):
    '''print : PRINT values
            |  PRINTLN values
    '''
    p[0]=Print(p[1],p[2])
    
def p_values(p):
    '''values : STRING COMMA values
              | expression COMMA values
              | STRING
              | expression
    '''
    if len(p)==4:
        p[0] = Values(p[1],p[3])
    else:
        p[0]= Values(p[1])
        
############ If Else ############   
        
def p_if(p):
    '''if : IF LPAREN expression RPAREN statement %prec IFX
          | IF LPAREN expression RPAREN statement else
    '''
    if len(p)==7:
        p[0]=if_statement(p[3],p[5],p[6])
    else:
        p[0]=if_statement(p[3],p[5])
        
def p_else(p):
    '''else : ELSE statement
    '''
    p[0]=else_statement(p[2])
    
    
############ For y Repeat While Do############

def p_for(p):
    '''for :  FOR IDENTIFIER MIN expression do
            | FOR IDENTIFIER MAX expression do
    '''
    p[0]=For_statement(Variable(p[2]),p[3],p[4],p[5])
    
def p_while(p):
    '''while : WHILE LPAREN expression RPAREN %prec GROUP'''
    p[0] = while_statement(p[3])
    
def p_repeat(p):
    '''repeat :   REPEAT statement
    '''
    p[0] = repeat_statement(p[2])
    
def p_do(p):
    '''do :   DO statement
    '''
    p[0]=Do(p[2])

def p_repeat_while_do(p):
    '''repeat_while_do : repeat while do
                        | repeat while
                        | while do
    '''
    if (len(p) == 3):
        if (isinstance(p[1],while_statement)):
            p[0] = repeat_while_do(While = p[1], Do = p[2])
        else:
            p[0] = repeat_while_do(Repeat = p[1], While = p[2])
    else:
        p[0] = repeat_while_do(Repeat = p[1], While = p[2], Do = p[3])
        
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        msj= "ERROR: unexpected token \'%s\' at line %d, column %d"
        msj=msj % (p.value,p.lexer.lineno,find_column(p.lexer.lexdata,p))
        parser_error.append(msj)
    else:
        parser_error.append('ERROR: End of file reached')

precedence = (
    # Operador de asignacion
    ('right', 'ASSIGN'),
    ('nonassoc','IFX'),
    ('nonassoc','ELSE'),
    # Operadores booleanos
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'NOT'),
    ('nonassoc', 'EQUALS', 'NOTEQUALS'),
    ('nonassoc', 'LESSTHAN', 'GREATERTHAN', 'LESSEQUALTHAN', 'GREATEREQUALTHAN'),
    ('nonassoc', 'ARROBA'),
    # Operadores de conjunto
    ('left', 'UNION', 'DIFFERENCE'),
    ('left', 'INTERSECTION'),
    ('left', 'SETPLUS', 'SETMINUS'),
    ('left', 'SETTIMES', 'SETDIV', 'SETMOD'),
    ('nonassoc', 'MINSET', 'MAXSET', 'CARDINALITY'),
    # Operadores de enteros
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MOD'),
    ('right', 'UMINUS'),
    ('nonassoc', 'GROUP')
)
